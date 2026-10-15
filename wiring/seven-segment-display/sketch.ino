/*
 * Proiect 19 — Afișaj 7-segmente cu 74HC595
 * Numără de la 9 la 0.
 */

int dataPin = 2;
int latchPin = 3;
int clockPin = 4;

// Tabelul cifrelor (catod comun): bit 7=DP, 6=G, 5=F, 4=E, 3=D, 2=C, 1=B, 0=A
byte digits[10] = {
  B00111111, // 0
  B00000110, // 1
  B01011011, // 2
  B01001111, // 3
  B01100110, // 4
  B01101101, // 5
  B01111101, // 6
  B00000111, // 7
  B01111111, // 8
  B01101111  // 9
};

void displayDigit(byte d) {
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, digits[d]);
  digitalWrite(latchPin, HIGH);
}

void setup() {
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

void loop() {
  for (int i = 9; i >= 0; i--) {
    displayDigit(i);
    delay(1000);
  }
}
