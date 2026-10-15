---
category: Arduino
tags: [Arduino, Buzzer, Sunet, PWM, Muzică]
summary: Cântă o gamă muzicală cu un buzzer pasiv — învață legătura dintre frecvență și notele muzicale.
image: assets/images/projects/arduino/starter_kit/preview-passive-buzzer.jpg
---

# Buzzer pasiv (melodii)

Buzzer-ul pasiv nu are oscilator propriu, așa că tu trebuie să-i generezi semnalul. Avantajul? Poți controla **frecvența** și astfel poți cânta note muzicale reale.

![Buzzer pasiv — frecvențe și note muzicale pe Arduino](../../../assets/images/projects/arduino/starter_kit/preview-passive-buzzer.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Buzzer pasiv (cu placă verde vizibilă) | 1 |
| Fire jumper F-M | 2 |

## Cum funcționează

Un buzzer pasiv este, în esență, un mic difuzor. Dacă îi trimiți un semnal dreptunghiular cu o anumită frecvență, membrana vibrează la acea frecvență și produce un ton audibil.

Frecvența este exprimată în **Hertz (Hz)** — câte oscilații pe secundă. Fiecare notă muzicală corespunde unei frecvențe specifice:

| Notă | Frecvență |
|------|-----------|
| Do (alto) | 523 Hz |
| Re | 587 Hz |
| Mi | 659 Hz |
| Fa | 698 Hz |
| Sol | 784 Hz |
| La | 880 Hz |
| Si | 988 Hz |
| Do (înalt) | 1047 Hz |

Arduino are o funcție specială, **`tone(pin, frecvență, durată)`**, care generează automat semnalul PWM necesar. **Nu folosi `analogWrite()`** pentru buzzer pasiv — frecvența ei este fixă (~500 Hz) și nu o poți schimba.

## Conectare

| Pin buzzer | Arduino |
|-----------|---------|
| `+` (pin roșu) | D8 |
| `−` (pin negru) | GND |

[[wokwi:buzzer]]

```board
    Arduino
     D8  ────── Buzzer pasiv (+)
     GND ────── Buzzer pasiv (−)
```

## Cod

```cpp
/*
 * Proiect 7 — Buzzer pasiv, gama muzicală
 * Cântă 8 note: Do Re Mi Fa Sol La Si Do
 */

int buzzerPin = 8;

// Frecvențele notelor (Hz)
int notes[] = {523, 587, 659, 698, 784, 880, 988, 1047};
int noteCount = 8;

void setup() {
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  for (int i = 0; i < noteCount; i++) {
    tone(buzzerPin, notes[i], 500); // cântă nota 500 ms
    delay(500);
  }
  noTone(buzzerPin); // oprește sunetul
  delay(1000);       // pauză 1 sec între repetări
}
```

## Ce să încerci

- Cântă **"La Mulți Ani"** — caută pe internet frecvențele notelor.
- Folosește biblioteca `<pitches.h>` (inclusă în kit) pentru a scrie `NOTE_C5` în loc de `523`.
- Combină cu **butoane** (Proiect 4) pentru a face un mini-pian.
- Ajustează durata notelor (`500` → `250`) pentru melodii mai rapide.

## Note

- Funcția `tone()` folosește **Timer2** pe Arduino Uno, care interferează cu PWM pe pinii 3 și 11.
- `noTone(pin)` oprește sunetul. Fără ea, ultimul ton continuă să sune.
- Frecvențele sub ~30 Hz sau peste ~5 kHz pot fi greu de auzit sau inaudibile.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
