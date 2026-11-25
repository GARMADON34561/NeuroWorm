import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected!")

        await asyncio.sleep(20)

        name = await client.read_gatt_char(
            "00002a00-0000-1000-8000-00805f9b34fb"
        )

        print(name)

asyncio.run(main())