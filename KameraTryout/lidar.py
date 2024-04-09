"""
Created by Fabian Gnatzig in 2024
Contact: fabiangnatzig@gmx.de
"""
import logging

from rplidar import RPLidar

log = logging.getLogger("log")


class Lidar:
    """
    Class for LIDAR-sensor.
    """

    def __init__(self, port: str):

        self._port = port
        try:
            self._sensor = RPLidar(port)
        except Exception as ex:
            print(ex)

    def test_mesurement(self):
        """
        Test method.
        """
        log.info(f"{self._sensor.get_info()}, {self._sensor.get_health()}")

        for i, scans in enumerate(self._sensor.iter_scans()):
            for measurement in scans:
                _, angle, distance = measurement
                print(angle, distance)

            if i > 10:
                break

        self._sensor.stop()
        self._sensor.stop_motor()
        self._sensor.disconnect()
