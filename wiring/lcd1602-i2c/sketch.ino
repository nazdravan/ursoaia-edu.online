/*
 * Proiect 14 — LCD1602 I2C
 * Afișează două rânduri de text.
 * Bibliotecă: LiquidCrystal_I2C
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Adresa 0x27, 16 coloane, 2 rânduri
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();         // inițializează LCD-ul
  lcd.backlight();    // pornește lumina de fundal

  lcd.setCursor(0, 0);
  lcd.print("Hello, world!");
  lcd.setCursor(0, 1);
  lcd.print("Ursoaia Edu");
}

void loop() {
  // Nimic; textul rămâne afișat.
}
