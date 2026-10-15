/*
 * Proiect 20 — Afișaj 4 cifre 7-segmente
 * Afișează un număr între 0 și 9999, incrementat la fiecare secundă.
 */

int dataPin  = 2;
int latchPin = 3;
int clockPin = 4;
int digitPins[4] = {10, 11, 12, 13}; // cifra 1..4

byte digits[10] = {
  B00111111, B00000110, B01011011, B01001111, B01100110,
  B01101101, B01111101, B00000111, B01111111, B01101111
};

int number = 0;
unsigned long lastIncrement = 0;

void showDigit(byte position, byte d) {
  for (int i = 0; i < 4; i++) digitalWrite(digitPins[i], HIGH);

  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, digits[d]);
  digitalWrite(latchPin, HIGH);

  // Aprinde doar cifra curentă (catod comun = LOW = activ)
  digitalWrite(digitPins[position], LOW);
  delay(2);
}

void displayNumber(int num) {
  for (int pos = 0; pos < 4; pos++) {
    int d = (num / (int)pow(10, 3 - pos)) % 10;
    showDigit(pos, d);
  }
}

void setup() {
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  for (int i = 0; i < 4; i++) {
    pinMode(digitPins[i], OUTPUT);
    digitalWrite(digitPins[i], HIGH);
  }
}

void loop() {
  displayNumber(number);

  if (millis() - lastIncrement > 1000) {
    number++;
    if (number > 9999) number = 0;
    lastIncrement = millis();
  }
}
