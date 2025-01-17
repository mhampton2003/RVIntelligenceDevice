import asyncio
from bleak import BleakClient

# Replace this with your Mopeka sensor's Bluetooth address
sensor_address = "XX:XX:XX:XX:XX:XX"

async def discover_services():
    async with BleakClient(sensor_address) as client:
        print(f"Connected to {sensor_address}")
        # Get all services and their characteristics
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - Properties: {char.properties}")

# Run the script
asyncio.run(discover_services())
