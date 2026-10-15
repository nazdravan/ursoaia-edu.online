/*
 * Proiect 2 — LED intermitent
 * Face un LED să clipească la fiecare secundă.
 */

int ledPin = 10;

void setup() {
  pinMode(ledPin, OUTPUT);   // Pinul 10 ca ieșire digitală
}

void loop() {
  digitalWrite(ledPin, HIGH); // LED aprins
  delay(1000);                // Așteaptă 1 secundă
  digitalWrite(ledPin, LOW);  // LED stins
  delay(1000);                // Așteaptă 1 secundă
}
