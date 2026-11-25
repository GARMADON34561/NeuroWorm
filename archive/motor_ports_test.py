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

        # Keep session alive
        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        ports = [0x00, 0x01, 0x02, 0x03]

        for port in ports:

            print(f"\nTrying port {port}")

            cmd = bytes([
                0x08,
                0x00,
                0x81,
                port,
                0x11,
                0x51,
                0x32,
                0x00
            ])

            await client.write_gatt_char(
                CHAR,
                cmd,
                response=False
            )

            await asyncio.sleep(3)

asyncio.run(main())