---
title: Arduino
overview: true
tags: [Arduino, electronică, microcontroller, C++]
summary: Proiecte Arduino cu scheme, cod și liste de componente — de la primul LED la cuburi multiplexate și kit-uri starter.
---

# Proiecte Arduino

Plăcile Arduino sunt punctul de intrare perfect în electronică. Cu un limbaj C/C++ simplificat și un IDE prietenos, sunt ideale pentru primele proiecte hardware. Toate proiectele de aici vin cu scheme complete, cod sursă și listă de materiale.

## Proiecte disponibile

### [Cub de LED-uri 3x3x3](led_cube.md)

Construiește un cub cu 27 de LED-uri controlate prin **multiplexare pe straturi** și animații POV. Folosește 9 coloane direct conectate la pini și 3 straturi controlate prin tranzistoare NPN.

- **Componente:** Arduino Uno, 27× LED, rezistențe, tranzistoare 2N2222, breadboard
- **Concepte:** multiplexare, POV (persistența vederii), control GPIO
- **Dificultate:** mediu

---

### [Display OLED 128x64 I2C](oled_display.md)

Afișează text și grafică pe un display OLED SSD1306 — întâi **fără nicio bibliotecă**, trimițând singur comenzile prin I2C, apoi cu **Adafruit SSD1306** (text în mai multe mărimi, forme, animații).

- **Componente:** Arduino Nano sau Uno, display OLED 0.96" 128x64 I2C
- **Concepte:** I2C, pagini de memorie, font bitmap, `PROGMEM`, buffer de ecran
- **Dificultate:** începător-mediu

---

### [Kit-uri de pornire Arduino](starter_kit/kits.md)

Cele **25 de proiecte** din Super Starter Kit pentru Arduino UNO (CH340) — de la „Hello World" până la motoare pas cu pas controlate prin telecomandă. Fiecare proiect are descriere, schemă și cod gata de încărcat.

- **Pentru cine:** începători absoluți și intermediari
- **Componente:** kit complet LA036
- **Concepte:** GPIO, PWM, I2C, ADC, comunicare serială, senzori, actuatori

---

## Resurse

- [Site oficial Arduino](https://www.arduino.cc/)
- [Arduino IDE — descărcare](https://www.arduino.cc/en/software)
- [Reference Arduino limbaj](https://www.arduino.cc/reference/en/)
- [Tinkercad Circuits](https://www.tinkercad.com/circuits) — simulator online gratuit

## De unde să începi

Dacă ești complet începător:

1. Instalează **Arduino IDE** și conectează placa
2. Începe cu [Hello World](starter_kit/01-hello-world.md) din Starter Kit
3. Continuă cu LED-uri, butoane, senzori — în ordinea proiectelor din kit
4. La final, încearcă [Cub-ul de LED-uri 3x3x3](led_cube.md) ca proiect-mai-complex

!!! tip "Programezi în C++ pentru prima oară?"
    Arduino folosește un dialect simplificat de C/C++. Funcțiile cheie sunt `setup()` (rulează o dată la pornire) și `loop()` (rulează în buclă infinită). Restul îl înveți pe parcurs din proiecte.
