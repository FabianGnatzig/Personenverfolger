"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
import argparse

import cv2 as cv
import face_recognition
from rplidar import RPLidar
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from color_camera import ColorCamera

# from color_camera import ColorCamera

PORT_NAME = 'COM3'
DMAX = 4000
IMIN = 0
IMAX = 50


def test_lidar():
    lidar = RPLidar("COM3")
    print(lidar.get_info(), lidar.get_health())

    x = lidar.iter_scans()
    y = enumerate(x)

    for i, scans in enumerate(lidar.iter_scans()):
        print('\n%d: Got %d measurments' % (i, len(scans)))
        for measurement in scans:
            quality, angle, distance = measurement
            print(angle, distance)

        if i > 10:
            break

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


def camera():
    x = ColorCamera()
    x.run()


if __name__ == '__main__':
    camera()
