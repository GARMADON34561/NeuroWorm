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

        # Keep hub alive
        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        # Port C (0x02)
        cmd = bytes([
            0x08,
            0x00,
            0x81,
            0x02,
            0x11,
            0x51,
            0x64,  # power 100
            0x00
        ])

        print("Sending Motor C command")

        await client.write_gatt_char(
            CHAR,
            cmd,
            response=False
        )

        await asyncio.sleep(5)

asyncio.run(main())