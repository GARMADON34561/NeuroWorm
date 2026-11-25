import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])


def motor_c(speed):

    return bytes([
        0x08,
        0x00,
        0x81,
        0x02,  # Port C

        0x11,
        0x01,

        speed & 0xFF,

        0x00
    ])


async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        print("LEFT")

        await client.write_gatt_char(
            CHAR,
            motor_c(40),
            response=False
        )

        await asyncio.sleep(1)

        print("STOP")

        await client.write_gatt_char(
            CHAR,
            motor_c(0),
            response=False
        )

        await asyncio.sleep(2)

        print("RIGHT")

        await client.write_gatt_char(
            CHAR,
            motor_c(216),  # -40
            response=False
        )

        await asyncio.sleep(1)

        print("STOP")

        await client.write_gatt_char(
            CHAR,
            motor_c(0),
            response=False
        )

        await asyncio.sleep(2)

asyncio.run(main())