---
category: ESP32
tags: [OLED, SSD1306, I2C, Display, MicroPython]
summary: Afișează text și grafică pe un display OLED 128x64 I2C cu ESP32 și MicroPython — întâi doar cu modulele din firmware, apoi cu driverul ssd1306.
---

# Display OLED 128x64 I2C

Conectăm un display OLED de 0.96" (controler SSD1306) la un ESP32 prin I2C și îl programăm în MicroPython, în două feluri. În **varianta 1** folosim doar modulele care vin deja în firmware — `machine.I2C` și `framebuf` — și trimitem singuri comenzile către display. În **varianta 2** instalăm driverul **ssd1306** din micropython-lib, care face același lucru într-un singur rând.

!!! tip "Ai un Arduino?"
    Același proiect, în C++: [Display OLED pe Arduino](../arduino/oled_display.md).

## Descriere

Ecranul are 128 × 64 = 8192 de pixeli. Fiecare pixel e un bit, deci toată imaginea ocupă **1024 de octeți**. Cele 64 de rânduri sunt împărțite în **8 pagini** a câte 8 rânduri; un octet trimis la display aprinde o **coloană verticală de 8 pixeli** în pagina curentă (bitul 0 sus, bitul 7 jos).

```board
          coloana 0   1   2  ...  127
         ┌───┬───┬───┬─────┬───┐
pagina 0 │   │   │   │     │   │  rândurile 0–7
pagina 1 │   │   │   │     │   │  rândurile 8–15
  ...    │   │   │   │     │   │
pagina 7 │   │   │   │     │   │  rândurile 56–63
         └───┴───┴───┴─────┴───┘
```

Fiecare transmisie I2C începe cu un **octet de control**: `0x00` — „urmează o comandă”, `0x40` — „urmează date (pixeli)”. Adresa display-ului este de obicei **`0x3C`**.

Spre deosebire de Arduino Nano (2 KB RAM), ESP32 are 520 KB de RAM, deci putem ține liniștiți o copie a întregului ecran în memorie și s-o trimitem dintr-o dată.

## Materiale

| Componentă                    | Cantitate | Note                             |
|-------------------------------|-----------|----------------------------------|
| ESP32 DevKit V1               | 1         | Cu firmware MicroPython          |
| Display OLED 0.96" 128x64 I2C | 1         | Controler SSD1306, 4 pini        |
| Fire jumper                   | 4         | M-F, sau M-M cu breadboard       |

## Conectare

```board
Pin OLED  →  ESP32
--------     -----
GND       →  GND
VCC       →  3V3
SCL       →  GPIO 22
SDA       →  GPIO 21
```

GPIO 22 (SCL) și GPIO 21 (SDA) sunt pinii I2C obișnuiți ai lui ESP32. Modulul OLED merge și la 3,3 V, și la 5 V; alimentându-l de la 3V3, nivelurile logice pe SDA/SCL rămân sigure pentru ESP32.

### Schema de conectare

[[wokwi:esp32-oled]]

## Varianta 1: doar modulele din firmware

`machine.I2C` vorbește cu display-ul, iar `framebuf` desenează în memorie text, linii și dreptunghiuri. Formatul `framebuf.MONO_VLSB` înseamnă „un octet = 8 pixeli verticali, bitul 0 sus” — exact cum își organizează SSD1306 memoria. De aceea bufferul se poate trimite la display așa cum e, fără nicio conversie.

```python
# Display OLED 128x64 I2C (SSD1306) pe ESP32 — doar machine.I2C și framebuf
# Conectare: VCC -> 3V3, GND -> GND, SCL -> GPIO 22, SDA -> GPIO 21
from machine import Pin, I2C
import framebuf

ADDR = 0x3C

INIT = (
    0xAE,        # display OFF
    0xD5, 0x80,  # frecvența ceasului
    0xA8, 0x3F,  # multiplex = 64 rânduri
    0xD3, 0x00,  # fără offset
    0x40,        # linia de start 0
    0x8D, 0x14,  # pornește charge pump (obligatoriu!)
    0x20, 0x00,  # adresare orizontală
    0xA1, 0xC8,  # orientare (oglindire X/Y)
    0xDA, 0x12,  # configurare pini COM
    0x81, 0xCF,  # contrast
    0xD9, 0xF1,  # pre-charge
    0xDB, 0x40,  # VCOMH
    0xA4,        # afișează conținutul RAM
    0xA6,        # normal (nu inversat)
    0xAF,        # display ON
)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
print("Dispozitive I2C:", [hex(a) for a in i2c.scan()])  # trebuie să apară 0x3c


def cmd(c):
    i2c.writeto(ADDR, bytes((0x00, c)))  # 0x00 = „urmează o comandă”


def show(buf):
    for c in (0x21, 0, 127, 0x22, 0, 7):  # toate coloanele, toate paginile
        cmd(c)
    i2c.writevto(ADDR, (b"\x40", buf))    # 0x40 = „urmează date”, apoi 1024 octeți


for c in INIT:
    cmd(c)

buf = bytearray(128 * 64 // 8)  # 1024 octeți = tot ecranul
fb = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_VLSB)

fb.fill(0)
fb.text("Salut!", 0, 0)
fb.text("Cerc de", 0, 16)
fb.text("informatica", 0, 26)
fb.rect(0, 44, 128, 20, 1)
fb.text("ESP32 2025", 24, 50)
show(buf)
```

Fontul din `framebuf` are 8×8 pixeli, deci pe un rând încap **16 caractere**, iar pe ecran — **8 rânduri**. Fiecare modificare apare pe ecran abia după `show(buf)`.

