/*
 * Proiect 5 — Senzor cu bilă (tilt)
 * Când senzorul este înclinat, LED-ul integrat se aprinde.
 */

int tiltPin = 2;
int ledPin = 13;
int tiltState = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(tiltPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  tiltState = digitalRead(tiltPin);

  if (tiltState == LOW) {           // circuit închis (bila conectează)
    digitalWrite(ledPin, HIGH);
    Serial.println("Inclinat!");
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(100);
}
