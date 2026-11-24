// Exercise 2: read an analog input and plot it. The potentiometer stands in for the EMG amplifier.
// On the UNO R3 of the simulator the ADC has 10 bits (0..1023); the UNO R4 of the project has 14.

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println(analogRead(A0));  // one number per line: the plotter draws it
  delay(2);                        // about 470 samples per second, see below
}