/*
 * Proiect 21 — Motor DC cu L293D
 * Rotește în ambele sensuri, cu pauză între mișcări.
 */

int enablePin = 5;
int in1Pin = 4;
int in2Pin = 3;

void setup() {
  pinMode(enablePin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
}

void loop() {
  // Rotire sens 1 (în sensul acelor de ceasornic)
  analogWrite(enablePin, 150);  // viteză (0-255)
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  delay(2000);

  // Oprire
  analogWrite(enablePin, 0);
  delay(2000);

  // Rotire sens 2 (invers)
  analogWrite(enablePin, 150);
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, HIGH);
  delay(2000);

  // Oprire
  analogWrite(enablePin, 0);
  delay(2000);
}
