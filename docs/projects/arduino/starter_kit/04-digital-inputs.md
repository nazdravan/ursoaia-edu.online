---
category: Arduino
tags: [Arduino, Buton, Digital Input, Pull-up]
summary: Folosește două butoane pentru a aprinde și stinge un LED — primul contact cu intrările digitale și rezistențele de pull-up.
image: assets/images/projects/arduino/starter_kit/preview-digital-inputs.jpg
---

# Intrări digitale (butoane)

În proiectele anterioare ai trimis semnale **de la** Arduino către lume. Acum învățăm inversul: cum să **citim** o stare — apăsarea unui buton.

![Intrări digitale — butoane controlând LED-uri](../../../assets/images/projects/arduino/starter_kit/preview-digital-inputs.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Breadboard 830 puncte | 1 |
| LED roșu 5 mm | 1 |
| Rezistență 220 Ω | 1 |
| Buton tactil (push-button) | 2 |
| Fire jumper M-M | 7 |

## Cum funcționează

Un **buton tactil** este un întrerupător: când îl apeși, închide două contacte și lasă curentul să treacă.

### Problema: pinul "flotant"

Dacă un pin digital nu e conectat la nimic, valoarea pe care o citește este aleatorie — zgomotul electric îl face să oscileze între `HIGH` și `LOW`. Trebuie să "fixăm" starea inactivă a pinului la o valoare cunoscută.

### Soluția: rezistența de pull-up internă

Arduino are **rezistențe de pull-up interne** de ~20 kΩ care pot fi activate software. Setăm pinul astfel:

```cpp
pinMode(buttonPin, INPUT_PULLUP);
```

Acum, în starea inactivă, pinul va citi `HIGH`. Când apeși butonul, îl conectezi la `GND`, iar pinul citește `LOW`.

**Logica este inversată**: `LOW` = apăsat, `HIGH` = liber.

### Schema proiectului

- **Butonul A** aprinde LED-ul.
- **Butonul B** îl stinge.

## Conectare

| Componentă | Arduino |
|-----------|---------|
| LED anod (+) | D9 prin 220 Ω |
| LED catod (−) | GND |
| Buton A (un picior) | D2 |
| Buton A (celălalt picior) | GND |
| Buton B (un picior) | D3 |
| Buton B (celălalt picior) | GND |

[[wokwi:digital-inputs]]

```board
     D9 ──[220Ω]──── Anod LED ── Catod ── GND
     D2 ─────────── Buton A ─── GND
     D3 ─────────── Buton B ─── GND
```

## Cod

```cpp
/*
 * Proiect 4 — Intrări digitale cu două butoane
 */

int ledPin = 9;
int buttonApin = 2;
int buttonBpin = 3;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);  // pull-up intern activ
  pinMode(buttonBpin, INPUT_PULLUP);
}

void loop() {
  // Butonul A apăsat → LED aprins
  if (digitalRead(buttonApin) == LOW) {
    digitalWrite(ledPin, HIGH);
  }
  // Butonul B apăsat → LED stins
  if (digitalRead(buttonBpin) == LOW) {
    digitalWrite(ledPin, LOW);
  }
}
```

## Ce să încerci

- Folosește un singur buton pentru a comuta (toggle) LED-ul la fiecare apăsare.
- Adaugă **debounce**: după o apăsare, ignoră schimbările timp de 50 ms.
- Folosește un buton ca să variezi frecvența de clipire a LED-ului.
- Combină cu un **buzzer** (Proiect 6) pentru a emite un sunet când apeși.

## Note

- Butoanele au **4 picioare** dar doar **2 conexiuni electrice** — pinii A-D și B-C sunt legați între ei intern.
- Așază corect butonul pe breadboard: picioarele sunt pe laturile opuse.
- Dacă folosești `INPUT` simplu (fără `PULLUP`), vei avea nevoie de o rezistență externă de 10 kΩ.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
