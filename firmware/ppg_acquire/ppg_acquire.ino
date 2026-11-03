// PPG acquisition: ESP32 + MAX30102
// Prints one line per sample over USB serial: millis,red,ir
// Wiring: VIN -> 3V3, GND -> GND, SDA -> GPIO 21, SCL -> GPIO 22
// Library: "SparkFun MAX3010x Pulse and Proximity Sensor Library"

#include <Wire.h>
#include "MAX30105.h"

MAX30105 sensor;

void setup() {
  Serial.begin(115200);               // must match BAUD in python/acquire.py
  Wire.begin(21, 22);                 // SDA = GPIO 21, SCL = GPIO 22
  if (!sensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found");
    while (1);
  }
  // LED brightness, averaging, mode (2 = red + IR), sample rate,
  // pulse width, ADC range
  // 400 samples/s averaged over 4 -> 100 samples per second
  sensor.setup(0x3F, 4, 2, 400, 411, 16384);
}

void loop() {
  sensor.check();
  while (sensor.available()) {
    Serial.print(millis());
    Serial.print(",");
    Serial.print(sensor.getFIFORed());
    Serial.print(",");
    Serial.println(sensor.getFIFOIR());
    sensor.nextSample();
  }
}
