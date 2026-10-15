---
category: Arduino
tags: [Arduino, Releu, Putere, Siguranță]
summary: Un modul releu permite Arduino să controleze aparate la 220V — becuri, motoare, ventilatoare — fără contact electric direct.
image: assets/images/projects/arduino/starter_kit/preview-relay.jpg
---

# Modul releu

Un releu este ca un "buton comandat" electromagnetic. Arduino nu poate porni direct un bec de 220 V, dar poate comanda un releu care, la rândul lui, închide circuitul de înaltă tensiune.

![Modul releu — Arduino UNO controlând aparate](../../../assets/images/projects/arduino/starter_kit/preview-relay.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul releu 5 V (1 canal) | 1 |
| Fire jumper F-M | 3 |
| Fire jumper M-M | 1 |

## Cum funcționează

În interiorul modulului există:

- O **bobină** care, alimentată la 5 V, creează un câmp magnetic.
- Un **contact metalic** care se mișcă sub acțiunea câmpului magnetic și închide circuitul de ieșire.

Modulul are **2 grupuri de pini**:

| Grup | Pini | Utilitate |
|------|------|-----------|
| Intrare (comandă) | `VCC`, `GND`, `IN` | Se conectează la Arduino |
| Ieșire (putere) | `NO`, `COM`, `NC` | Se conectează la aparatul controlat |

- **NO** = Normally Open (deschis în stare de repaus).
- **NC** = Normally Closed (închis în stare de repaus).
- **COM** = Common (punct comun).

### Specificații cheie
- Curent maxim: **10 A** (NO), 5 A (NC).
- Tensiune de comutare: **150 VAC / 24 VDC**.
- LED indicator de stare pe modul.

**Siguranță**: pentru începători, conectează doar un LED sau un mic bec la ieșirea releului. **NU lucra la 220 V fără supraveghere adultă.**

## Conectare

| Pin modul | Arduino |
|-----------|---------|
| VCC | 5V |
| GND | GND |
| IN | D8 |

[[wokwi:relay]]

```board
    Arduino          Modul Releu
     5V   ───────── VCC
     GND  ───────── GND
     D8   ───────── IN

    Ieșire releu:
     COM ── aparat ── sursă (ex: bec + baterie 9V)
     NO  ── celălalt fir al aparatului
```

## Cod

```cpp
/*
 * Proiect 11 — Modul releu
 * Pornește și oprește releul la fiecare 2 secunde.
 */

int relayPin = 8;

void setup() {
  pinMode(relayPin, OUTPUT);
}

void loop() {
  digitalWrite(relayPin, HIGH); // Activează releul (clic!)
  delay(2000);
  digitalWrite(relayPin, LOW);  // Dezactivează releul
  delay(2000);
}
```

## Ce să încerci

- Controlează un **ventilator mic** sau o **mini-lampă de birou** cu baterie.
- Aprinde releul când senzorul ultrasonic (Proiect 10) detectează cineva aproape.
- Folosește-l ca timer: pornește aparatul pentru o perioadă fixă.
- Combină cu **IR-ul** (Proiect 12) pentru o telecomandă rudimentară.

## Note

- Vei auzi un "clic" caracteristic la fiecare comutare — acesta este sunetul bobinei.
- Unele module au logica **inversată** (`LOW` = activ). Verifică LED-ul indicator.
- **Nu depăși** specificațiile: 10 A la 150 V. Peste acestea, contactele se ard.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
