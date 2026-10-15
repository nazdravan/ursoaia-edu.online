/*
 * Cub de LED-uri 3x3x3 — Arduino Uno
 */

// === Configurare pini ===
const byte COL_PINS[9] = {2, 3, 4, 5, 6, 7, 8, 9, 10};
const byte LAYER_PINS[3] = {11, 12, 13};

#define NUM_LAYERS  3
#define NUM_COLS    9

uint16_t cube[NUM_LAYERS];
#define POV_DELAY 3

void displayCube() {
  for (byte layer = 0; layer < NUM_LAYERS; layer++) {
    for (byte l = 0; l < NUM_LAYERS; l++) digitalWrite(LAYER_PINS[l], LOW);
    for (byte col = 0; col < NUM_COLS; col++) digitalWrite(COL_PINS[col], (cube[layer] >> col) & 1);
    digitalWrite(LAYER_PINS[layer], HIGH);
    delay(POV_DELAY);
  }
  for (byte l = 0; l < NUM_LAYERS; l++) digitalWrite(LAYER_PINS[l], LOW);
}

void showFor(unsigned long duration) {
  unsigned long start = millis();
  while (millis() - start < duration) displayCube();
}

void clearCube() {
  for (byte i = 0; i < NUM_LAYERS; i++) cube[i] = 0;
}

void fillCube() {
  for (byte i = 0; i < NUM_LAYERS; i++) cube[i] = 0b111111111;
}

void setLed(byte x, byte y, byte z, bool state) {
  byte col = y * 3 + x;
  if (state) cube[z] |= (1 << col);
  else cube[z] &= ~(1 << col);
}

// Animațiile sunt omise pentru scurtarea acestui fragment,
// dar poți adăuga propriile tale!
// Vezi codul complet pentru detalii.

void setup() {
  for (byte i = 0; i < NUM_COLS; i++) {
    pinMode(COL_PINS[i], OUTPUT);
    digitalWrite(COL_PINS[i], LOW);
  }
  for (byte i = 0; i < NUM_LAYERS; i++) {
    pinMode(LAYER_PINS[i], OUTPUT);
    digitalWrite(LAYER_PINS[i], LOW);
  }
  randomSeed(analogRead(A0));
  clearCube();
}

void loop() {
  fillCube();
  showFor(1000);
  clearCube();
  showFor(500);
}
