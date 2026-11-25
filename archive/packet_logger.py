# packet_logger.py

import asyncio
import time
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

start = None

def callback(sender, data):
    global start

    if start is None:
        start = time.time()

    print(
        f"{time.time()-start:.3f}s",
        data.hex()
    )

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected")

        await client.start_notify(
            CHAR,
            callback
        )

        await asyncio.sleep(20)

asyncio.run(main())