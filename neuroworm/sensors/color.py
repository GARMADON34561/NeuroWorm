COLOR_MAP = {

    255: "NONE",

    0: "BLACK",

    5: "GREEN",

    7: "YELLOW",

    9: "RED",
}


def notification_handler(sender, data):

    msg = data.hex()

    if msg.startswith("05004503"):

        val = int(
            msg[-2:],
            16
        )

        print(
            f"{val} -> "
            f"{COLOR_MAP.get(val, 'UNKNOWN')}"
        )