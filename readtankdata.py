from bleak import BleakClient

# Replace with the Bluetooth address of your Mopeka sensor
sensor_address = "XX:XX:XX:XX:XX:XX"

# Replace with the characteristic UUID for the data you want to read
characteristic_uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

async def read_sensor_data():
    async with BleakClient(sensor_address) as client:
        print(f"Connected to {sensor_address}")

# Read the value of the specified characteristic
value = await client.read_gatt_char(characteristic_uuid)
print(f"Sensor Data: {value}")

# Run the script
import asyncio
asyncio.run(read_sensor_data())
