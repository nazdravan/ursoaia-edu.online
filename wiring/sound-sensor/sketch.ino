/*
 * Proiect 25 — Senzor de sunet
 * Afișează valoarea analogică și starea digitală.
 */

int analogPin = A0;
int digitalPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(digitalPin, INPUT);
}

void loop() {
  int soundLevel = analogRead(analogPin);
  int threshold = digitalRead(digitalPin);

  Serial.print("Analog: ");
  Serial.print(soundLevel);
  Serial.print("  Digital: ");
  Serial.println(threshold == HIGH ? "LINISTE" : "ZGOMOT");

  delay(50);
}
