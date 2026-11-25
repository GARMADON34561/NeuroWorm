import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05,0x00,0x01,0x01,0x00
])

ENABLE_SENSOR_D = bytes([
    0x0A,0x00,0x41,0x03,
    0x00,0x01,0x00,0x00,
    0x00,0x01
])

counts = {}

def cb(sender, data):

    msg = data.hex()

    if msg.startswith("05004503"):

        value = int(msg[-2:], 16)

        counts[value] = counts.get(value, 0) + 1

async def main():

    async with BleakClient(ADDRESS) as client:

        await client.start_notify(
            CHAR,
            cb
        )

        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        await client.write_gatt_char(
            CHAR,
            ENABLE_SENSOR_D,
            response=False
        )

        print("Collecting for 20 seconds...")

        for _ in range(10):

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            await asyncio.sleep(2)

        print("\nCounts:")
        print(counts)

asyncio.run(main())