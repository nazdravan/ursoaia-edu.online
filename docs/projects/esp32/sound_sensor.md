---
category: ESP32
tags: [Sunet, Microfon, Senzor, ADC, MicroPython]
summary: Detectează sunete cu un microfon electret pe ESP32 — ieșire analogică pentru nivel, ieșire digitală pentru alarmă peste un prag reglabil.
image: assets/images/projects/esp32/preview-sound-sensor.jpg
---

# Senzor de sunet

Modulul de sunet KY-038 (sau similar, bazat pe LM393) îți permite să „auzi" mediul cu ESP32: nivel continuu pe ieșirea analogică, plus un comparator digital care declanșează când sunetul depășește un prag reglabil. Ideal pentru alarme la bătaia din palme, sisteme „clap-on", VU-meter sau pornire la voce.

![Modul senzor de sunet conectat la ESP32](../../assets/images/projects/esp32/preview-sound-sensor.jpg)

## Descriere

Pe modul găsești un **microfon electret condensator** — o capsulă mică cu o diafragmă care vibrează la presiunea sunetului. Un cip **LM393** comparator amplifică semnalul și îl compară cu un prag setat de potențiometrul de pe placă.

Modulul scoate **două semnale**:

- **AO** (Analog Out) — tensiune proporțională cu intensitatea sunetului în timp real. Util pentru VU-metere, înregistrare de nivel, declanșare proporțională.
- **DO** (Digital Out) — `0` când sunetul depășește pragul, `1` în liniște (active LOW). Util pentru detecție on/off de tip alarmă.

!!! tip "Două LED-uri pe modul"
    LED-ul roșu numit **PWR** confirmă alimentarea. Al doilea LED, marcat de obicei **L1** sau **DO**, se aprinde când DO trece în LOW (sunet detectat). Folosește-l ca să calibrezi pragul: rotește potențiometrul până se stinge când nu vorbește nimeni.

## Componente

| Component | Cantitate |
|-----------|-----------|
| Placă ESP32 (DevKit V1) | 1 |
| Modul senzor de sunet (KY-038 sau similar, cu LM393) | 1 |
| Fire jumper F-M | 4 |

## Conectare

| Pin modul | ESP32 | Note |
|-----------|-------|------|
| VCC (sau +) | 3.3V | la 3,3 V e perfect, fără probleme de tensiune pe ESP32 |
| GND (sau −) | GND | masă comună |
| AO | GPIO 34 | ieșire analogică, ADC1 |
| DO | GPIO 35 | ieșire digitală, citită ca input |

[[wokwi:esp32-sound-sensor]]

```board
    ESP32                Senzor sunet
    3.3V ──────────── VCC
    GND ───────────── GND
    GPIO 34 ◄────────── AO  (analog)
    GPIO 35 ◄────────── DO  (digital)
```

!!! warning "Alimentare la 3,3 V, nu 5 V"
    Multe module sunt marcate „5 V" dar funcționează fără probleme la 3,3 V. Asta e important pentru ESP32: pinii lui **nu sunt 5 V tolerant**, iar dacă alimentezi senzorul la 5 V, AO și DO pot ajunge la 5 V → risc pentru GPIO. La 3,3 V, ieșirile rămân în plaja sigură.

!!! note "Pini de input"
    GPIO **34** și **35** sunt **doar input** pe ESP32 — perfect pentru a citi semnale, nu le poți comuta ca ieșire. Sunt și pe ADC1, deci funcționează corect chiar și când Wi-Fi e activ (ADC2 nu funcționează în paralel cu Wi-Fi).

## Cod

```python
from machine import Pin, ADC
import time

# --- Configurare ---

ao = ADC(Pin(34))
ao.atten(ADC.ATTN_11DB)          # plaja completă 0-3,3 V

do = Pin(35, Pin.IN)             # ieșire digitală a modulului

# Prag software pentru AO (0-4095). Calibrează în liniștea camerei tale.
ANALOG_THRESHOLD = 2500


def read_sound():
    """Returnează (nivel_analogic, zgomot_detectat)."""
    level = ao.read()
    # DO e active LOW: 0 = sunet peste pragul potențiometrului
    digital_noise = (do.value() == 0)
    return level, digital_noise


print("Senzor de sunet activ. Ctrl+C pentru oprire.\n")

while True:
    try:
        level, noisy = read_sound()
        analog_noise = level > ANALOG_THRESHOLD

        flag = ""
        if noisy or analog_noise:
            flag = "  [ZGOMOT]"

        print(f"AO = {level:4d}   DO = {'LOW (sunet)' if noisy else 'HIGH (liniște)'}{flag}")
        time.sleep_ms(50)
    except KeyboardInterrupt:
        print("\nStop.")
        break
```

## Rulează scriptul

1. Asamblează circuitul: VCC la 3,3V, GND la GND, AO la GPIO 34, DO la GPIO 35.
2. În Thonny, lipește codul și apasă **Run** (F5).
3. Bate o singură dată din palme — în consolă vei vedea ceva de tipul:

```
AO =  812   DO = HIGH (liniște)
AO =  834   DO = HIGH (liniște)
AO = 3902   DO = LOW (sunet)  [ZGOMOT]
AO = 4061   DO = LOW (sunet)  [ZGOMOT]
AO = 1284   DO = HIGH (liniște)
```

