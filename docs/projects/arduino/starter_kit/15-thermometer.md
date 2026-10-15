---
category: Arduino
tags: [Arduino, Termistor, Temperatură, LCD, Analog]
summary: Măsoară temperatura ambientală cu un termistor NTC și afișează-o pe LCD — primul senzor analogic de mediu.
image: assets/images/projects/arduino/starter_kit/preview-thermometer.jpg
---

# Termometru cu termistor

Construiește un termometru digital care afișează temperatura în timp real pe ecranul LCD. Folosești un **termistor** — o rezistență a cărei valoare scade cu temperatura.

![Termometru — Arduino UNO citind temperatura cu termistor](../../../assets/images/projects/arduino/starter_kit/preview-thermometer.jpg)

## Componente necesare

| Componentă | Cantitate |
|------------|-----------|
| Arduino Uno R3 | 1 |
| Modul LCD1602 I2C | 1 |
| Termistor NTC 10 kΩ | 1 |
| Rezistență 10 kΩ | 1 |
| Breadboard 830 puncte | 1 |
| Fire jumper M-M | 5 |
| Fire jumper M-F | 4 |

## Cum funcționează

### Termistor

Un **termistor** (thermal resistor) este o rezistență care își schimbă valoarea în funcție de temperatură. Există două tipuri:

- **NTC** (Negative Temperature Coefficient) — rezistența scade când temperatura crește. Folosit ca senzor de temperatură.
- **PTC** (Positive Temperature Coefficient) — rezistența crește cu temperatura. Folosit ca siguranță resetabilă.

Termistorul din kit este **NTC 10 kΩ la 25 °C**.

### Divizor de tensiune

Arduino citește tensiuni, nu rezistențe. Ca să transformăm rezistența în tensiune, folosim un **divizor de tensiune**:

```
    5V ──[termistor]──┬──[10 kΩ]── GND
                      │
                      └── A0 (Arduino)
```

Când temperatura crește → rezistența termistorului scade → mai mult curent → tensiunea pe A0 crește. Citim cu `analogRead()` și aplicăm **ecuația Steinhart-Hart** pentru a obține temperatura în Kelvin, apoi o convertim în Celsius.

## Conectare

| Componentă | Arduino |
|-----------|---------|
| LCD I2C VCC | 5V |
| LCD I2C GND | GND |
| LCD I2C SDA | A4 |
| LCD I2C SCL | A5 |
| Termistor (picior 1) | 5V |
| Termistor (picior 2) | A0 + rezistență 10 kΩ la GND |

[[wokwi:thermometer]]

## Cod

```cpp
/*
 * Proiect 15 — Termometru cu termistor și LCD I2C
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <math.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
int tempPin = A0;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
}

void loop() {
  int tempReading = analogRead(tempPin);

  // Ecuația Steinhart-Hart pentru NTC 10kΩ
  double tempK = log(10000.0 * ((1024.0 / tempReading - 1)));
  tempK = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 *
          tempK * tempK)) * tempK);
  float tempC = tempK - 273.15;
  float tempF = (tempC * 9.0) / 5.0 + 32.0;

  lcd.setCursor(0, 0);
  lcd.print("Temp:           ");
  lcd.setCursor(6, 0);
  lcd.print(tempC, 1);
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("       ");
  lcd.setCursor(6, 1);
  lcd.print(tempF, 1);
  lcd.print(" F");

  Serial.print("C = "); Serial.print(tempC);
  Serial.print("  F = "); Serial.println(tempF);

  delay(500);
}
```

## Ce să încerci

- **Alarmă de temperatură**: dacă depășește 30 °C, aprinde un LED roșu sau un buzzer.
- Afișează **min/max** — valorile extreme din ultimele minute.
- Construiește un mic **termostat**: la <20 °C pornește un releu (Proiect 11) către un ventilator.
- Înregistrează datele pe Serial Monitor și desenează un grafic în Excel.

## Note

- Atinge termistorul cu degetul — vei vedea temperatura urcând rapid.
- Scrie o linie întreagă de spații când actualizezi ecranul — altfel cifrele vechi rămân pe el.
- Dacă valorile par eronate, verifică **rezistența** (exact 10 kΩ, maro-negru-portocaliu).
- Pentru precizie mai mare, poți calibra scrierea fixă cu un termometru de referință.

---

**Vezi și:** [Toate proiectele kit-ului](kits.md)
