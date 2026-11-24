// Exercise 1: the structure of every sketch. setup() runs once, loop() runs forever.

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);   // the small LED on the board is an output
  Serial.begin(115200);           // opens the serial line towards the PC
  Serial.println("Ciao, sono vivo");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // LED on
  delay(500);                       // wait 500 ms
  digitalWrite(LED_BUILTIN, LOW);   // LED off
  delay(500);                       // wait 500 ms
  Serial.println(millis());         // milliseconds since the board started
}