## Calibrare

### Pragul digital (potențiometrul de pe modul)

Rotește **potențiometrul albastru** pe modul cu o șurubelniță mică:

1. Lasă liniște în cameră.
2. Privește LED-ul al doilea (`DO` / `L1`). În liniște trebuie să fie **stins**.
3. Dacă e aprins, rotește potențiometrul (de obicei minim 10 ture de precizie) până se stinge.
4. Testează cu o bătaie din palme: LED-ul ar trebui să clipească la sunet.

### Pragul analogic (software)

Citește valorile AO în liniștea ta de fundal și setează `ANALOG_THRESHOLD` la `valoare_repaus + 1500`. Exemplu rapid:

```python
# Mediază 50 de citiri când e liniște
samples = [ao.read() for _ in range(50)]
baseline = sum(samples) // len(samples)
print("Liniște:", baseline)
ANALOG_THRESHOLD = baseline + 1500
```

## Exemplu: aprinde LED-ul la bătaia din palme

LED-ul integrat (GPIO 2) se aprinde pentru 1 secundă la fiecare sunet detectat:

```python
from machine import Pin, ADC
import time

ao = ADC(Pin(34)); ao.atten(ADC.ATTN_11DB)
do = Pin(35, Pin.IN)
led = Pin(2, Pin.OUT)

led_off_at = 0

while True:
    if do.value() == 0:                      # sunet detectat
        led.value(1)
        led_off_at = time.ticks_add(time.ticks_ms(), 1000)

    if led.value() == 1 and time.ticks_diff(led_off_at, time.ticks_ms()) <= 0:
        led.value(0)

    time.sleep_ms(20)
```

## Exemplu: clap-clap (două bătăi consecutive)

Pornește/oprește LED-ul doar la **două bătăi** într-un interval scurt — clasicul „clap-clap" pentru lampă:

```python
from machine import Pin
import time

do = Pin(35, Pin.IN)
led = Pin(2, Pin.OUT)

last_clap = 0
state = False

while True:
    if do.value() == 0:                      # sunet detectat
        now = time.ticks_ms()
        if 100 < time.ticks_diff(now, last_clap) < 800:
            state = not state                # două bătăi în 0,1-0,8 s
            led.value(state)
        last_clap = now
        time.sleep_ms(200)                   # debounce — ignoră ecouri
    time.sleep_ms(10)
```

`100 < dt < 800` filtrează atât „ecouri" foarte apropiate (sub 100 ms — același sunet declanșând de două ori) cât și pauze prea lungi (peste 800 ms — bătăi necorelate).

## Probleme frecvente

??? question "Senzorul declanșează tot timpul, fără sunet"
    - Pragul potențiometrului e prea scăzut. Rotește-l (în liniște) până LED-ul `DO` se stinge.
    - Microfonul prinde un zgomot constant — frigider, computer, climatizare. Mută senzorul.
    - Vibrațiile mesei se transmit prin firele rigide. Pune modulul pe burete sau ceva moale.

??? question "Senzorul nu reacționează deloc"
    - Verifică alimentarea: LED-ul `PWR` trebuie să fie aprins.
    - Pragul e prea sus — rotește potențiometrul invers.
    - Sunetul nu ajunge la microfon — îndreaptă diafragma spre sursă.
    - Microfonul electret e direcțional; nu îl pune cu fața spre masă.

??? question "AO oscilează între 0 și 4095 chiar și în liniște"
    - Cablu prea lung sau zgomotos. Folosește fire scurte (sub 20 cm).
    - Modulul e prea aproape de antena Wi-Fi a ESP32 — distanțează-l 5-10 cm.
    - Mediază mai multe citiri pentru a stabiliza valoarea:
      ```python
      level = sum(ao.read() for _ in range(8)) // 8
      ```

??? question "Vreau să măsor decibeli, nu doar nivel"
    - Modulele KY-038 nu sunt calibrate pentru dB. Pentru SPL real ai nevoie de module dedicate (ex. **MAX9814** cu AGC) sau un microfon **I2S** (INMP441, SPH0645) cu prelucrare FFT — semnificativ mai complex.

## Idei de extindere

- **Pornește un servo** (vezi [Servomotor](servo.md)) la bătaia din palme — capac care se deschide la sunet.
- **Comandă culoarea unui LED RGB** (vezi [LED RGB](rgb_led.md)) după nivelul sunetului în timp real — verde liniște, roșu zgomot.
- **Server web** cu nivel de sunet live: extinde proiectul [Server web pentru temperatură](temperature_web.md) și înlocuiește citirea DHT22 cu citirea AO.
- **Detecție de bătăi pe distanță:** trimite evenimentele cu [ESP-NOW](esp_now.md) către o placă-master care numără bătăi din mai multe camere.

---

## Referințe

- [MicroPython — `machine.ADC` reference](https://docs.micropython.org/en/latest/library/machine.ADC.html)
- [LM393 datasheet (Texas Instruments)](https://www.ti.com/product/LM393)
- [Random Nerd Tutorials — ESP32 Sound Sensor](https://randomnerdtutorials.com/esp32-microphone-sensor-arduino-ide/)
