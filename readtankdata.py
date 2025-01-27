"""
=================================================================
 RV Intelligence Device
 Emmanuel Loria, Jordan Krause, Maya Hampton
 Date 1/15/2025
 Script to read data from the Mopeka Sensors via BLE Connection
 https://chatgpt.com/share/67980b5a-8c5c-8001-8f81-2f3e6a8debc7
    > used to learn how to read data from the Mopeka Sensors
=================================================================
"""

import asyncio
from bleak import BleakClient

# Mopeka sensor's MAC address
sensor_address = "DA:53:DE:F3:55:C7"  

# connect to Mopeka Sensor and read data from sensor using UUID
async def subscribe_to_notifications():
    async with BleakClient(sensor_address) as client:
        def notification_handler(sender, data):
            print(f"{data}") # print the data (encoded)

        # Enable notifications on the characteristic
        notify_uuid = "6ff60201-1392-4a00-93d7-551c884c2ec7"
        await client.start_notify(notify_uuid, notification_handler)
        print(f"Subscribed to notifications on {notify_uuid}")

        # Keep the program running to listen for notifications
        await asyncio.sleep(30) 
        await client.stop_notify(notify_uuid)

# Run the script
asyncio.run(subscribe_to_notifications())
