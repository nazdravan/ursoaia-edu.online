---
category: Arduino
tags: [Arduino, Sunet, Microfon, Senzor, Analog]
summary: Detectează sunete (bătăi din palme, voci) cu un microfon electret și senzor dedicat — ieșire analogică sau digitală.
image: assets/images/projects/arduino/starter_kit/preview-sound-sensor.jpg
---

# Senzor de sunet

Ultimul proiect al kit-ului! Detectează sunete din mediu — perfect pentru alarme controlate prin voce, aprinsul la bătaie din palme sau vizualizatoare audio.

![Senzor de sunet — Arduino UNO detectând sunete cu microfon](../../../assets/images/projects/arduino/starter_kit/preview-sound-sensor.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul senzor de sunet (cu microfon electret) | 1 |
| Fire jumper F-M | 4 |

## Cum funcționează

### Microfonul electret

Pe modul există un microfon **electret condensator** — un mic dispozitiv cu două plăci paralele, una fixă și una mobilă (diafragma). Când sunetul lovește diafragma, aceasta vibrează, schimbând capacitatea între plăci. Circuitul de amplificare de pe modul transformă aceste variații într-un semnal electric proporțional cu intensitatea sunetului.

### Două ieșiri

Modulul are **două ieșiri**:

- **AO** (Analog Out) — tensiune analogică în timp real, reflectă forma de undă a sunetului (~0–5 V).
- **DO** (Digital Out) — `HIGH` sau `LOW` în funcție de un prag reglabil prin potențiometrul albastru de pe modul.

Pentru **detecție simplă** (ex: alarmă la sunet puternic) → folosește **DO**.
Pentru **analiză a nivelului** (ex: VU-meter) → folosește **AO**.

### Reglarea sensibilității

Potențiometrul albastru de pe modul reglează pragul pentru DO. **Are nevoie de minim 10 rotații complete** ca să ai vreun efect — este un potențiometru de precizie.

## Conectare

| Pin modul | Arduino |
|-----------|---------|
| VCC | 5V |
| GND | GND |
| AO (analog) | A0 |
| DO (digital) | D7 |

[[wokwi:sound-sensor]]

```board
    Arduino              Senzor sunet
     5V   ──────────── VCC
     GND  ──────────── GND
     A0   ──────────── AO
     D7   ──────────── DO
```

## Cod

```cpp
/*
 * Proiect 25 — Senzor de sunet
 * Afișează valoarea analogică și starea digitală.
 */

int analogPin = A0;
int digitalPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(digitalPin, INPUT);
}

void loop() {
  int soundLevel = analogRead(analogPin);
  int threshold = digitalRead(digitalPin);

  Serial.print("Analog: ");
  Serial.print(soundLevel);
  Serial.print("  Digital: ");
  Serial.println(threshold == HIGH ? "LINISTE" : "ZGOMOT");

  delay(50);
}
```

## Ce să încerci

- **Aprinde un LED la bătaia din palme** — când `soundLevel` depășește un prag.
- Construiește un **VU-meter**: bara de 8 LED-uri (Proiect 16) reflectă intensitatea sunetului.
- Pornește/oprește o lampă prin **releu** (Proiect 11) la o bătaie din palme.
- Combină cu un **LCD** (Proiect 14) pentru a afișa nivelul în dB.

## Note

- Microfonul este **sensibil la poziție** — îndreaptă-l spre sursa sonoră.
- Dacă LED-ul pragului (al doilea LED de pe modul) rămâne aprins constant, rotește potențiometrul până se stinge în liniște.
- Pentru analiză spectrală (frecvențe), ai nevoie de biblioteci precum **`arduinoFFT`** — mai avansat.
- Microfonul detectează și sunete prea slabe pentru urechea umană — perfect pentru detecție de vibrații.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)

**Felicitări!** Ai terminat toate cele 25 de proiecte din Super Starter Kit. Acum poți combina cunoștințele acumulate în proiecte proprii.
