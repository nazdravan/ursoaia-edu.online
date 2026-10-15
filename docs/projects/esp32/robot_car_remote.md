---
category: ESP32
tags: [Joystick, WiFi, MicroPython, Telecomandă, Robot]
summary: Telecomandă wireless cu joystick PS2 și ESP32 care comandă robotul ESP32-CAM 4WD prin HTTP peste Wi-Fi.
image: assets/images/projects/esp32/preview-robot_car_remote.jpg
---

# Telecomandă wireless pentru robot ESP32-CAM 4WD

Construiește o telecomandă cu un ESP32 DevKit V1 și un modul joystick PS2 care se conectează la rețeaua Wi-Fi a unui robot ESP32-CAM 4WD și îi trimite comenzi de mișcare prin cereri HTTP. Un buton suplimentar aprinde și stinge proiectorul LED de pe robot.

![Kitul ESP32 Camera 4WD Robot Car comandat de telecomanda cu joystick](../../assets/images/projects/esp32/preview-robot_car_remote.jpg)

## Descriere

Robotul ESP32-CAM creează un punct de acces Wi-Fi (`ESP32-CAM Robot`, fără parolă) și expune un API HTTP simplu pe `http://192.168.4.1`. Telecomanda:

1. Se conectează la AP-ul robotului și clipește LED-ul cât timp caută rețeaua.
2. Citește două axe ADC (VRX, VRY) de la joystick și determină direcția: înainte, înapoi, stânga, dreapta sau oprit.
3. Trimite comenzi HTTP `GET /go`, `/back`, `/left`, `/right`, `/stop` doar când direcția se schimbă, plus reîmprospătare la fiecare 500 ms ca să compenseze pachetele pierdute.
4. Citește un buton cu debounce de 200 ms și comută proiectorul LED prin `/ledon` / `/ledoff`.

## Componente

| Component | Cantitate |
|-----------|-----------|
| ESP32 DevKit V1 | 1 |
| Modul joystick PS2 | 1 |
| Buton push | 1 |
| Robot ESP32-CAM 4WD (kit LAFVIN) | 1 |

## Conectare

[[wokwi:esp32-robot-car-remote]]

```board
ESP32 DevKit V1
┌──────────────────────┐
│                      │
│  GPIO 34 ◄─── VRX    │  Joystick axa X (stânga/dreapta)
│  GPIO 35 ◄─── VRY    │  Joystick axa Y (înainte/înapoi)
│  3.3V ────── +5V     │  Alimentare joystick (3.3V este suficient)
│  GND ─────── GND     │  Masă joystick
│                      │
│  GPIO 33 ◄─── BTN    │  Buton push (al doilea picior la GND)
│                      │
│  GPIO 2 ───► LED     │  LED încorporat (status conexiune)
│                      │
└──────────────────────┘
```

!!! tip "De ce GPIO 34 și 35"
    Sunt pini doar de intrare, conectați la ADC1. ADC2 nu poate fi folosit când Wi-Fi este activ pe ESP32, deci toate citirile analogice trebuie să rămână pe ADC1.

Pinul `SW` al joystick-ului (apăsarea stick-ului) nu se conectează — nu este folosit.

## Maparea joystick → direcție

Domeniul ADC este 0–4095. Centrul este aproximativ 2048. Definim o zonă moartă între 1400 și 2700 (centru ± ~30%) ca să ignorăm zgomotul când stick-ul este eliberat.

```
         VRY < 1400
           ↑ ÎNAINTE
           │
VRX < 1400 ◄── STOP ──► VRX > 2700
  STÂNGA   (zonă moartă)  DREAPTA
           │
           ↓ ÎNAPOI
         VRY > 2700
```

Când ambele axe ies din zona moartă, câștigă axa cu deflecția mai mare față de centru.

## API-ul robotului

| Endpoint | Acțiune |
|----------|---------|
| `GET /go` | Înainte |
| `GET /back` | Înapoi |
| `GET /left` | Viraj stânga |
| `GET /right` | Viraj dreapta |
| `GET /stop` | Oprește motoarele |
| `GET /ledon` | Aprinde LED-ul de pe robot |
| `GET /ledoff` | Stinge LED-ul de pe robot |

Toate răspund cu `OK` (`text/html`). Robotul mai expune `GET /capture` pentru o singură cadră JPEG și `GET :81/stream` pentru flux MJPEG continuu.

## Cod

