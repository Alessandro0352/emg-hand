// Exercise 5: the logic of the hand actuator (firmware/actuator/actuator.ino) on the simulator.
// Commands in the Serial Monitor: C,0.5 (close) O,0.5 (open) S,0 (stop).
// Optional feedback: potentiometer on A0 = force sensor, LED on pin 5 = vibration motor.
#include <Servo.h>

const int SERVO_PIN = 9;
const int FSR_PIN = A0;
const int VIB_PIN = 5;
const bool USE_FEEDBACK = false;
const float POS_OPEN = 20.0;              // servo angle with the hand open [degrees]
const float POS_CLOSED = 150.0;           // servo angle with the hand closed [degrees]
const float MAX_RATE = 120.0;             // maximum speed [degrees per second]
const unsigned long WATCHDOG_MS = 200;   // start with 2000, then try the real value, 200
const unsigned long UPDATE_MS = 10;       // the servo position is updated every 10 ms

Servo servo;
float pos = POS_OPEN;
char dir = 'S';
float speed = 0.0;
unsigned long last_cmd = 0, last_update = 0, last_print = 0;
char line[32];
uint8_t len = 0;

void parseLine() {
  line[len] = '\0';
  if (len >= 1 && (line[0] == 'C' || line[0] == 'O' || line[0] == 'S')) {
    dir = line[0];
    speed = (len > 2) ? constrain(atof(line + 2), 0.0, 1.0) : 0.0;
    last_cmd = millis();
  }
  len = 0;
}

void setup() {
  Serial.begin(115200);
  servo.attach(SERVO_PIN);
  servo.write((int)pos);
  pinMode(VIB_PIN, OUTPUT);
  last_update = millis();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') parseLine();
    else if (c != '\r' && len < sizeof(line) - 1) line[len++] = c;
  }

  unsigned long now = millis();
  if (now - last_cmd > WATCHDOG_MS) dir = 'S';

  if (now - last_update >= UPDATE_MS) {
    float dt = (now - last_update) / 1000.0;
    last_update = now;
    if (dir == 'C') pos += speed * MAX_RATE * dt;
    if (dir == 'O') pos -= speed * MAX_RATE * dt;
    pos = constrain(pos, POS_OPEN, POS_CLOSED);
    servo.write((int)(pos + 0.5));

    if (USE_FEEDBACK) {
      int f = analogRead(FSR_PIN);  // 10 bits here: 0..1023
      int duty = map(constrain(f, 100, 750), 100, 750, 0, 150);
      analogWrite(VIB_PIN, f > 100 ? duty : 0);
    }
  }

  if (now - last_print >= 250) {  // four times per second, show where the hand is
    last_print = now;
    Serial.print("posizione ");
    Serial.print(pos);
    Serial.print(" comando ");
    Serial.println(dir);
  }
}