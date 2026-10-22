---
category: Arduino
tags: [OLED, SSD1306, I2C, Display, Arduino Nano]
summary: Afișează text și grafică pe un display OLED 128x64 I2C cu Arduino — întâi fără nicio bibliotecă, apoi cu Adafruit SSD1306.
---

# Display OLED 128x64 I2C

Conectăm un display OLED de 0.96" (controler SSD1306) la un Arduino Nano prin I2C și îl programăm în două feluri. În **varianta 1** trimitem singuri comenzile către display, folosind doar `Wire.h` — așa vedem cum funcționează ecranul pe dinăuntru. În **varianta 2** folosim biblioteca **Adafruit SSD1306**, care ne dă text în mai multe mărimi, linii, cercuri și animații în câteva rânduri de cod.

!!! tip "Ai un ESP32?"
    Același proiect, în MicroPython: [Display OLED pe ESP32](../esp32/oled_display.md).

## Cum funcționează

Ecranul are 128 × 64 = 8192 de pixeli. Fiecare pixel e un bit (aprins sau stins), deci toată imaginea ocupă 8192 / 8 = **1024 de octeți**.

Cele 64 de rânduri sunt împărțite în **8 pagini** a câte 8 rânduri. Un octet trimis la display aprinde o **coloană verticală de 8 pixeli** în pagina curentă: bitul 0 e pixelul de sus, bitul 7 — cel de jos.

```board
          coloana 0   1   2  ...  127
         ┌───┬───┬───┬─────┬───┐
pagina 0 │   │   │   │     │   │  rândurile 0–7
pagina 1 │   │   │   │     │   │  rândurile 8–15
  ...    │   │   │   │     │   │
pagina 7 │   │   │   │     │   │  rândurile 56–63
         └───┴───┴───┴─────┴───┘
```

Fiecare transmisie I2C începe cu un **octet de control**: `0x00` înseamnă „urmează o comandă”, `0x40` — „urmează date (pixeli)”. Adresa I2C a display-ului este de obicei **`0x3C`**, mai rar `0x3D`.

## Listă de materiale

| Componentă                    | Cantitate | Note                                  |
|-------------------------------|-----------|---------------------------------------|
| Arduino Nano (sau Uno)        | 1         | Testat pe o clonă Nano cu CH340       |
| Display OLED 0.96" 128x64 I2C | 1         | Controler SSD1306, 4 pini             |
| Fire jumper                   | 4         | M-F, sau M-M cu breadboard            |
| Cablu USB                     | 1         | Mini-USB pentru Nano                  |

## Schema de conectare

[[wokwi:arduino-nano-oled]]

| Pin display | Arduino Nano / Uno | Arduino Mega |
|-------------|--------------------|--------------|
| GND         | GND                | GND          |
| VCC         | 5V                 | 5V           |
| SCL         | A5                 | 21           |
| SDA         | A4                 | 20           |

!!! warning "Ordinea pinilor diferă"
    La unele module primul pin e VCC, nu GND. Citește inscripțiile de pe placă, nu te baza pe poziție.

## Varianta 1: fără biblioteci

Folosim doar `Wire.h`, care vine deja cu Arduino IDE.

### Pasul 1. Trimiterea unei comenzi

```cpp
void cmd(uint8_t c) {
  Wire.beginTransmission(oledAddr);  // începem să vorbim cu display-ul
  Wire.write(0x00);                  // „urmează o comandă”
  Wire.write(c);                     // comanda propriu-zisă
  Wire.endTransmission();
}
```

### Pasul 2. Inițializarea

La pornire display-ul e stins. Îi trimitem o secvență de comenzi din fișa tehnică SSD1306. Cele mai importante:

- **`0x8D, 0x14`** — pornește „pompa de sarcină” care ridică tensiunea pentru OLED. Fără ea ecranul rămâne negru.
- **`0x20, 0x00`** — adresare orizontală: după coloana 127 cursorul trece singur pe pagina următoare.
- **`0xA1, 0xC8`** — orientarea. Dacă textul apare oglindit sau cu susul în jos, încearcă `0xA0` / `0xC0`.
- **`0xAF`** — aprinde ecranul.

### Pasul 3. Fontul

Display-ul nu știe ce e litera „A” — știe doar pixeli. Desenăm fiecare literă din **5 coloane** (5 octeți) înalte de 7 pixeli:

```board
          col0 col1 col2 col3 col4
           7E   11   11   11   7E
 bit 0     .    ■    ■    ■    .
 bit 1     ■    .    .    .    ■
 bit 2     ■    .    .    .    ■
 bit 3     ■    .    .    .    ■
 bit 4     ■    ■    ■    ■    ■
 bit 5     ■    .    .    .    ■
 bit 6     ■    .    .    .    ■
```

Fontul stă în memoria flash datorită lui `PROGMEM` — Nano are doar 2 KB de RAM, dar 30 KB de flash. Îl citim cu `pgm_read_byte()`.

### Pasul 4. Codul complet

```cpp
// Display OLED 128x64 I2C (SSD1306) fără biblioteci suplimentare — doar Wire.h
// Conectare Arduino Nano/Uno: VCC -> 5V, GND -> GND, SCL -> A5, SDA -> A4

#include <Wire.h>
#include <avr/pgmspace.h>

uint8_t oledAddr = 0x3C;  // de obicei 0x3C, uneori 0x3D (se detectează în setup)

// Font 5x7: spațiu, 0-9, A-Z (fiecare literă = 5 coloane a câte 8 pixeli)
const uint8_t font[][5] PROGMEM = {
  {0x00,0x00,0x00,0x00,0x00}, // ' '
  {0x3E,0x51,0x49,0x45,0x3E}, {0x00,0x42,0x7F,0x40,0x00}, // 0 1
  {0x42,0x61,0x51,0x49,0x46}, {0x21,0x41,0x45,0x4B,0x31}, // 2 3
  {0x18,0x14,0x12,0x7F,0x10}, {0x27,0x45,0x45,0x45,0x39}, // 4 5
  {0x3C,0x4A,0x49,0x49,0x30}, {0x01,0x71,0x09,0x05,0x03}, // 6 7
  {0x36,0x49,0x49,0x49,0x36}, {0x06,0x49,0x49,0x29,0x1E}, // 8 9
  {0x7E,0x11,0x11,0x11,0x7E}, {0x7F,0x49,0x49,0x49,0x36}, // A B
  {0x3E,0x41,0x41,0x41,0x22}, {0x7F,0x41,0x41,0x22,0x1C}, // C D
  {0x7F,0x49,0x49,0x49,0x41}, {0x7F,0x09,0x09,0x09,0x01}, // E F
  {0x3E,0x41,0x49,0x49,0x7A}, {0x7F,0x08,0x08,0x08,0x7F}, // G H
  {0x00,0x41,0x7F,0x41,0x00}, {0x20,0x40,0x41,0x3F,0x01}, // I J
  {0x7F,0x08,0x14,0x22,0x41}, {0x7F,0x40,0x40,0x40,0x40}, // K L
  {0x7F,0x02,0x0C,0x02,0x7F}, {0x7F,0x04,0x08,0x10,0x7F}, // M N
  {0x3E,0x41,0x41,0x41,0x3E}, {0x7F,0x09,0x09,0x09,0x06}, // O P
  {0x3E,0x41,0x51,0x21,0x5E}, {0x7F,0x09,0x19,0x29,0x46}, // Q R
  {0x46,0x49,0x49,0x49,0x31}, {0x01,0x01,0x7F,0x01,0x01}, // S T
  {0x3F,0x40,0x40,0x40,0x3F}, {0x1F,0x20,0x40,0x20,0x1F}, // U V
  {0x3F,0x40,0x38,0x40,0x3F}, {0x63,0x14,0x08,0x14,0x63}, // W X
  {0x07,0x08,0x70,0x08,0x07}, {0x61,0x51,0x49,0x45,0x43}  // Y Z
};

// Trimite o comandă: octetul de control 0x00 = "urmează comandă"
void cmd(uint8_t c) {
  Wire.beginTransmission(oledAddr);
  Wire.write(0x00);
  Wire.write(c);
  Wire.endTransmission();
}

// Fixează cursorul: coloana 0..127, pagina 0..7 (o pagină = 8 rânduri de pixeli)
void setPos(uint8_t col, uint8_t page) {
  cmd(0x21); cmd(col);  cmd(127);
  cmd(0x22); cmd(page); cmd(7);
}

void oledInit() {
  const uint8_t init[] = {
    0xAE,       // display OFF
    0xD5, 0x80, // frecvența ceasului
    0xA8, 0x3F, // multiplex = 64 rânduri
    0xD3, 0x00, // fără offset
    0x40,       // linia de start 0
    0x8D, 0x14, // pornește charge pump (obligatoriu!)
    0x20, 0x00, // adresare orizontală
    0xA1, 0xC8, // orientare (oglindire X/Y)
    0xDA, 0x12, // configurare pini COM
    0x81, 0xCF, // contrast
    0xD9, 0xF1, // pre-charge
    0xDB, 0x40, // VCOMH
    0xA4,       // afișează conținutul RAM
    0xA6,       // normal (nu inversat)
    0xAF        // display ON
  };
  for (uint8_t i = 0; i < sizeof(init); i++) cmd(init[i]);
}

// Șterge tot ecranul: 128*64/8 = 1024 octeți de zero
void clearScreen() {
  setPos(0, 0);
  for (int i = 0; i < 1024; i += 16) {  // bufferul Wire are doar 32 octeți
    Wire.beginTransmission(oledAddr);
    Wire.write(0x40);                   // octetul de control 0x40 = "urmează date"
    for (uint8_t j = 0; j < 16; j++) Wire.write(0x00);
    Wire.endTransmission();
  }
}

void drawChar(char c) {
  uint8_t idx = 0;                                   // implicit spațiu
  if (c >= '0' && c <= '9') idx = 1 + c - '0';
  else if (c >= 'A' && c <= 'Z') idx = 11 + c - 'A';
  else if (c >= 'a' && c <= 'z') idx = 11 + c - 'a'; // litere mici -> mari

  Wire.beginTransmission(oledAddr);
  Wire.write(0x40);
  for (uint8_t i = 0; i < 5; i++) Wire.write(pgm_read_byte(&font[idx][i]));
  Wire.write(0x00);                                  // spațiu între litere
  Wire.endTransmission();
}

void drawText(uint8_t col, uint8_t page, const char *s) {
  setPos(col, page);
  while (*s) drawChar(*s++);
}

// Verifică dacă la adresa dată răspunde un dispozitiv I2C
bool i2cPresent(uint8_t addr) {
  Wire.beginTransmission(addr);
  return Wire.endTransmission() == 0;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (i2cPresent(0x3C)) oledAddr = 0x3C;
  else if (i2cPresent(0x3D)) oledAddr = 0x3D;
  else {
    Serial.println("OLED negasit pe I2C (0x3C/0x3D) - verifica firele SDA=A4, SCL=A5");
    return;
  }
  Serial.print("OLED gasit la adresa 0x");
  Serial.println(oledAddr, HEX);

  oledInit();
  clearScreen();
  drawText(0, 0, "SALUT");
  drawText(0, 2, "CERC DE INFORMATICA");
  drawText(0, 4, "2025");
  Serial.println("Text afisat");
}

void loop() {}
```