!!! note "De ce `writevto`?"
    `writevto` trimite mai multe bucăți una după alta, într-o singură transmisie I2C: întâi octetul de control `0x40`, apoi bufferul. Așa nu mai e nevoie să lipim cei 1024 de octeți la `b"\x40"` și să creăm o copie nouă la fiecare cadru.

## Varianta 2: driverul ssd1306

Driverul `ssd1306` din micropython-lib conține exact codul din varianta 1, împachetat într-o clasă. Clasa moștenește `framebuf.FrameBuffer`, deci are aceleași funcții de desenare, plus `show()`.

### Instalarea driverului

- **Thonny:** **Tools → Manage packages…**, caută `ssd1306`, apasă **Install**.
- **mpremote** (placa conectată prin USB):

```bash
mpremote mip install ssd1306
```

### Cod

```python
# Display OLED 128x64 I2C (SSD1306) pe ESP32 cu driverul ssd1306 din micropython-lib
# Conectare: VCC -> 3V3, GND -> GND, SCL -> GPIO 22, SDA -> GPIO 21
# Instalare driver: mpremote mip install ssd1306  (sau Thonny -> Manage packages)
from machine import Pin, I2C
from time import sleep
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
print("Dispozitive I2C:", [hex(a) for a in i2c.scan()])  # trebuie să apară 0x3c

oled = ssd1306.SSD1306_I2C(128, 64, i2c)


def demo_text():
    oled.fill(0)
    oled.text("Cerc de", 0, 0)
    oled.text("informatica", 0, 10)
    oled.text("Salut, ESP32!", 0, 30)
    oled.text("2025", 0, 50)
    oled.show()


def demo_shapes():
    oled.fill(0)
    oled.rect(0, 0, 40, 30, 1)            # dreptunghi
    oled.fill_rect(45, 0, 40, 30, 1)      # dreptunghi plin
    oled.ellipse(108, 15, 14, 14, 1)      # cerc (MicroPython 1.20+)
    oled.line(0, 63, 127, 34, 1)          # linie
    oled.show()


def demo_counter():
    for i in range(0, 101, 5):
        oled.fill(0)
        oled.text("Incarcare...", 0, 0)
        oled.text("{:3d}%".format(i), 48, 24)
        oled.rect(0, 52, 128, 12, 1)                  # contur bară
        oled.fill_rect(2, 54, i * 124 // 100, 8, 1)   # bara
        oled.show()
        sleep(0.1)


while True:
    demo_text()
    sleep(2)
    demo_shapes()
    sleep(2)
    demo_counter()
    sleep(1)
```

### Funcțiile de bază

| Funcție                          | Ce face                                        |
|----------------------------------|------------------------------------------------|
| `fill(c)`                        | umple tot ecranul (`0` = negru, `1` = alb)     |
| `text(s, x, y, c=1)`             | text cu font 8×8, de la pixelul `(x, y)`       |
| `pixel(x, y, c)`                 | un pixel                                       |
| `line(x0, y0, x1, y1, c)`        | linie                                          |
| `rect` / `fill_rect(x, y, w, h, c)` | dreptunghi / dreptunghi plin                |
| `ellipse(x, y, rx, ry, c, f)`    | elipsă sau cerc; `f=True` = plin (MicroPython 1.20+) |
| `scroll(dx, dy)`                 | mută tot conținutul cu `dx`, `dy` pixeli       |
| `invert(1)`                      | inversează culorile pe ecran                   |
| `contrast(0..255)`               | luminozitatea                                  |
| `show()`                         | trimite bufferul pe ecran                      |

## Probleme frecvente

| Simptom                                        | Cauza / soluția                                                  |
|------------------------------------------------|------------------------------------------------------------------|
| `i2c.scan()` întoarce `[]`                     | Verifică firele; SDA și SCL inversate e greșeala cea mai des întâlnită |
| `OSError: [Errno 19] ENODEV`                   | Display-ul nu răspunde la `0x3C` — vezi ce adresă arată `i2c.scan()` (poate `0x3d`) și folosește-o |
| `ImportError: no module named 'ssd1306'`       | Driverul nu e instalat pe placă (vezi „Instalarea driverului”)   |
| `AttributeError: ... 'ellipse'`                | Firmware MicroPython mai vechi de 1.20 — actualizează-l sau folosește doar `rect`/`line` |
| Pixeli aleatori, imagine deplasată cu 2 px     | Display-ul are controler **SH1106** (de obicei cele de 1.3"), nu SSD1306 — e nevoie de un driver `sh1106` |

## Exerciții

1. Afișează temperatura și umiditatea de la [senzorul DHT22](temperature.md) în loc de text fix.
2. Fă un ceas: afișează `time.ticks_ms() // 1000` (secundele de la pornire), actualizat în fiecare secundă.
3. O minge care sare de pereții ecranului (variabile `x`, `y`, `dx`, `dy`).
4. Desenează graficul funcției `math.sin` pe toată lățimea ecranului.
5. Folosește `oled.scroll(0, -8)` ca să faci un „terminal” în care fiecare rând nou împinge textul în sus.

---

## Referințe

- [Random Nerd Tutorials — MicroPython: OLED Display with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/)
- [Documentația MicroPython — `framebuf`](https://docs.micropython.org/en/latest/library/framebuf.html)
- [Driverul ssd1306 în micropython-lib](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306)
- [Fișa tehnică SSD1306 (PDF)](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
