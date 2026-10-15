/*
 * Proiect 18 — Fotocelulă
 * Numărul de LED-uri aprinse = cât de multă lumină este.
 */

int latchPin = 11;
int clockPin = 9;
int dataPin = 12;
int lightPin = A0;
byte leds = 0;

void updateShiftRegister() {
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, leds);
  digitalWrite(latchPin, HIGH);
}

void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(lightPin);
  int numLEDSLit = reading / 57; // împarte 0-1023 în 9 intervale

  if (numLEDSLit > 8) numLEDSLit = 8;

  leds = 0;
  for (int i = 0; i < numLEDSLit; i++) {
    bitSet(leds, i);
  }
  updateShiftRegister();

  Serial.print("Lumina: ");
  Serial.print(reading);
  Serial.print("  LED-uri: ");
  Serial.println(numLEDSLit);

  delay(100);
}