!!! note "De ce câte 16 octeți la ștergere?"
    Biblioteca `Wire` pe Arduino are un buffer de doar **32 de octeți**. Ce trimiți peste această limită într-o singură transmisie se pierde.

Fiecare literă ocupă 6 coloane (5 + un spațiu), deci pe un rând încap **21 de caractere**, iar pe ecran — **8 rânduri**. Programul ocupă 4,4 KB de flash și 562 de octeți de RAM. În Serial Monitor (9600 baud) trebuie să apară `OLED gasit la adresa 0x3C`.

## Varianta 2: biblioteca Adafruit SSD1306

### Pasul 1. Instalarea bibliotecilor

În Arduino IDE: **Tools → Manage Libraries…**, caută **Adafruit SSD1306** → **Install**, iar la întrebarea despre dependențe (**Adafruit GFX Library**, **Adafruit BusIO**) alege **Install All**. Din linia de comandă:

```bash
arduino-cli lib install "Adafruit SSD1306"
```

### Pasul 2. Ideea principală: bufferul

Biblioteca păstrează o **copie a ecranului în RAM-ul Arduino** (1024 de octeți). Toate funcțiile de desenare modifică doar această copie, iar imaginea ajunge pe ecran abia la **`display.display()`**.

```board
  drawLine(), print(), drawCircle()...
              │
              ▼
   ┌─────────────────────┐   display.display()   ┌──────────┐
   │ buffer în RAM       │ ────────────────────► │  OLED    │
   │ (1024 octeți)       │        prin I2C       │          │
   └─────────────────────┘                       └──────────┘
```

