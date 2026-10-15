/*
 * Proiect 6 — Buzzer activ
 * Emite un bip la fiecare secundă.
 */

int buzzerPin = 8;

void setup() {
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  digitalWrite(buzzerPin, HIGH);  // Pornește sunetul
  delay(500);
  digitalWrite(buzzerPin, LOW);   // Oprește sunetul
  delay(500);
}
