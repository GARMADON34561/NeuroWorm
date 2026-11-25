# read_test.py

import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"

CHAR = "00001624-1212-efde-1623-785feabcd123"

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected:", client.is_connected)

        await asyncio.sleep(2)

        try:
            data = await client.read_gatt_char(CHAR)
            print(data)
        except Exception as e:
            print("ERROR:", e)

asyncio.run(main())