```python
import network
import urequests
import socket
import time
from machine import Pin, ADC

# --- Configurare hardware ---

# Joystick pe ADC1 (sigur cu Wi-Fi activ)
vrx = ADC(Pin(34))
vry = ADC(Pin(35))
vrx.atten(ADC.ATTN_11DB)  # Domeniu complet 0-3.3V
vry.atten(ADC.ATTN_11DB)

# Buton (active LOW cu pull-up intern)
button = Pin(33, Pin.IN, Pin.PULL_UP)

# LED de stare (încorporat pe DevKit V1)
led = Pin(2, Pin.OUT)

# --- Constante ---

ROBOT_IP = "http://192.168.4.1"
WIFI_SSID = "ESP32-CAM Robot"
WIFI_PASS = ""

# Praguri zonă moartă (centru ~2048, ±30%)
DEAD_LOW = 1400
DEAD_HIGH = 2700

# Timing (ms)
LOOP_INTERVAL = 20
REPEAT_INTERVAL = 150
DEBOUNCE_TIME = 200

# Direcții
STOP = "stop"
FORWARD = "go"
BACKWARD = "back"
LEFT = "left"
RIGHT = "right"

# --- Stare ---

prev_direction = None
last_command_time = 0
last_button_time = 0
light_on = False
wlan = None


def connect_wifi():
    """Conectează la AP-ul robotului. Clipește LED-ul cât timp caută."""
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    while not wlan.isconnected():
        led.value(not led.value())
        time.sleep_ms(500)

    led.value(1)  # Solid ON = conectat
    print("Connected:", wlan.ifconfig())


def send_command(cmd):
    """Trimite GET la robot fire-and-forget — nu așteaptă răspunsul."""
    print("-> send_command:", cmd)
    try:
        s = socket.socket()
        s.settimeout(0.3)
        s.connect(("192.168.4.1", 80))
        req = "GET /" + cmd + " HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: close\r\n\r\n"
        s.send(req.encode())
        s.close()
    except Exception as e:
        print("   ERROR:", e)


def read_direction():
    """Citește joystick-ul și întoarce direcția."""
    x = vrx.read()
    y = vry.read()

    dx = x - 2048
    dy = y - 2048

    x_outside = x < DEAD_LOW or x > DEAD_HIGH
    y_outside = y < DEAD_LOW or y > DEAD_HIGH

    print("ADC x={} y={} dx={} dy={} x_out={} y_out={}".format(x, y, dx, dy, x_outside, y_outside))

    if not x_outside and not y_outside:
        return STOP

    # Prioritate: axa cu deflecția mai mare
    if abs(dx) >= abs(dy):
        return LEFT if x < DEAD_LOW else RIGHT
    else:
        return FORWARD if y < DEAD_LOW else BACKWARD


def handle_button():
    """Verifică butonul cu debounce. Comută proiectorul LED."""
    global last_button_time, light_on

    now = time.ticks_ms()
    btn = button.value()
    if btn == 0 and time.ticks_diff(now, last_button_time) > DEBOUNCE_TIME:
        print("BUTTON pressed (raw={})".format(btn))
        last_button_time = now
        light_on = not light_on
        send_command("ledon" if light_on else "ledoff")


def main():
    global prev_direction, last_command_time

    connect_wifi()

    while True:
        if not wlan.isconnected():
            led.value(0)
            connect_wifi()

        now = time.ticks_ms()

        # --- Joystick ---
        direction = read_direction()

        if direction != prev_direction:
            print("DIRECTION change: {} -> {}".format(prev_direction, direction))
            send_command(direction)
            prev_direction = direction
            last_command_time = now
        elif direction != STOP and time.ticks_diff(now, last_command_time) > REPEAT_INTERVAL:
            print("DIRECTION repeat: {}".format(direction))
            send_command(direction)
            last_command_time = now

        # --- Buton ---
        handle_button()

        time.sleep_ms(LOOP_INTERVAL)


main()
```

!!! warning "Limitări actuale"
    Firmware-ul robotului folosește o viteză fixă (`speed = 150` din 255) și suportă doar 4 direcții. Pentru control proporțional sau mișcare diagonală ar trebui modificat firmware-ul robotului și adăugat un endpoint `/speed?val=N`.

## Idei de extindere

- Afișaj OLED cu starea conexiunii și nivelul bateriei.
- Al doilea joystick pentru pan/tilt al camerei (folosind `/control?var=...&val=...`).
- Buton suplimentar pentru capturi cu `GET /capture`.
- Control proporțional al vitezei după modificarea firmware-ului robotului.

---

## Surse originale

- Kit LAFVIN — [ESP32 Camera 4WD Robot Car Kit (arhivă Dropbox)](https://www.dropbox.com/scl/fo/9wcw8blqgkdy5iwn5y3qe/ABYUCXjqT0jWxQ0rco5Hch4?rlkey=gxunwfluft4dystlj1y9rx745&st=vznahh15&dl=0)
