// Exercise 3: why the acquisition firmware uses micros() and not delay().
// Run it with USE_MICROS = false, then with true, and compare the samples per second.

const bool USE_MICROS = true;
const unsigned long PERIOD_US = 1000;  // one sample every 1000 us = 1 kHz

unsigned long next_t, last_report;
unsigned long count = 0;
int sample;

void setup() {
  Serial.begin(115200);
  next_t = micros();
  last_report = millis();
}

void loop() {
  if (USE_MICROS) {
    if ((long)(micros() - next_t) >= 0) {  // it is time for the next sample
      next_t += PERIOD_US;                 // the next one is due exactly 1000 us later
      sample = analogRead(A0);
      count++;
    }
  } else {
    sample = analogRead(A0);  // the reading itself takes about 0.1 ms...
    count++;
    delay(1);                 // ...and then we wait 1 ms more
  }

  if (millis() - last_report >= 1000) {  // once per second, report and restart the count
    last_report += 1000;
    Serial.print("campioni nell'ultimo secondo: ");
    Serial.println(count);
    count = 0;
  }
}