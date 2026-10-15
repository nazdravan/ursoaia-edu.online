/*
 * Proiect 24 — Senzor nivel apă
 * Afișează valoarea analogică pe Serial Monitor.
 */

int waterPin = A0;
int value = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  value = analogRead(waterPin);

  Serial.print("Nivel apa: ");
  Serial.print(value);

  if (value < 100) {
    Serial.println("  [USCAT]");
  } else if (value < 400) {
    Serial.println("  [Putin]");
  } else if (value < 700) {
    Serial.println("  [Mediu]");
  } else {
    Serial.println("  [MULT!]");
  }

  delay(500);
}
