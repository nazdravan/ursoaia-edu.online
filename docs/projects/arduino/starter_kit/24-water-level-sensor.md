---
category: Arduino
tags: [Arduino, Apă, Senzor, Analog, Nivel]
summary: Detectează prezența și nivelul apei cu un senzor cu piste conductoare — util pentru alarme de inundație sau udare automată.
image: assets/images/projects/arduino/starter_kit/preview-water-level-sensor.jpg
---

# Senzor nivel apă

Acest senzor este extrem de util: detectează dacă apa atinge anumite linii pe placa lui și cât de mult este apă. Este perfect pentru **alarme anti-inundație**, **ghivece auto-udate** sau **detectoare de ploaie**.

![Senzor nivel apă — Arduino UNO citind un container cu apă](../../../assets/images/projects/arduino/starter_kit/preview-water-level-sensor.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul senzor nivel apă | 1 |
| Fire jumper F-M | 3 |

## Cum funcționează

### Principiul

Pe placa senzorului există **două seturi de piste paralele** intercalate:
- Un set este conectat la **GND**.
- Celălalt set la pinul **S** (semnal), cu o rezistență internă de **1 MΩ** spre VCC (pull-up).

În stare uscată, nu există continuitate între piste → pinul S este `HIGH` (pull-up).

Când apa atinge pistele, ea conduce electricitatea (slab, dar suficient) și **scurtcircuitează** pistele cu GND. Cu cât **mai multe piste** sunt acoperite, cu atât tensiunea pe S scade mai mult.

Arduino citește tensiunea pe pinul analog (A0) cu `analogRead()`:
- **Uscat** → valoare mare (aproape de 1023).
- **Udat complet** → valoare mică (aproape de 0).

### Specificații
- Tensiune de lucru: **5 V**
- Curent: < 20 mA
- Zonă de detecție: **40 × 16 mm**
- Ieșire: semnal **analogic** (0–4.2 V)

## Conectare

| Pin senzor | Arduino |
|-----------|---------|
| `+` (VCC) | 5V |
| `−` (GND) | GND |
| S (signal) | A0 |

[[wokwi:water-level-sensor]]

```board
    Arduino              Senzor apă
     5V   ──────────── +
     GND  ──────────── −
     A0   ──────────── S
```

## Cod

```cpp
/*
 * Proiect 24 — Senzor nivel apă
 * Afișează valoarea analogică pe Serial Monitor.
 */

int waterPin = A0;
int value = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  value = analogRead(waterPin);

  Serial.print("Nivel apa: ");
  Serial.print(value);

  if (value < 100) {
    Serial.println("  [USCAT]");
  } else if (value < 400) {
    Serial.println("  [Putin]");
  } else if (value < 700) {
    Serial.println("  [Mediu]");
  } else {
    Serial.println("  [MULT!]");
  }

  delay(500);
}
```

## Ce să încerci

- Aprinde un **LED roșu** când apa depășește un prag — alarmă de inundație.
- Pornește un **buzzer** (Proiect 6) la apariția apei.
- Construiește un **ghiveci auto-udat**: când senzorul e uscat, pornește o pompă prin releu (Proiect 11).
- Afișează nivelul pe un **LCD** (Proiect 14) cu o bară grafică.

## Note

- **Nu scufunda** complet senzorul — doar partea cu piste trebuie să atingă apa. Conectorul trebuie să rămână uscat.
- Citirile sunt influențate de **mineralitatea apei** (apa pură nu conduce bine). Calibrează senzorul cu apa pe care o vei folosi.
- **Piste corodate** în timp din cauza electrolizei. Alimentează senzorul doar când citești (printr-un pin digital), apoi oprește-l.
- Valorile se stabilizează după ~1 secundă.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
