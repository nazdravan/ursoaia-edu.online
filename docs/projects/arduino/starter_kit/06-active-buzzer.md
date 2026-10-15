---
category: Arduino
tags: [Arduino, Buzzer, Sunet, Digital Output]
summary: Generează primul sunet cu un buzzer activ — e nevoie doar să îi dai tensiune, oscilatorul intern face restul.
image: assets/images/projects/arduino/starter_kit/preview-active-buzzer.jpg
---

# Buzzer activ

Este momentul să faci Arduino să emită primul sunet. Buzzer-ul activ este cel mai simplu generator de sunete — îi dai tensiune și sună singur.

![Buzzer activ — Arduino UNO emite sunet](../../../assets/images/projects/arduino/starter_kit/preview-active-buzzer.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Buzzer activ (carcasă neagră, cu bandă adezivă deasupra) | 1 |
| Fire jumper F-M | 2 |

## Cum funcționează

Există două tipuri de buzzere:

- **Buzzer activ** — are un **oscilator încorporat**. Când îi aplici 5 V, sună singur la o frecvență fixă (≈ 2 kHz).
- **Buzzer pasiv** — nu are oscilator. Trebuie să îi trimiți un semnal PWM cu o frecvență anume (Proiect 7).

Cum îi distingi?
- **Activul** are carcasa **neagră** și deseori o **etichetă adezivă** deasupra.
- **Pasivul** are fața **deschisă** și se vede placa verde.

Activul are și **polaritate**:
- Pin lung / marcat `+` → la pinul digital (sau 5 V).
- Pin scurt → la GND.

În acest proiect, pur și simplu alternăm `HIGH`/`LOW` pe pinul 8 pentru a porni și opri sunetul — ca un **bip** intermitent.

## Conectare

| Pin buzzer | Arduino |
|-----------|---------|
| `+` (pin lung) | D8 |
| `−` (pin scurt) | GND |

[[wokwi:buzzer]]

```board
    Arduino
     D8  ────── Buzzer (+) 
     GND ────── Buzzer (−)
```

## Cod

```cpp
/*
 * Proiect 6 — Buzzer activ
 * Emite un bip la fiecare secundă.
 */

int buzzerPin = 8;

void setup() {
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  digitalWrite(buzzerPin, HIGH);  // Pornește sunetul
  delay(500);
  digitalWrite(buzzerPin, LOW);   // Oprește sunetul
  delay(500);
}
```

## Ce să încerci

- Fă un cod Morse "SOS": trei scurte, trei lungi, trei scurte.
- Combină cu un **buton** (Proiect 4): buzzer-ul sună doar când este apăsat.
- Combină cu **senzorul cu bilă** (Proiect 5) pentru o alarmă anti-înclinare.
- Schimbă durata bip-urilor pentru a crea ritmuri diferite.

## Note

- Dacă buzzer-ul nu sună, **întoarce-l** — pinii pot fi inversați.
- Este posibil ca buzzer-ul activ să fie puțin cam tare; poți adăuga o rezistență de 100 Ω în serie pentru a reduce volumul.
- Nu aștepta de la el melodii — pentru asta folosește buzzer-ul pasiv.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
