---
category: Arduino
tags: [Arduino, Senzor, Înclinare, Digital Input]
summary: Detectează înclinarea folosind un senzor cu bilă — un întrerupător mecanic simplu care se închide când este răsturnat.
image: assets/images/projects/arduino/starter_kit/preview-tilt-ball-switch.jpg
---

# Senzor cu bilă (înclinare)

Senzorul cu bilă este cea mai simplă formă de detector de orientare — practic, un întrerupător care se închide sau se deschide în funcție de poziția fizică a senzorului.

![Senzor cu bilă — Arduino UNO cu detector de înclinare](../../../assets/images/projects/arduino/starter_kit/preview-tilt-ball-switch.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Senzor cu bilă (tilt ball switch) | 1 |
| Fire jumper F-M | 2 |

## Cum funcționează

Înăuntrul senzorului se află o **bilă metalică** liberă și două contacte conductoare. Când senzorul este orientat într-un anumit unghi, bila cade peste contacte și închide circuitul; când este răsturnat, bila se rostogolește și circuitul se deschide.

Este **mai puțin precis** decât un accelerometru, dar foarte ieftin, fără consum electric propriu și foarte ușor de utilizat. Este folosit în jucării, alarme și detectoare simple de mișcare.

Electric, îl conectezi exact ca pe un buton:
- Un pin la `D2` (cu `INPUT_PULLUP`).
- Celălalt pin la `GND`.

Când bila închide contactul → pinul citește `LOW`. Când circuitul este deschis → pinul citește `HIGH` (grație pull-up-ului intern).

În acest proiect vom folosi **LED-ul integrat** (pinul 13) ca indicator: se aprinde când senzorul este înclinat.

## Conectare

| Pin senzor | Arduino |
|-----------|---------|
| Un picior | D2 |
| Alt picior | GND |

[[wokwi:tilt-ball-switch]]

```board
    Arduino
     D2 ──── Senzor bilă ──── GND
     D13 (LED integrat, folosit ca indicator)
```

## Cod

```cpp
/*
 * Proiect 5 — Senzor cu bilă (tilt)
 * Când senzorul este înclinat, LED-ul integrat se aprinde.
 */

int tiltPin = 2;
int ledPin = 13;
int tiltState = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(tiltPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  tiltState = digitalRead(tiltPin);

  if (tiltState == LOW) {           // circuit închis (bila conectează)
    digitalWrite(ledPin, HIGH);
    Serial.println("Inclinat!");
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(100);
}
```

## Ce să încerci

- Adaugă un **buzzer** (Proiect 6) care să sune ca alarmă.
- Numără de câte ori a fost înclinat senzorul (pe front — nu constant).
- Folosește ca sistem "anti-furt" pentru o cutie.
- Combină cu un LED RGB: verde = vertical, roșu = înclinat.

## Note

- Bila este liberă înăuntru — scutură ușor senzorul și îl vei auzi.
- Răspunsul poate fi "zgomotos" (bila sare) — adaugă un mic **debounce** software.
- Orientează senzorul astfel încât poziția "normală" să fie cu circuitul deschis.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
