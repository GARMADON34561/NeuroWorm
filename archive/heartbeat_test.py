# heartbeat_test.py

import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])

def callback(sender, data):
    print("RX:", data.hex())

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(CHAR, callback)

        count = 0

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            print("TX", count)

            count += 1

            await asyncio.sleep(2)

asyncio.run(main())