Avantajul: poți desena orice pixel, oriunde, iar imaginea apare dintr-o dată, fără pâlpâire. Dezavantajul: bufferul ia jumătate din cei 2 KB de RAM ai lui Nano.

!!! warning "Ecranul rămâne gol?"
    Cea mai frecventă greșeală: ai desenat, dar ai uitat `display.display()`.

### Pasul 3. Funcțiile de bază

| Funcție                              | Ce face                                          |
|--------------------------------------|--------------------------------------------------|
| `clearDisplay()`                     | golește bufferul                                 |
| `setCursor(x, y)`                    | poziția textului în **pixeli**                   |
| `setTextSize(n)`                     | mărește literele de `n` ori (1 = 6×8 pixeli)     |
| `setTextColor(c)`                    | `SSD1306_WHITE` sau `SSD1306_BLACK`              |
| `print()` / `println()`              | ca la `Serial` — text, numere, `float`           |
| `drawPixel(x, y, c)`                 | un pixel                                         |
| `drawLine(x0, y0, x1, y1, c)`        | linie                                            |
| `drawRect` / `fillRect(x, y, w, h, c)` | dreptunghi / dreptunghi plin                   |
| `drawCircle` / `fillCircle(x, y, r, c)` | cerc / disc                                   |
| `fillTriangle(x0,y0, x1,y1, x2,y2, c)` | triunghi plin                                  |
| `display()`                          | trimite bufferul pe ecran                        |

Coordonatele pornesc din colțul stânga-sus: `x` crește spre dreapta (0–127), `y` în jos (0–63).

### Pasul 4. Codul complet

Programul arată în buclă: text în trei mărimi → forme geometrice → text inversat → un contor 0–100% cu bară de progres.

```cpp
// Display OLED 128x64 I2C (SSD1306) cu bibliotecile Adafruit SSD1306 + Adafruit GFX
// Conectare Arduino Nano/Uno: VCC -> 5V, GND -> GND, SCL -> A5, SDA -> A4

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH   128
#define SCREEN_HEIGHT  64
#define OLED_RESET     -1     // display-ul nu are pin RESET separat
#define SCREEN_ADDRESS 0x3C   // dacă nu merge, încearcă 0x3D

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// 1. Text în mai multe mărimi
void demoText() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);            // 6x8 pixeli pe literă
  display.setCursor(0, 0);
  display.println(F("Cerc de informatica"));

  display.setTextSize(2);            // 12x16 pixeli pe literă
  display.setCursor(0, 16);
  display.println(F("Salut!"));

  display.setTextSize(3);            // 18x24 pixeli pe literă
  display.setCursor(0, 38);
  display.println(F("2025"));

  display.display();                 // abia acum imaginea ajunge pe ecran
}

// 2. Forme geometrice
void demoShapes() {
  display.clearDisplay();
  display.drawRect(0, 0, 40, 30, SSD1306_WHITE);           // dreptunghi
  display.fillRect(45, 0, 40, 30, SSD1306_WHITE);          // dreptunghi plin
  display.drawCircle(108, 15, 14, SSD1306_WHITE);          // cerc
  display.drawLine(0, 63, 127, 34, SSD1306_WHITE);         // linie
  display.fillTriangle(64, 36, 44, 63, 84, 63, SSD1306_WHITE);
  display.display();
}

// 3. Text inversat (negru pe alb)
void demoInverse() {
  display.clearDisplay();
  display.fillRect(0, 20, 128, 24, SSD1306_WHITE);
  display.setTextColor(SSD1306_BLACK);
  display.setTextSize(2);
  display.setCursor(10, 25);
  display.print(F("INVERSAT"));
  display.display();
}

// 4. Contor cu bară de progres
void demoCounter() {
  for (int i = 0; i <= 100; i += 5) {
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print(F("Incarcare..."));

    display.setTextSize(3);
    display.setCursor(30, 18);
    display.print(i);
    display.print('%');

    display.drawRect(0, 52, 128, 12, SSD1306_WHITE);           // contur bară
    display.fillRect(2, 54, map(i, 0, 100, 0, 124), 8, SSD1306_WHITE);
    display.display();
    delay(100);
  }
}

void setup() {
  Serial.begin(9600);

  // begin() alocă bufferul de 1024 octeți în RAM și inițializează ecranul
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("Eroare: SSD1306 nu a pornit (adresa sau firele?)"));
    for (;;);                        // oprim programul
  }
  Serial.println(F("OLED pornit"));
}

void loop() {
  demoText();    delay(2000);
  demoShapes();  delay(2000);
  demoInverse(); delay(2000);
  demoCounter(); delay(1000);
}
```

