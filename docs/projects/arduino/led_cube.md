---
category: Arduino
tags: [LED, Cub, Multiplexare, Arduino Uno]
summary: Construiește un cub cu 27 de LED-uri folosind multiplexarea pe straturi și animații POV pe Arduino Uno.
image: assets/images/projects/arduino/3x3x3_led_cube.jpg
featured: true
---

# Cub de LED-uri 3x3x3

O versiune simplificată a proiectului [8x8x8 LED Cube](https://www.instructables.com/8x8x8-Arduino-LED-Cube/), adaptată pentru începători.

![Cub de LED-uri 3x3x3 asamblat](../../assets/images/projects/arduino/3x3x3_led_cube.jpg)

## Cum funcționează

Cubul folosește **multiplexarea pe straturi**:

- **9 coloane** (anozii LED-urilor) sunt conectate la pinii digitali ai Arduino prin rezistențe de 220 Ω.
- **3 straturi** (catozii LED-urilor) sunt controlate prin tranzistoare NPN (2N2222 / BC547).
- Arduino comută rapid între straturi (POV — persistența vederii), creând iluzia că toate cele 27 de LED-uri sunt aprinse simultan.

```board
     Vedere de sus (numerotarea coloanelor):

         C0   C1   C2
         C3   C4   C5
         C6   C7   C8

     Straturi (vedere laterală):
         Stratul 2 (sus)
         Stratul 1 (mijloc)
         Stratul 0 (jos)
```

## Listă de materiale

| Componentă                 | Cantitate | Note                              |
|----------------------------|-----------|-----------------------------------|
| Arduino Uno (CH340)        | 1         | Sau Nano                          |
| LED 5mm (orice culoare)    | 27        | Poți folosi 3 culori, câte 9      |
| Rezistență 220 Ω           | 9         | Limitare curent (coloane)         |
| Rezistență 1 kΩ            | 3         | Baze tranzistoare (straturi)      |
| Tranzistor NPN 2N2222      | 3         | Sau BC547/BC337                   |
| Breadboard                 | 1         | 830 puncte de conexiune           |
| Fire jumper                | ~20       | M-M                               |

> Toate componentele sunt incluse în **Kit-ul Super Starter LA036 pentru Arduino UNO**.

## Schema de conectare

[[wokwi:led-cube]]
```board
                        Arduino Uno
                     ┌──────────────────┐
                     │                  │
    Coloane          │  D2  ──[220Ω]──── C0 (anod LED)
    (anozi)          │  D3  ──[220Ω]──── C1
                     │  D4  ──[220Ω]──── C2
                     │  D5  ──[220Ω]──── C3
                     │  D6  ──[220Ω]──── C4
                     │  D7  ──[220Ω]──── C5
                     │  D8  ──[220Ω]──── C6
                     │  D9  ──[220Ω]──── C7
                     │  D10 ──[220Ω]──── C8
                     │                  │
    Straturi         │  D11 ──[1kΩ]──┐  │
    (catozi           │  D12 ──[1kΩ]──┤  │
     prin              │  D13 ──[1kΩ]──┤  │
     tranzistoare)   │                │  │
                     │  GND ──────────┘  │
                     └──────────────────┘

    Tranzistor 2N2222 (pentru fiecare strat):

        Pin Arduino ──[1kΩ]──► Bază
                               Colector ◄── Catozi strat (toate cele 9 LED-uri)
                               Emitor ──► GND
```

### Atribuire pini

| Pin Arduino | Funcție               |
|-------------|-----------------------|
| D2          | Coloana 0 (anod)      |
| D3          | Coloana 1             |
| D4          | Coloana 2             |
| D5          | Coloana 3             |
| D6          | Coloana 4             |
| D7          | Coloana 5             |
| D8          | Coloana 6             |
| D9          | Coloana 7             |
| D10         | Coloana 8             |
| D11         | Stratul 0 (jos)       |
| D12         | Stratul 1 (mijloc)    |
| D13         | Stratul 2 (sus)       |
| GND         | Emitoare tranzistoare |

## Construirea cubului

### 1. Pregătirea LED-urilor

- Testează fiecare LED înainte de lipire (cu o rezistență de 220 Ω la 5V).
- Identifică polaritatea: piciorul lung = anod (+), piciorul scurt = catod (−).
- Îndoaie catodul (−) al fiecărui LED la 90° — vor fi conectați orizontal pentru a forma un strat.

### 2. Realizarea unui șablon

- Desenează o grilă 3×3 pe carton sau placaj cu ~20 mm spațiu între centre.
- Găurește 9 orificii cu diametrul de 5 mm.

### 3. Lipirea straturilor

- Inserează 9 LED-uri în șablon.
- Lipește toți catozi (−) într-o grilă orizontală folosind fir de cupru.
- Repetă pentru toate cele 3 straturi. Testează fiecare strat!

### 4. Conectarea coloanelor

- Plasează stratul de jos pe breadboard.
- Lipește stratul din mijloc deasupra, conectând anozii (+) vertical.
- Lipește stratul de sus.
- Folosește distanțieri de înălțime egală între straturi (~20 mm).

### 5. Conectarea la Arduino

- 9 anozi (coloane) → prin rezistențe de 220 Ω → pinii D2–D10.
- 3 straturi catod → prin tranzistoare 2N2222 → pinii D11–D13.

## Cod

```cpp
/*
 * Cub de LED-uri 3x3x3 — Arduino Uno
 */

// === Configurare pini ===
const byte COL_PINS[9] = {2, 3, 4, 5, 6, 7, 8, 9, 10};
const byte LAYER_PINS[3] = {11, 12, 13};

#define NUM_LAYERS  3
#define NUM_COLS    9

uint16_t cube[NUM_LAYERS];
#define POV_DELAY 3

void displayCube() {
  for (byte layer = 0; layer < NUM_LAYERS; layer++) {
    for (byte l = 0; l < NUM_LAYERS; l++) digitalWrite(LAYER_PINS[l], LOW);
    for (byte col = 0; col < NUM_COLS; col++) digitalWrite(COL_PINS[col], (cube[layer] >> col) & 1);
    digitalWrite(LAYER_PINS[layer], HIGH);
    delay(POV_DELAY);
  }
  for (byte l = 0; l < NUM_LAYERS; l++) digitalWrite(LAYER_PINS[l], LOW);
}

void showFor(unsigned long duration) {
  unsigned long start = millis();
  while (millis() - start < duration) displayCube();
}

void clearCube() {
  for (byte i = 0; i < NUM_LAYERS; i++) cube[i] = 0;
}

void fillCube() {
  for (byte i = 0; i < NUM_LAYERS; i++) cube[i] = 0b111111111;
}

void setLed(byte x, byte y, byte z, bool state) {
  byte col = y * 3 + x;
  if (state) cube[z] |= (1 << col);
  else cube[z] &= ~(1 << col);
}

// Animațiile sunt omise pentru scurtarea acestui fragment,
// dar poți adăuga propriile tale!
// Vezi codul complet pentru detalii.

void setup() {
  for (byte i = 0; i < NUM_COLS; i++) {
    pinMode(COL_PINS[i], OUTPUT);
    digitalWrite(COL_PINS[i], LOW);
  }
  for (byte i = 0; i < NUM_LAYERS; i++) {
    pinMode(LAYER_PINS[i], OUTPUT);
    digitalWrite(LAYER_PINS[i], LOW);
  }
  randomSeed(analogRead(A0));
  clearCube();
}

void loop() {
  fillCube();
  showFor(1000);
  clearCube();
  showFor(500);
}
```

## Referințe

- [Proiectul original 8x8x8](https://www.instructables.com/8x8x8-Arduino-LED-Cube/)
- [Forum Arduino: Cub simplu 3x3x3](https://forum.arduino.cc/t/very-simple-3x3x3-cube-sketch/922655)
- [Instructables: Cub LED 3x3x3 Arduino UNO](https://www.instructables.com/3x3x3-LED-Cube-Arduino-UNO/)
