#include <Arduino.h>

// #define btnPin 2
// #define rpiPin 14
boolean isStart = false;

void setup() {
  /* code */
  Serial.begin(921600);
  // pinMode(rpiPin, OUTPUT);
  // digitalWrite(rpiPin, LOW);
  attachInterrupt(2, pinChanged, FALLING);
}

void loop(){

}

void pinChanged() {
  if (!isStart) {
    Serial.println('p');
    isStart = true;
  }
}
