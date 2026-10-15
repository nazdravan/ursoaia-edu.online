/*
 * Proiect 12 — Receptor IR
 * Afișează codul fiecărui buton apăsat pe telecomandă.
 * Bibliotecă necesară: IRremote (v3+).
 */

#include <IRremote.h>

int IR_RECV_PIN = 11;

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(IR_RECV_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
  if (IrReceiver.decode()) {
    // Afișează codul primit
    Serial.print("Cod buton: 0x");
    Serial.println(IrReceiver.decodedIRData.command, HEX);
    IrReceiver.resume(); // pregătește-te pentru următorul semnal
  }
}
