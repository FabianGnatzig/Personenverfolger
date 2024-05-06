"""
Created by Fabian Gnatzig in 2024
Contact: fabiangnatzig@gmx.de
"""
import logging
import time

from rplidar import RPLidar
log = logging.getLogger("log")


class Lidar:
    """
    Class for LIDAR-sensor.
    """

    def __init__(self, port: str):
        self._port = port
        self._measurements = []
        self._angle_measurements = []
        self._run = True
        self._ready = False
        try:
            self._sensor = RPLidar(port)
        except Exception as ex:
            print(ex)

    def test_measurement(self):
        """
        Test method.
        """
        log.info(f"{self._sensor.get_info()}, {self._sensor.get_health()}")
        self._ready = True

        for i, scan in enumerate(self._sensor.iter_scans()):
            self._measurements = scan
            self.get_angle_measurements(scan)

            if not self._run:
                break

        self._sensor.stop()
        self._sensor.stop_motor()
        self._sensor.disconnect()

    def get_angle_measurements(self, measurements):
        angle_measurements = []
        for _, angle, distance in measurements:
            if 45 < angle < 315:
                continue

            angle_measurements.append((angle, distance))

        self._angle_measurements = angle_measurements

    @property
    def measurements(self):
        return self._measurements

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value: bool):
        self._run = value

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value: bool):
        self._ready = value

    @property
    def angle_measurements(self):
        return self._angle_measurements
