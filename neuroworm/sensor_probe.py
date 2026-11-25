import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])

client = None


def notification_handler(sender, data):

    print(
        f"RX: {data.hex()}"
    )


def sensor_mode_packet(mode):

    return bytes([
        0x0A,
        0x00,
        0x41,
        0x03,
        0x00,
        mode,
        0x00,
        0x00,
        0x00,
        0x01
    ])


async def keepalive_loop():

    while True:

        try:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

        except Exception:
            return

        await asyncio.sleep(2)


async def main():

    global client

    async with BleakClient(
        ADDRESS
    ) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            notification_handler
        )

        asyncio.create_task(
            keepalive_loop()
        )

        for mode in range(0, 11):

            print()
            print("=" * 60)
            print(f"TESTING MODE {mode}")
            print("=" * 60)

            await client.write_gatt_char(
                CHAR,
                sensor_mode_packet(mode),
                response=False
            )

            print(
                "Show colors/objects now..."
            )

            await asyncio.sleep(20)

        print("\nDONE")


asyncio.run(main())