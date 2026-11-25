import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

latest = 255

COLOR_MAP = {

    255: "NONE",

    0: "BLACK",

    5: "GREEN",

    7: "YELLOW",

    9: "RED",
}


def callback(sender, data):

    global latest

    msg = data.hex()

    if msg.startswith("05004503"):

        latest = int(
            msg[-2:],
            16
        )


KEEPALIVE = bytes([
    0x05,
    0x00,
    0x01,
    0x01,
    0x00
])

ENABLE_MODE0 = bytes([
    0x0A,
    0x00,
    0x41,
    0x03,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x01
])


async def main():

    async with BleakClient(
        ADDRESS
    ) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            callback
        )

        await client.write_gatt_char(
            CHAR,
            ENABLE_MODE0,
            response=False
        )

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            print(
                f"RAW={latest:<4} "
                f"COLOR={COLOR_MAP.get(latest,'UNKNOWN')}"
            )

            await asyncio.sleep(
                0.2
            )


asyncio.run(main())