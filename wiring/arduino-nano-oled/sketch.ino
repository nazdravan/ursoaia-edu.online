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