`F("text")` păstrează textul în flash, nu în RAM — pe Nano merită folosit mereu. Principiul oricărei animații: **șterge → desenează cadrul nou → `display()` → pauză**.

## Comparație

| Parametru     | Varianta 1 (fără bibliotecă)  | Varianta 2 (Adafruit)                 |
|---------------|-------------------------------|---------------------------------------|
| Flash         | 4,4 KB (14%)                  | 15,6 KB (50%)                         |
| RAM           | ~0,6 KB                       | ~1,5 KB (cu bufferul de 1 KB)         |
| Poziționare   | coloană + pagină (8 px)       | orice pixel (x, y)                    |
| Font          | doar ce desenezi tu           | ASCII complet, mărimi 1–8             |
| Grafică       | nu                            | linii, cercuri, triunghiuri, imagini  |
| Ce înveți     | cum funcționează display-ul   | cum să-l folosești rapid              |

!!! note "RAM-ul raportat la compilare"
    Pentru varianta 2 compilatorul raportează doar ~523 de octeți de RAM, pentru că bufferul de 1024 de octeți se alocă abia la `display.begin()`. Dacă adaugi multe variabile și `begin()` întoarce `false`, ai rămas fără memorie.

## Încărcarea pe placă

1. **Tools → Board → Arduino Nano**.
2. **Tools → Processor → ATmega328P (Old Bootloader)** — pentru majoritatea clonelor Nano. Dacă upload-ul dă eroare, încearcă **ATmega328P**.
3. **Tools → Port** — portul plăcii (`COM3`, `/dev/cu.usbserial-…`).
4. **Upload**, apoi **Tools → Serial Monitor** la 9600 baud.

```bash
arduino-cli compile -b arduino:avr:nano:cpu=atmega328old .
arduino-cli upload  -b arduino:avr:nano:cpu=atmega328old -p /dev/cu.usbserial-1460 .
```

## Probleme frecvente

| Simptom                                     | Cauza / soluția                                                        |
|---------------------------------------------|------------------------------------------------------------------------|
| `not in sync: resp=0x00` la upload          | Alege **ATmega328P (Old Bootloader)** la Processor                     |
| „OLED negasit” / „SSD1306 nu a pornit”      | Verifică firele — SDA și SCL inversate e greșeala cea mai des întâlnită; încearcă adresa `0x3D` |
| Ecran negru, dar display-ul răspunde        | Lipsește `0x8D, 0x14` (varianta 1) sau `display()` (varianta 2)        |
| Text oglindit sau cu susul în jos           | Schimbă `0xA1` ↔ `0xA0` sau `0xC8` ↔ `0xC0`                            |
| Apare logo-ul Adafruit                      | `begin()` pune logo-ul în buffer; apelează `clearDisplay()` înainte de primul `display()` |
| Pixeli aleatori, imagine deplasată cu 2 px  | Display-ul are controler **SH1106** (de obicei cele de 1.3"), nu SSD1306 — folosește `Adafruit SH110X` sau `U8g2` |

## Exerciții

1. Varianta 1: adaugă în font semnele `!`, `?`, `.` și `:` — desenează-le întâi pe hârtie, într-o grilă 5×7.
2. Varianta 1: afișează secundele de la pornire (`millis() / 1000`). Indiciu: `itoa()` transformă un număr în text.
3. Varianta 2: o minge care sare de pereții ecranului (variabile `x`, `y`, `dx`, `dy`).
4. Varianta 2: un potențiometru pe `A0` — afișează `analogRead(A0)` ca număr și ca bară de progres.
5. Varianta 2: desenează graficul funcției `sin` pe toată lățimea ecranului.

## Referințe

- [Random Nerd Tutorials — Guide for I2C OLED Display with Arduino](https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/)
- [Fișa tehnică SSD1306 (PDF)](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
- [Adafruit SSD1306 pe GitHub](https://github.com/adafruit/Adafruit_SSD1306)
- [Adafruit GFX — ghid de grafică](https://learn.adafruit.com/adafruit-gfx-graphics-library)
- [U8g2 — bibliotecă alternativă, suportă și SH1106](https://github.com/olikraus/u8g2)
