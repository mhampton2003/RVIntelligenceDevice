#include <DHT.h>
#include "BluetoothSerial.h"
#include <ArduinoJson.h>

BluetoothSerial SerialBT; // Initialize Bluetooth

DHT dht(4, DHT11);

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);   // Serial monitor
  SerialBT.begin("ESP32_1"); // Bluetooth device name
  Serial.println("Bluetooth started, waiting for connection...");

  dht.begin();
  delay(2000);

  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:

  if (SerialBT.connected()) {
    
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();
    SerialBT.print("Temp 1: ");
    SerialBT.print((temp * 1.8) + 31);
    SerialBT.print(" F \n");
    delay(2000);

  }


}
