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

run = True

PORT_NAME = 'COM3'
log = logging.getLogger("log")

lidar_sensor = Lidar(PORT_NAME)
lidar_thread = Thread(target=lidar_sensor.measurement)

camera_sensor = ColorCamera()
camera_thread = Thread(target=camera_sensor.run)


def main():
    setup_logging()
    start_threads()

    try:
        while run:
            test_lidar()
    except KeyboardInterrupt:
        close_threads()


def start_threads():
    """
    Starting threads
    """
    lidar_thread.start()
    camera_thread.start()


def close_threads():
    """
    Closing the threads.
    """
    lidar_sensor.run = False
    camera_sensor.stop()

    lidar_thread.join()
    camera_thread.join()

    print("Stopped")


def test_lidar():
    """
    Test method for LIDAR
    """

    try:

        log.info(f"Number of measurements {len(lidar_sensor.measurements)}")
        log.info(f"Number of angled measurements {len(lidar_sensor.target_measurements)}")

        log.info(f" WALL {lidar_sensor.wall_measurements}")

        if len(lidar_sensor.target_measurements):
            log.info(f"target = {lidar_sensor.target_measurements[0]}, distance: {lidar_sensor.target_measurements[1]}")

            drive()

        time.sleep(2)

    except Exception as ex:
        print(ex)


def is_map_angle(cam_angle: float, lidar_angle: float):
    diff = abs(cam_angle- lidar_angle)
    if diff > 180:
        diff = 360 - diff
    if diff <= 5:
        return True

    return False


def drive():
    if is_map_angle(camera_sensor.angle, lidar_sensor.target_measurements[0]):
        #ToDo: Drive to DISTANCE_LIDAR
        print("DRIVE TO X")
        return

    #ToDO: Drive to Camera Angle


def set_message(angle, distance):
    pass


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
