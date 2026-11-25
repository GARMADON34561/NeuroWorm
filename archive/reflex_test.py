import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05,0x00,0x01,0x01,0x00
])

ENABLE_SENSOR = bytes([
    0x0A,0x00,0x41,0x03,
    0x00,0x01,0x00,0x00,
    0x00,0x01
])

motor_triggered = False
client_ref = None


async def move_motor():

    global client_ref

    cmd = bytes([
        0x08,
        0x00,
        0x81,
        0x02,
        0x11,
        0x01,
        0x64,
        0x00
    ])

    await client_ref.write_gatt_char(
        CHAR,
        cmd,
        response=False
    )


def cb(sender, data):

    global motor_triggered

    msg = data.hex()

    if msg.startswith("05004503"):

        value = int(msg[-2:], 16)

        print("Sensor:", value)

        if value != 255 and not motor_triggered:

            motor_triggered = True

            asyncio.create_task(
                move_motor()
            )


async def main():

    global client_ref

    async with BleakClient(ADDRESS) as client:

        client_ref = client

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
            ENABLE_SENSOR,
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