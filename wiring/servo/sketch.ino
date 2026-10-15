/*
 * Proiect 8 — Servomotor SG90
 * Rotește axul între 0° și 180°.
 */

#include <Servo.h>

Servo myservo;          // Obiectul care controlează servomotorul
int pos = 0;            // Poziția curentă

void setup() {
  myservo.attach(9);    // Servo conectat la pinul 9
}

void loop() {
  // De la 0 la 180 grade
  for (pos = 0; pos <= 180; pos += 1) {
    myservo.write(pos);
    delay(15);
  }

  // De la 180 la 0 grade
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(15);
  }
}
