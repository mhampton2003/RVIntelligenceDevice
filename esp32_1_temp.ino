/**
=================================================================
 RV Intelligence Device
 Emmanuel Loria, Jordan Krause, Maya Hampton
 Date 11/20/2024
 Script to allow ESP32 to connect via BlueTooth and read temperature
 https://youtu.be/bsss1MyXVNI?si=Iq3n1tNmUvDSUoeq
    > used to learn how to set up BlueTooth connection
=================================================================
**/

#include <DHT.h>
#include "BluetoothSerial.h"
#include <ArduinoJson.h>

BluetoothSerial SerialBT; // Initialize Bluetooth

DHT dht(4, DHT11);

void setup() {

  Serial.begin(115200);   // Serial monitor
  SerialBT.begin("ESP32_2"); // Bluetooth device name
  Serial.println("Bluetooth started, waiting for connection...");
  dht.begin();
  delay(2000);
  Serial.begin(115200);
}

void loop() {

  // if the ESP32 is connected then run
  if (SerialBT.connected()) {
    // print data through the BlueTooth Serial port
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();
    SerialBT.print((temp * 1.8) + 31);
    SerialBT.print(humidity);
    delay(2000);

  }
}
