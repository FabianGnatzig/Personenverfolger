"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
from rplidar import RPLidar
from color_camera import ColorCamera


PORT_NAME = 'COM3'
DMAX = 4000
IMIN = 0
IMAX = 50


def test_lidar():
    """
    Test method for LIDAR
    """
    lidar = RPLidar("COM3")
    print(f"{lidar.get_info()}, {lidar.get_health()}")

    for i, scans in enumerate(lidar.iter_scans()):
        for measurement in scans:
            _, angle, distance = measurement
            print(angle, distance)

        if i > 10:
            break

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


def camera():
    """
    Camera
    """
    x = ColorCamera()
    x.run()


if __name__ == '__main__':
    camera()
