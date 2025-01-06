#include "BluetoothSerial.h"
#include <ArduinoJson.h>
#include <WiFi.h>

BluetoothSerial SerialBT; // Initialize Bluetooth

void setup() {
  Serial.begin(115200);   // Serial monitor
  SerialBT.begin("ESP32_2"); // Bluetooth device name
  Serial.println("Bluetooth started, waiting for connection...");

  

}

void loop() {

  /*
  
  StaticJsonDocument<256> doc;
  doc["id"]="ALAT01";
  doc["suhu"] = random(20,30);
  doc["kelembaban"] = random(60,80);
  serializeJson(doc, SerialBT);
  */
  if (SerialBT.connected()) {
    String data = "Sensor Reading"; // Replace with sensor data
    SerialBT.println(data);         // Send data over Bluetooth
    delay(1000);                    // Delay before next send
  }
}