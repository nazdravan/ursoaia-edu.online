---
title: ESP32
overview: true
tags: [ESP32, IoT, MicroPython, Wi-Fi]
summary: Proiecte ESP32 cu MicroPython — Wi-Fi, senzori, servere web și prototipuri IoT.
---

# Proiecte ESP32

ESP32 este un microcontroller cu **Wi-Fi și Bluetooth integrate**, ideal pentru proiecte IoT, automatizări și mici servere web. Rulează nativ MicroPython — sintaxa Python se aplică direct, fără compilare.

## Proiecte disponibile

### [LED intermitent](led_blink.md)

„Hello World" al sistemelor integrate — aprinde și stinge LED-ul integrat (GPIO 2) cu MicroPython. Include și un exemplu **LED chaser** pe pini consecutivi.

- **Componente:** ESP32, LED extern (opțional), rezistență 220 Ω
- **Concepte:** GPIO, ciclu de viață al unui script MicroPython
- **Dificultate:** începător

---

### [LED RGB](rgb_led.md)

Comandă un LED RGB cu trei canale **PWM** pe ESP32 — fade lin între roșu, verde și albastru, plus exemple pentru culoare fixă și aleatoare. Cod MicroPython.

- **Componente:** ESP32, LED RGB catod comun, 3× rezistență 220 Ω
- **Concepte:** PWM 10 biți, `duty()`, amestec aditiv de culori
- **Dificultate:** începător

---

### [Servomotor](servo.md)

Rotește un **servo SG90** la unghi precis între 0° și 180° folosind PWM la 50 Hz. Include baleiere lentă, calibrare manuală a capetelor și sfaturi de alimentare pentru a evita reset-uri.

- **Componente:** ESP32, servo SG90, alimentare 5 V (Vin sau sursă externă)
- **Concepte:** PWM 50 Hz, mapare unghi → duty, calibrare mecanică
- **Dificultate:** începător-mediu

---

### [Joystick](joystick.md)

Citește un joystick analogic pe **ADC1** (GPIO 34, 35) plus butonul de click — și transformă cele două axe în direcție (stânga / dreapta / sus / jos) cu zonă moartă. Include și mapare proporțională −100…+100 pentru jocuri.

- **Componente:** ESP32, modul joystick KY-023, fire jumper
- **Concepte:** ADC 12 biți, atenuare, zonă moartă, ADC1 vs ADC2 cu Wi-Fi
- **Dificultate:** începător-mediu

---

### [Senzor ultrasonic](ultrasonic.md)

Măsoară distanța până la obiecte cu **HC-SR04** — un puls de 10 µs pe Trig, cronometrarea ecoului pe Echo, calcul în cm. Include divizor de tensiune obligatoriu pentru ESP32 (3,3 V), filtru median și alarmă de proximitate.

- **Componente:** ESP32, HC-SR04 (sau HC-SR04P), rezistențe 1 kΩ + 2 kΩ
- **Concepte:** `time_pulse_us`, 5 V vs 3,3 V, divizor de tensiune, median filter
- **Dificultate:** începător-mediu

---

### [Senzor de sunet](sound_sensor.md)

Detectează sunete cu un modul **KY-038** (microfon electret + LM393) — citește atât nivelul analogic (AO), cât și ieșirea digitală cu prag reglabil (DO). Exemple: bătaia din palme aprinde un LED, plus comutare „clap-clap".

- **Componente:** ESP32, modul KY-038, fire jumper
- **Concepte:** comparator LM393, ADC vs digital input, calibrare prag, debounce sonor
- **Dificultate:** începător-mediu

---

### [Temperatură și umiditate](temperature.md)

Citește un senzor **DHT22** (sau DHT11) și afișează valorile pe consola serială la fiecare 2 secunde.

- **Componente:** ESP32, DHT22/DHT11, rezistență pull-up 10 kΩ
- **Concepte:** comunicare 1-wire, manipulare excepții, formatarea outputului
- **Dificultate:** începător-mediu

---

### [Server web pentru temperatură](temperature_web.md)

Combină Wi-Fi-ul ESP32 cu senzorul DHT22 — servește o **pagină HTML stilizată** cu citirile live, accesibilă din browser-ul oricărui dispozitiv din aceeași rețea.

- **Componente:** ESP32, DHT22, conexiune Wi-Fi
- **Concepte:** socket TCP, HTTP de bază, format string-uri HTML
- **Dificultate:** mediu

---

### [Mesagerie ESP-NOW](esp_now.md)

Două plăci ESP32 schimbă mesaje **direct, fără router și fără internet**, prin protocolul ESP-NOW. Latență sub 10 ms, până la 250 de octeți pe pachet.

- **Componente:** 2× ESP32 (atât)
- **Concepte:** ESP-NOW peer-to-peer, MAC addressing, canale Wi-Fi, broadcast vs unicast
- **Dificultate:** mediu

---

### [Display OLED 128x64 I2C](oled_display.md)

Afișează text și grafică pe un display OLED SSD1306 cu MicroPython — întâi doar cu `machine.I2C` și `framebuf` din firmware, apoi cu driverul **ssd1306** din micropython-lib.

- **Componente:** ESP32, display OLED 0.96" 128x64 I2C
- **Concepte:** I2C, `framebuf`, buffer de ecran, `mip install`
- **Dificultate:** începător-mediu

---

## De ce ESP32?

| Caracteristică | Detaliu |
|----------------|---------|
| **CPU** | Dual-core 240 MHz (mult mai rapid decât Arduino Uno) |
| **Memorie** | 520 KB RAM, 4 MB Flash |
| **Wi-Fi** | 802.11 b/g/n integrat |
| **Bluetooth** | Classic + BLE |
| **Pini I/O** | 30+ GPIO, ADC, DAC, PWM |
| **Preț** | ~5–10 € per placă |

## Instrumente

- **[Thonny](https://thonny.org/)** — IDE recomandat pentru MicroPython (vine cu suport ESP32)
- **[esptool.py](https://github.com/espressif/esptool)** — flash firmware MicroPython pe ESP32
- **[MicroPython firmware](https://micropython.org/download/esp32/)** — descarcă varianta ESP32 generic

## De unde să începi

1. **Flashează MicroPython** pe ESP32 cu `esptool.py`
2. Conectează cu Thonny (selectează interpreter „MicroPython (ESP32)")
3. Rulează prima dată [LED intermitent](led_blink.md) pentru a verifica setup-ul
4. Continuă cu senzorul de temperatură, apoi serverul web

!!! tip "Vii din lumea Arduino?"
    Sintaxa e diferită — Python în loc de C++ — dar conceptele sunt identice (GPIO, sleep, interrupt, comunicare). Avantajul MicroPython e că **nu trebuie să compilezi** la fiecare modificare; codul rulează direct.

!!! note "Diferența dintre ESP32 și ESP8266"
    ESP8266 e mai vechi și mai limitat (doar Wi-Fi, mai puțin RAM). Pentru proiecte noi recomandăm ESP32.
