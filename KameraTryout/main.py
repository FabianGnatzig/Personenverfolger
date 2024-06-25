"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
import logging
import time
from threading import Thread
import RPi.GPIO as GPIO


from color_camera import ColorCamera
from custom_formatter import CustomFormatter
from lidar import Lidar

run = True

PORT_NAME = '/dev/ttyUSB0'
log = logging.getLogger("log")

lidar_sensor = Lidar(PORT_NAME)
lidar_thread = Thread(target=lidar_sensor.measurement)

camera_sensor = ColorCamera()
camera_thread = Thread(target=camera_sensor.run)


def main():
    """
    Main Function. Setups and function.
    :return:
    """
    setup_logging()
    start_gpio()
    start_threads()

    try:
        while run:
            lidar()
    except KeyboardInterrupt:
        close_threads()


def start_gpio():
    """
    GPIO pin setup.
    :return: None
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)

    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

    GPIO.output(25, False)
    GPIO.output(8, False)
    GPIO.output(7, False)

    GPIO.output(23, False)
    GPIO.output(24, False)


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


def lidar():
    """
    Method to run the LIDAR sensor.
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
    """
    Checks if the angles are nearby.
    :param cam_angle: The detected angle from the camera.
    :param lidar_angle: The detected angle from the lidar.
    :return: True if angles are nearby.
    """
    diff = abs(cam_angle- lidar_angle)
    if diff > 180:
        diff = 360 - diff
    if diff <= 5:
        return True

    return False


def drive():
    """
    Drives to the object. Faster if LIDAR and Cam are mapped.
    :return: None
    """
    if is_map_angle(camera_sensor.angle, lidar_sensor.target_measurements[0]):
        print("DRIVE TO LIDAR")
        set_message(camera_sensor.angle, lidar_sensor.target_measurements[1])
        return
    print("DRIVE TO CAMERA")
    set_message(camera_sensor.angle, lidar_sensor.target_measurements[1] / 2)


def set_message(angle, distance):
    """
    Sets the GPIO Pins for the incoming angle and distances.
    :param angle: The angle of the detected object.
    :param distance: The distance to the detected object.
    :return: None
    """
    print(angle, distance)
    if distance <= 300:
        GPIO.output(23, False)
        GPIO.output(24, False)

    elif 300 < distance <= 1000:
        GPIO.output(23, False)
        GPIO.output(24, True)

    elif 1000 < distance <= 5000:
        GPIO.output(23, True)
        GPIO.output(24, False)

    else:
        GPIO.output(23, True)
        GPIO.output(24, True)

    if 0 <= angle < 10 or 350 < angle <= 360:
        GPIO.output(25, False)
        GPIO.output(8, False)
        GPIO.output(7, True)

    elif 10 <= angle < 40:
        GPIO.output(25, True)
        GPIO.output(8, True)
        GPIO.output(7, False)

    elif 40 <= angle < 90:
        GPIO.output(25, True)
        GPIO.output(8, False)
        GPIO.output(7, False)

    elif 270 < angle <= 320:
        GPIO.output(25, False)
        GPIO.output(8, True)
        GPIO.output(7, True)

    elif 320 < angle <= 350:
        GPIO.output(25, True)
        GPIO.output(8, False)
        GPIO.output(7, True)

    else:
        GPIO.output(25, False)
        GPIO.output(8, False)
        GPIO.output(7, True)


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
