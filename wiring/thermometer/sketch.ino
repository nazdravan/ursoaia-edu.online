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
