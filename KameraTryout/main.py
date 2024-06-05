"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
import logging
import time
from threading import Thread

from color_camera import ColorCamera
from custom_formatter import CustomFormatter
from lidar import Lidar
import matplotlib.pyplot as plt

import numpy as np

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

    lidar_thread = Thread(target=lidar_sensor.test_measurement)
    lidar_thread.start()

    i = 0

    try:

        while i < 6:
            log.info(f"Number of measurements {len(lidar_sensor.measurements)}")
            log.info(f"Number of angled measurements {len(lidar_sensor.target_measurements)}")

            distance_array = []

            log.info(f" WALL {lidar_sensor.wall_measurements}")

            if len(lidar_sensor.target_measurements):
                log.info(f"target = {lidar_sensor.target_measurements[0]}, distance: {lidar_sensor.target_measurements[1]}")

            # plt.show()

            time.sleep(2)
            i += 1

    except Exception as ex:
        print(ex)

    lidar_sensor.run = False
    lidar_thread.join()


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


def get_angle(first: float, second: float):
    """
    Get the angle between 315 and 45 degree.
    """
    midpoint = (first + second) / 2

    if abs(first - second) > 180:
        midpoint += 180

    return float


if __name__ == '__main__':
    main()
