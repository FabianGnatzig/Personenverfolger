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

    while i < 4:
        log.info(f"Number of measurements {len(lidar_sensor.measurements)}")
        log.info(f"Number of angled measurements {len(lidar_sensor.angle_measurements)}")

        distance_array = []

        for (angle, distance) in lidar_sensor.angle_measurements:
            log.info(f"{angle}, {distance}")
            distance_array.append(distance)

        plt.plot(lidar_sensor.angle_measurements)

        if lidar_sensor.angle_measurements:
            print("YEET", distance_array)
            plt.plot(np.diff(distance_array))

        plt.show()

        time.sleep(0.5)
        i += 1


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


if __name__ == '__main__':
    main()
