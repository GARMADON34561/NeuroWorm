# neuroworm/ble/keepalive.py

"""
Session maintenance packet discovered experimentally.

Observations:
- Without periodic transmission:
    Hub disconnects after ~7 seconds.

- Sending KEEPALIVE every 2 seconds:
    Hub remains connected indefinitely.

- Hub responds with:
    0500050105
"""

KEEPALIVE = bytes([
    0x05,
    0x00,
    0x01,
    0x01,
    0x00
])

KEEPALIVE_RESPONSE = "0500050105"