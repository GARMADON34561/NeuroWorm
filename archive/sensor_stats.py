import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])

ENABLE_SENSOR_D = bytes([
    0x0A,
    0x00,
    0x41,
    0x03,
    0x00,
    0x01,
    0x00,
    0x00,
    0x00,
    0x01
])

last_value = None

def cb(sender, data):

    global last_value

    msg = data.hex()

    if msg.startswith("05004503"):

        value = int(msg[-2:], 16)

        if value != last_value:
            print(f"Sensor changed -> {value}")

            last_value = value

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            cb
        )

        # Keepalive
        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(1)

        # Enable sensor D
        await client.write_gatt_char(
            CHAR,
            ENABLE_SENSOR_D,
            response=False
        )

        print(
            "\nTEST POSITIONS:"
            "\nA = Nothing nearby"
            "\nB = Hand close"
            "\nC = Covered"
            "\nD = Flashlight"
        )

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            await asyncio.sleep(2)

asyncio.run(main())