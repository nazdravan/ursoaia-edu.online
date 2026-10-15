/*
 * Proiect 16 — 8 LED-uri cu 74HC595
 * Aprinde LED-urile pe rând, apoi le stinge.
 */

int latchPin = 11;
int clockPin = 9;
int dataPin = 12;

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
}

void loop() {
  leds = 0;
  updateShiftRegister();
  delay(500);

  for (int i = 0; i < 8; i++) {
    bitSet(leds, i);       // setează bit-ul i la 1
    updateShiftRegister();
    delay(500);
  }
}
