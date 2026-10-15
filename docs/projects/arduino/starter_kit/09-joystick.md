---
category: Arduino
tags: [Arduino, Joystick, Analog, Potențiometru, Input]
summary: Citește axele X și Y ale unui joystick analogic și folosește butonul de click — input pe două axe cu o singură componentă.
image: assets/images/projects/arduino/starter_kit/preview-joystick.jpg
---

# Joystick analogic

Un joystick analogic este, de fapt, două **potențiometre** — unul pentru axa X și unul pentru axa Y — plus un buton care se activează când apeși pe manșă.

![Joystick analogic — Arduino UNO citind axele X și Y](../../../assets/images/projects/arduino/starter_kit/preview-joystick.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul joystick analogic | 1 |
| Fire jumper F-M | 5 |

## Cum funcționează

Modulul are 5 pini: `GND`, `+5V`, `VRx`, `VRy`, `SW`.

- **VRx și VRy** sunt ieșiri analogice (tensiune între 0 V și 5 V).
- **SW** este un buton digital (apăsare pe manșă).

Arduino Uno are un **ADC pe 10 biți**, așa că `analogRead()` returnează valori între **0 și 1023**:

- Poziția de repaus (centru) → ~ 512 pe ambele axe.
- Extrema stângă/jos → 0.
- Extrema dreaptă/sus → 1023.

Pentru buton, folosim `INPUT_PULLUP` (ca la Proiectul 4) pentru că modulul nu are rezistență integrată.

## Conectare

| Pin modul | Arduino |
|-----------|---------|
| GND | GND |
| +5V | 5V |
| VRx | A0 |
| VRy | A1 |
| SW (buton) | D2 |

[[wokwi:joystick]]

```board
    Arduino             Joystick
     5V   ────────── +5V
     GND  ────────── GND
     A0   ────────── VRx  (axa X, analog)
     A1   ────────── VRy  (axa Y, analog)
     D2   ────────── SW   (buton, digital)
```

## Cod

```cpp
/*
 * Proiect 9 — Joystick analogic
 * Afișează în Serial valorile X, Y și starea butonului.
 */

int xPin = A0;
int yPin = A1;
int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  int xValue = analogRead(xPin);
  int yValue = analogRead(yPin);
  int btn = digitalRead(buttonPin);  // LOW = apăsat

  Serial.print("X = ");
  Serial.print(xValue);
  Serial.print("  Y = ");
  Serial.print(yValue);
  Serial.print("  Buton = ");
  Serial.println(btn == LOW ? "APASAT" : "liber");

  delay(200);
}
```

## Ce să încerci

- Controlează un **servo** (Proiect 8) cu axa X.
- Controlează **două LED-uri RGB** — unul cu X, altul cu Y.
- Detectează "comenzi": sus, jos, stânga, dreapta — pe baza unui prag.
- Controlează un cursor pe un **LCD** (Proiect 14).

## Note

- Valorile de repaus pot varia: e normal să fie între 490 și 530, nu exact 512.
- În general, butonul SW este **invers** (deschis = HIGH, apăsat = LOW).
- Pentru control continuu (jocuri), mapează valorile cu `map(val, 0, 1023, -100, 100)`.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
