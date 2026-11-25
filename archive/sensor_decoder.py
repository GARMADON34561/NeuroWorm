def decode_sensor(packet):

    data = bytes.fromhex(packet)

    if len(data) != 5:
        return None

    if data[2] != 0x45:
        return None

    port = data[3]

    value = data[4]

    return (
        f"Port {port} "
        f"Value {value}"
    )