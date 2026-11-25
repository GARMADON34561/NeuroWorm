import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

COLOR_MAP = {
    0: "BLACK",
    5: "GREEN",
    7: "YELLOW",
    9: "RED",
    255: "NONE"
}

latest = 255


def callback(sender, data):

    global latest

    msg = data.hex()

    if msg.startswith("05004503"):

        latest = int(
            msg[-2:],
            16
        )


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


KEEPALIVE = bytes([
    0x05,
    0x00,
    0x01,
    0x01,
    0x00
])


async def main():

    async with BleakClient(
        ADDRESS
    ) as client:

        await client.start_notify(
            CHAR,
            callback
        )

        await client.write_gatt_char(
            CHAR,
            ENABLE_MODE0,
            response=False
        )

        print()
        print("Present colors.")
        print()

        while True:

            try:

                await client.write_gatt_char(
                    CHAR,
                    KEEPALIVE,
                    response=False
                )

                print(
                    latest,
                    "->",
                    COLOR_MAP.get(
                        latest,
                        "UNKNOWN"
                    )
                )

                await asyncio.sleep(
                    0.5
                )

            except KeyboardInterrupt:

                break


asyncio.run(main())