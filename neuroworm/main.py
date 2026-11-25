import asyncio
from bleak import BleakClient
from brain.behavior import (
    choose_behavior
)

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

client = None
latest_sensor = 255


def notification_handler(sender, data):

    global latest_sensor

    msg = data.hex()

    if msg.startswith("05004503"):
        latest_sensor = int(
            msg[-2:],
            16
        )


def motor(port, speed):

    return bytes([
        0x08,
        0x00,
        0x81,
        port,
        0x11,
        0x01,
        speed & 0xFF,
        0x00
    ])


async def keepalive_loop():

    while True:

        await client.write_gatt_char(
            CHAR,
            KEEPALIVE,
            response=False
        )

        await asyncio.sleep(2)


# --------------------
# TRACK CONTROL
# --------------------

async def stop_tracks():

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 0),
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 0),
        response=False
    )


async def move_forward():

    print("ACTION = FORWARD")

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 40),
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 40),
        response=False
    )

    await asyncio.sleep(0.8)

    await stop_tracks()

async def move_backward():

    print("ACTION = BACKWARD")

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 216),   # Right track reverse
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 216),   # Left track reverse
        response=False
    )

    await asyncio.sleep(0.6)

    await stop_tracks()

async def turn_around():

    print("ACTION = TURN AROUND")

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 40),
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 216),
        response=False
    )

    await asyncio.sleep(1.4)

    await stop_tracks()


async def turn_left():

    print("ACTION = TURN LEFT")

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 40),
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 0),
        response=False
    )

    await asyncio.sleep(0.6)

    await stop_tracks()


async def turn_right():

    print("ACTION = TURN RIGHT")

    await client.write_gatt_char(
        CHAR,
        motor(0x00, 0),
        response=False
    )

    await client.write_gatt_char(
        CHAR,
        motor(0x01, 40),
        response=False
    )

    await asyncio.sleep(0.6)

    await stop_tracks()


# --------------------
# NECK CONTROL
# --------------------

async def neck_left():

    print("\nLOOK LEFT")

    await client.write_gatt_char(
        CHAR,
        motor(0x02, 216),
        response=False
    )

    await asyncio.sleep(0.25)

    await client.write_gatt_char(
        CHAR,
        motor(0x02, 0),
        response=False
    )


async def neck_right():

    print("\nLOOK RIGHT")

    await client.write_gatt_char(
        CHAR,
        motor(0x02, 40),
        response=False
    )

    await asyncio.sleep(0.25)

    await client.write_gatt_char(
        CHAR,
        motor(0x02, 0),
        response=False
    )


# --------------------
# SENSOR
# --------------------

async def sample_sensor():

    values = []

    for _ in range(20):

        values.append(
            latest_sensor
        )

        await asyncio.sleep(0.05)

    meaningful = [
        v for v in values
        if v != 255
    ]

    if meaningful:

        value = min(meaningful)

    else:

        value = 255

    print(
        f"RAW={values}"
    )

    print(
        f"SENSOR={value}"
    )

    return value


# --------------------
# SCAN
# --------------------

async def scan_environment():

    # Assume robot starts near left

    left = await sample_sensor()

    await neck_right()

    right = await sample_sensor()

    await neck_left()

    print()

    print(
        f"LEFT={left} | RIGHT={right}"
    )

    print("-" * 40)

    return {
        "left": left,
        "right": right
    }


# --------------------
# BRAIN
# --------------------

def classify_stimulus(value):

    if value == 255:
        return "NONE"

    if value == 0:
        return "STRONG"

    return "WEAK"

async def execute(behavior):

    print(
        f"BEHAVIOR={behavior}"
    )

    if behavior == "ESCAPE":

        await move_backward()
        await turn_around()

    elif behavior == "AVOID":

        await move_backward()
        await turn_right()

    elif behavior == "INVESTIGATE":

        await turn_right()

    elif behavior == "EXPLORE":

        await move_forward()

    else:

        print(
            "UNKNOWN BEHAVIOR"
        )

# --------------------
# MAIN
# --------------------

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

        await client.write_gatt_char(
            CHAR,
            ENABLE_SENSOR_D,
            response=False
        )

        asyncio.create_task(
            keepalive_loop()
        )

        await asyncio.sleep(1)

        while True:
            scan = await scan_environment()

            left_state = classify_stimulus(
                scan["left"]
            )

            right_state = classify_stimulus(
                scan["right"]
            )

            behavior = choose_behavior(
                left_state,
                right_state
            )

            print(
                f"BEHAVIOR={behavior}"
            )

            await execute(
                behavior
            )

            await asyncio.sleep(1)


asyncio.run(main())