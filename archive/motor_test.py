# motor_test.py

import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05,0x00,0x01,0x01,0x00
])

# Port Output Command
# Port 0x00 = Motor A
MOTOR_A_TEST = bytes([
    0x08,       # length
    0x00,
    0x81,       # Port Output Command
    0x00,       # Port A
    0x11,       # Execute immediately
    0x51,       # Start Power command
    0x32,       # Power = +50
    0x00
])

def cb(sender, data):
    print("RX:", data.hex())

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(CHAR, cb)

        # Keepalive
        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        print("Sending motor command")

        await client.write_gatt_char(
            CHAR,
            MOTOR_A_TEST,
            response=False
        )

        await asyncio.sleep(10)

asyncio.run(main())