import asyncio
from bleak import BleakClient

ADDRESS = "00:16:53:B2:69:3B"
CHAR = "00001624-1212-efde-1623-785feabcd123"

async def main():

    async with BleakClient(ADDRESS) as client:

        print("Connected!")

        start = asyncio.get_event_loop().time()

        while True:

            try:

                data = await client.read_gatt_char(CHAR)

                print(
                    f"{asyncio.get_event_loop().time()-start:.1f}s",
                    data.hex()
                )

                await asyncio.sleep(1)

            except Exception as e:

                print("Disconnected:", e)
                break

asyncio.run(main())