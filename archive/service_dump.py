# service_dump.py

import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected:", client.is_connected)

        services = await client.get_services()

        for service in services:
            print("\nSERVICE:", service.uuid)

            for char in service.characteristics:
                print(
                    char.uuid,
                    char.properties
                )

asyncio.run(main())