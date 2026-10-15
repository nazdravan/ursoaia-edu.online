/*
 * Proiect 23 — Stepper controlat prin IR
 * Sus = rotație CW, Jos = rotație CCW.
 * Biblioteci: IRremote, Stepper
 */

#include <IRremote.h>
#include <Stepper.h>

const int stepsPerRevolution = 2048;
const int IR_PIN = 12;

// Înlocuiește aceste coduri cu cele ale telecomenzii tale!
#define BUTTON_UP   0x46
#define BUTTON_DOWN 0x15

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(IR_PIN, ENABLE_LED_FEEDBACK);
  myStepper.setSpeed(10);
}

void loop() {
  if (IrReceiver.decode()) {
    uint32_t code = IrReceiver.decodedIRData.command;
    Serial.print("Primit: 0x"); Serial.println(code, HEX);

    if (code == BUTTON_UP) {
      Serial.println("SUS -> rotire CW");
      myStepper.step(stepsPerRevolution);
    } else if (code == BUTTON_DOWN) {
      Serial.println("JOS -> rotire CCW");
      myStepper.step(-stepsPerRevolution);
    }
    IrReceiver.resume();
  }
}
