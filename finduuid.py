"""
================================================= 
 RV Intelligence Device
 Emmanuel Loria, Jordan Krause, Maya Hampton
 Date 1/17/2025
 Script to find the characteristic UUID
 
==================================================
"""
import asyncio
from bleak import BleakClient

# Mopeka sensor's MAC address
sensor_address = "D3:89:69:6E:82:DC"

# connects to sensor using MAC address and provides UUID
async def discover_services():
    async with BleakClient(sensor_address) as client:
        print(f"Connected to {sensor_address}")
        # Get all services and their characteristics
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - Properties: {char.properties})

# Run the script
asyncio.run(discover_services())
