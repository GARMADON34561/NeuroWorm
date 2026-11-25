"""
NeuroWorm Motor Commands
========================

Current findings:

Port 0 = Internal Motor A (assumed)
Port 1 = Internal Motor B (assumed)
Port 2 = External Motor C (confirmed)
Port 3 = Sensor D

Verified command:

08 00 81 02 11 01 64 00

moves Motor C.
"""

def motor_command(port: int, speed: int):
    """
    Generate a motor command packet.

    port:
        0 = A
        1 = B
        2 = C

    speed:
        0-100
    """

    speed = max(0, min(100, speed))

    return bytes([
        0x08,
        0x00,
        0x81,
        port,
        0x11,
        0x01,
        speed,
        0x00
    ])


def motor_a(speed=100):
    return motor_command(0, speed)


def motor_b(speed=100):
    return motor_command(1, speed)


def motor_c(speed=100):
    return motor_command(2, speed)