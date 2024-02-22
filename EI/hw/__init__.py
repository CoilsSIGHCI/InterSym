import os
import platform


def is_raspberry_pi():
    """Checks if the platform is a Raspberry Pi."""
    return all([
        'arm' in platform.uname().machine,
        os.path.exists('/dev/vchiq')
    ])
