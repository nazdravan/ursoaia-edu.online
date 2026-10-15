/*
 * Proiect 22 — Motor stepper 28BYJ-48 cu ULN2003
 * Rotește o tură completă într-un sens, apoi invers.
 * Bibliotecă: Stepper (inclusă în Arduino IDE)
 */

#include <Stepper.h>

// Numărul de pași pentru o rotație completă
const int stepsPerRevolution = 2048;

// Notă: ordinea pinilor este (8, 10, 9, 11) pentru secvența corectă pe 28BYJ-48
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  myStepper.setSpeed(10); // rotații/minut
  Serial.begin(9600);
}

void loop() {
  Serial.println("Rotire inainte");
  myStepper.step(stepsPerRevolution);
  delay(1000);

  Serial.println("Rotire inapoi");
  myStepper.step(-stepsPerRevolution);
  delay(1000);
}
