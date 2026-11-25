import asyncio
from bleak import BleakClient

from neuroworm.brain.network import SimpleNetwork

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

MOTOR_ON = bytes([
    0x08,
    0x00,
    0x81,
    0x02,
    0x11,
    0x01,
    0x64,
    0x00
])

MOTOR_OFF = bytes([
    0x08,
    0x00,
    0x81,
    0x02,
    0x11,
    0x01,
    0x00,
    0x00
])

client_ref = None
motor_running = False

# Two-neuron network
brain = SimpleNetwork()


async def motor_on():
    await client_ref.write_gatt_char(
        CHAR,
        MOTOR_ON,
        response=False
    )


async def motor_off():
    await client_ref.write_gatt_char(
        CHAR,
        MOTOR_OFF,
        response=False
    )


def cb(sender, data):

    global motor_running

    msg = data.hex()

    if msg.startswith("05004503"):

        value = int(msg[-2:], 16)

        print("Sensor:", value)

        if value != 255:

            if brain.stimulate():

                print("NETWORK FIRED!")

                if not motor_running:

                    motor_running = True

                    asyncio.create_task(
                        motor_on()
                    )

        else:

            if motor_running:

                print("NO OBJECT -> MOTOR OFF")

                motor_running = False

                asyncio.create_task(
                    motor_off()
                )


async def main():

    global client_ref

    async with BleakClient(ADDRESS) as client:

        client_ref = client

        print("Connected")

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
            ENABLE_SENSOR_D,
            response=False
        )

        print("\nReflex V4 Running")
        print("Sensor -> Network -> Motor\n")

        while True:

            await client.write_gatt_char(
                CHAR,
                KEEPALIVE,
                response=False
            )

            await asyncio.sleep(2)


asyncio.run(main())