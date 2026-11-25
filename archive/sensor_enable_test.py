import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])

def cb(sender, data):
    print("RX:", data.hex())

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(CHAR, cb)

        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        cmd = bytes([
            0x0A,
            0x00,
            0x41,
            0x03,   # Port D
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x01
        ])

        print("Enabling Sensor D")

        await client.write_gatt_char(
            CHAR,
            cmd,
            response=False
        )

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            await asyncio.sleep(2)

asyncio.run(main())