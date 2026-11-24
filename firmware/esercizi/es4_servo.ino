// Exercise 4: the potentiometer moves the servo.
#include <Servo.h>

Servo servo;

void setup() {
  servo.attach(9);  // servo signal wire on pin 9
}

void loop() {
  int v = analogRead(A0);               // 0..1023
  int angle = map(v, 0, 1023, 0, 180);  // rescale to 0..180 degrees
  servo.write(angle);
  delay(15);                            // give the servo time to move
}