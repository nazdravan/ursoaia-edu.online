/*
 * Proiect 4 — Intrări digitale cu două butoane
 */

int ledPin = 9;
int buttonApin = 2;
int buttonBpin = 3;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);  // pull-up intern activ
  pinMode(buttonBpin, INPUT_PULLUP);
}

void loop() {
  // Butonul A apăsat → LED aprins
  if (digitalRead(buttonApin) == LOW) {
    digitalWrite(ledPin, HIGH);
  }
  // Butonul B apăsat → LED stins
  if (digitalRead(buttonBpin) == LOW) {
    digitalWrite(ledPin, LOW);
  }
}
