/*
 * Proiect 9 — Joystick analogic
 * Afișează în Serial valorile X, Y și starea butonului.
 */

int xPin = A0;
int yPin = A1;
int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  int xValue = analogRead(xPin);
  int yValue = analogRead(yPin);
  int btn = digitalRead(buttonPin);  // LOW = apăsat

  Serial.print("X = ");
  Serial.print(xValue);
  Serial.print("  Y = ");
  Serial.print(yValue);
  Serial.print("  Buton = ");
  Serial.println(btn == LOW ? "APASAT" : "liber");

  delay(200);
}
