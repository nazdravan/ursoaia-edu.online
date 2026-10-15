---
category: Arduino
tags: [Arduino, Keypad, Tastatură, Matrix, Input]
summary: Conectează o tastatură 4x4 cu membrană și citește caracterul apăsat folosind biblioteca Keypad.
image: assets/images/projects/arduino/starter_kit/preview-membrane-switch.jpg
---

# Tastatură cu membrană

Tastaturile matriciale sunt peste tot: telefoane, microunde, lacăte electronice, bancomate. Învață cum se conectează la Arduino — e mai elegant decât 16 butoane separate.

![Tastatură cu membrană — Arduino UNO citește tastatura matricială](../../../assets/images/projects/arduino/starter_kit/preview-membrane-switch.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Tastatură cu membrană 4×4 | 1 |
| Fire jumper M-M | 8 |

## Cum funcționează

Tastatura 4×4 are **16 taste** (0–9, A–D, `*`, `#`), dar doar **8 pini** de ieșire. Cum?

Folosește o schemă **matricială**:
- 4 rânduri × 4 coloane formează o grilă.
- Fiecare tastă este o intersecție între un rând și o coloană.
- Când apeși o tastă, se conectează acel rând cu acea coloană.

### Scanarea matricei

Arduino "scanează" tastatura foarte rapid:
1. Pune un rând la `LOW`, restul la `HIGH`.
2. Citește cele 4 coloane.
3. Dacă o coloană este `LOW`, tasta de la intersecție a fost apăsată.
4. Repetă pentru celelalte 3 rânduri.

**Biblioteca `Keypad.h`** face tot acest lucru automat — tu doar întrebi "ce tastă a fost apăsată?".

## Conectare

Privind tastatura de sus, cu cablul ieșind spre tine, pinii sunt de la stânga la dreapta `P1..P8`:

| Pin tastatură | Arduino | Funcție |
|-----------|---------|---------|
| P1 | D9 | Rând 1 |
| P2 | D8 | Rând 2 |
| P3 | D7 | Rând 3 |
| P4 | D6 | Rând 4 |
| P5 | D5 | Coloană 1 |
| P6 | D4 | Coloană 2 |
| P7 | D3 | Coloană 3 |
| P8 | D2 | Coloană 4 |

[[wokwi:membrane-switch]]

## Cod

```cpp
/*
 * Proiect 13 — Tastatură cu membrană 4x4
 * Afișează caracterul apăsat în Serial Monitor.
 * Bibliotecă necesară: Keypad
 */

#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    Serial.print("Tasta apasata: ");
    Serial.println(key);
  }
}
```

## Ce să încerci

- Construiește un **lacăt electronic** — o parolă de 4 cifre deblochează un LED verde.
- Folosește tastele pentru a introduce un număr și afișează-l pe **LCD** (Proiect 14).
- Calculator simplu: două numere și o operație.
- Pornește sunete diferite pentru fiecare tastă (Proiect 7).

## Note

- Instalează biblioteca **`Keypad`** din Library Manager (de obicei de Mark Stanley).
- Dacă tastele apar greșit, ai inversat pinii de rânduri/coloane.
- Funcția `getKey()` este **non-blocantă** — returnează `0` (NO_KEY) dacă nu este nimic apăsat.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
