/*
 * Proiect 3 — LED RGB cu fade între culori
 */

#define BLUE  3
#define GREEN 5
#define RED   6

int redValue, greenValue, blueValue;
int delayTime = 10;

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  // De la roșu la verde
  redValue = 255; greenValue = 0; blueValue = 0;
  for (int i = 0; i < 255; i++) {
    redValue--;
    greenValue++;
    analogWrite(RED, redValue);
    analogWrite(GREEN, greenValue);
    delay(delayTime);
  }

  // De la verde la albastru
  redValue = 0; greenValue = 255; blueValue = 0;
  for (int i = 0; i < 255; i++) {
    greenValue--;
    blueValue++;
    analogWrite(GREEN, greenValue);
    analogWrite(BLUE, blueValue);
    delay(delayTime);
  }

  // De la albastru la roșu
  redValue = 0; greenValue = 0; blueValue = 255;
  for (int i = 0; i < 255; i++) {
    blueValue--;
    redValue++;
    analogWrite(BLUE, blueValue);
    analogWrite(RED, redValue);
    delay(delayTime);
  }
}
