"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
import logging

from color_camera import ColorCamera
from custom_formatter import CustomFormatter
from lidar import Lidar

PORT_NAME = 'COM3'
log = logging.getLogger("log")


def main():
    setup_logging()
    #camera()
    lidar()


def lidar():
    """
    Test method for LIDAR
    """
    lidar_sensor = Lidar(PORT_NAME)
    lidar_sensor.test_measurement()


def camera():
    """
    Camera
    """
    x = ColorCamera()
    x.run()


def setup_logging():
    """
    Setup th logging.
    """
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    log.addHandler(ch)


if __name__ == '__main__':
    main()
