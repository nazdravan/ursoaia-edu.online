---
category: Arduino
tags: [Arduino, Ultrasonic, HC-SR04, Distanță, Senzor]
summary: Măsoară distanța până la obiecte cu HC-SR04 — senzor ultrasonic care folosește ecoul sunetului la 40 kHz.
image: assets/images/projects/arduino/starter_kit/preview-ultrasonic-sensor.jpg
---

# Senzor ultrasonic (distanță)

HC-SR04 este un senzor foarte popular: îl folosești ca să afli cât de departe este un obiect, fără contact. Este prezent în roboți care ocolesc obstacole și în sisteme de parcare.

![Senzor ultrasonic HC-SR04 — Arduino UNO măsoară distanța](../../../assets/images/projects/arduino/starter_kit/preview-ultrasonic-sensor.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul ultrasonic HC-SR04 | 1 |
| Fire jumper F-M | 4 |

## Cum funcționează

Senzorul are 4 pini: `VCC`, `Trig`, `Echo`, `GND`.

**Principiul** este identic cu cel al liliecilor și delfinilor:

1. Arduino trimite un impuls `HIGH` de **10 microsecunde** pe pinul `Trig`.
2. Senzorul emite 8 cicluri de ultrasunet la **40 kHz** (inaudibil pentru om).
3. Când ultrasunetul lovește un obstacol, se întoarce ca ecou.
4. Pinul `Echo` rămâne în `HIGH` exact cât durează această călătorie dus-întors.
5. Noi măsurăm acest timp cu funcția `pulseIn()`.

### Calculul distanței

Sunetul se propagă cu ~**340 m/s** = 0.034 cm/μs. Pentru că timpul măsurat este dus-întors, împărțim la 2:

```
distanță [cm] = timp [μs] × 0.034 / 2
```

Sau, echivalent: `timp / 58`.

**Domeniu de măsurare:** 2 cm – 400 cm, cu precizie ~3 mm.

## Conectare

| Pin senzor | Arduino |
|-----------|---------|
| VCC | 5V |
| GND | GND |
| Trig | D10 |
| Echo | D9 |

[[wokwi:ultrasonic-sensor]]

```board
    Arduino              HC-SR04
     5V   ──────────  VCC
     GND  ──────────  GND
     D10  ──────────  Trig
     D9   ──────────  Echo
```

## Cod

```cpp
/*
 * Proiect 10 — Senzor ultrasonic HC-SR04
 * Afișează distanța în cm pe Serial Monitor.
 */

int trigPin = 10;
int echoPin = 9;
long duration;
float distance;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Trimite un impuls de 10μs pe Trig
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Măsoară durata impulsului pe Echo (μs)
  duration = pulseIn(echoPin, HIGH);

  // Calculăm distanța în cm
  distance = duration * 0.0343 / 2;

  Serial.print("Distanta = ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(200);
}
```

## Ce să încerci

- Aprinde un **LED** când distanța scade sub 10 cm.
- Un sistem de **parcare** cu buzzer care bipăie mai rapid pe măsură ce te apropii.
- Un **radar** care rotește senzorul cu un servo (Proiect 8).
- Afișează distanța pe un **LCD** (Proiect 14).

## Note

- Nu îndrepta senzorul spre **materiale moi** (haine, burete) — absorb sunetul și dau citiri greșite.
- Obiectele mai mici de 2 cm pot fi invizibile pentru senzor.
- Lasă **60 ms** între măsurători pentru a evita interferența între ecouri.
- Poți folosi biblioteca `<HC-SR04.h>` inclusă în kit, dar codul de mai sus merge și fără ea.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
