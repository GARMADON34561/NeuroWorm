import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"

CHAR = "00001624-1212-efde-1623-785feabcd123"

packets = []

def callback(sender, data):

    msg = data.hex()

    packets.append(msg)

    print(msg)

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            callback
        )

        await asyncio.sleep(15)

        print("\n------------")
        print("PACKET COUNT:", len(packets))

asyncio.run(main())