# inspect_hub.py

import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected:", client.is_connected)

        for service in client.services:
            print("\nSERVICE", service.uuid)

            for char in service.characteristics:
                print("   ", char.uuid, char.properties)

asyncio.run(main())
