/*
 * Proiect 10 — Senzor ultrasonic HC-SR04
 * Afișează distanța în cm pe Serial Monitor.
 */

int trigPin = 10;
int echoPin = 9;
long duration;
float distance;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Trimite un impuls de 10μs pe Trig
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Măsoară durata impulsului pe Echo (μs)
  duration = pulseIn(echoPin, HIGH);

  // Calculăm distanța în cm
  distance = duration * 0.0343 / 2;

  Serial.print("Distanta = ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(200);
}
