import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

KEEPALIVE = bytes([
    0x05, 0x00, 0x01, 0x01, 0x00
])

def cb(sender, data):

    msg = data.hex()

    if msg != "0500050105":
        print(msg)

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            cb
        )

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            await asyncio.sleep(2)

asyncio.run(main())