---
category: Arduino
tags: [Arduino, LED, RGB, PWM, Culoare]
summary: Folosește PWM pentru a amesteca roșu, verde și albastru într-un LED RGB și a genera orice culoare.
image: assets/images/projects/arduino/starter_kit/preview-rgb-led.jpg
---

# LED RGB

Un **LED RGB** are trei LED-uri (roșu, verde, albastru) împachetate într-o singură carcasă. Controlând intensitatea fiecărei culori în parte, poți genera aproape orice culoare din spectrul vizibil.

![LED RGB — Arduino UNO cu LED multicolor](../../../assets/images/projects/arduino/starter_kit/preview-rgb-led.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Breadboard 830 puncte | 1 |
| LED RGB (catod comun) | 1 |
| Rezistență 220 Ω | 3 |
| Fire jumper M-M | 4 |

## Cum funcționează

Un LED RGB are **4 picioare**:

- 3 anozi (+): roșu, verde, albastru — câte unul pentru fiecare culoare.
- 1 catod (−) comun — cel mai lung picior, se conectează la GND.

Fiecare anod are nevoie de **propria rezistență de 220 Ω** pentru limitarea curentului.

### PWM — Pulse Width Modulation

Pentru a controla **intensitatea** fiecărui LED, nu putem folosi doar `HIGH` și `LOW`. În schimb, folosim **PWM** (Modulare prin lățimea impulsului): Arduino generează un semnal care comută foarte rapid între `HIGH` și `LOW`, iar ochiul nostru percepe media ca intensitate luminoasă.

Funcția `analogWrite(pin, valoare)` acceptă valori între `0` (stins) și `255` (aprins la maxim). Pinii care suportă PWM pe Uno sunt marcați cu `~`: **3, 5, 6, 9, 10, 11**.

Amestecând `(R, G, B)`:
- `(255, 0, 0)` → roșu pur
- `(0, 255, 0)` → verde pur
- `(255, 255, 0)` → galben
- `(255, 255, 255)` → alb

## Conectare

| Pin LED RGB | Arduino |
|-------------|---------|
| R (roșu)    | D6 (prin 220 Ω) |
| Catod comun (−) | GND |
| G (verde)   | D5 (prin 220 Ω) |
| B (albastru)| D3 (prin 220 Ω) |

[[wokwi:rgb-led]]

```board
    Arduino            LED RGB (catod comun)
     D6 ──[220Ω]──── R
     D5 ──[220Ω]──── G
     D3 ──[220Ω]──── B
    GND ─────────── Catod (−, piciorul cel mai lung)
```

## Cod

```cpp
/*
 * Proiect 3 — LED RGB cu fade între culori
 */

#define BLUE  3
#define GREEN 5
#define RED   6

int redValue, greenValue, blueValue;
int delayTime = 10;

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  // De la roșu la verde
  redValue = 255; greenValue = 0; blueValue = 0;
  for (int i = 0; i < 255; i++) {
    redValue--;
    greenValue++;
    analogWrite(RED, redValue);
    analogWrite(GREEN, greenValue);
    delay(delayTime);
  }

  // De la verde la albastru
  redValue = 0; greenValue = 255; blueValue = 0;
  for (int i = 0; i < 255; i++) {
    greenValue--;
    blueValue++;
    analogWrite(GREEN, greenValue);
    analogWrite(BLUE, blueValue);
    delay(delayTime);
  }

  // De la albastru la roșu
  redValue = 0; greenValue = 0; blueValue = 255;
  for (int i = 0; i < 255; i++) {
    blueValue--;
    redValue++;
    analogWrite(BLUE, blueValue);
    analogWrite(RED, redValue);
    delay(delayTime);
  }
}
```

## Ce să încerci

- Afișează o singură culoare fixă (ex: mov `(128, 0, 255)`).
- Adaugă o funcție `setColor(r, g, b)` ca să scurtezi codul.
- Combină cu un **joystick** (Proiect 9) pentru a schimba culorile manual.
- Pentru LED cu **anod comun**, inversează logica: `analogWrite(RED, 255 - r)`.

## Note

- Verifică ce tip de LED ai: **catod comun** (cel mai lung pin la GND) sau **anod comun** (cel mai lung pin la 5V).
- Folosește doar pini cu `~` (PWM) — altfel `analogWrite` nu va funcționa.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
