/*
 * Proiect 11 — Modul releu
 * Pornește și oprește releul la fiecare 2 secunde.
 */

int relayPin = 8;

void setup() {
  pinMode(relayPin, OUTPUT);
}

void loop() {
  digitalWrite(relayPin, HIGH); // Activează releul (clic!)
  delay(2000);
  digitalWrite(relayPin, LOW);  // Dezactivează releul
  delay(2000);
}
