"""
Created by Fabian Gnatzig in 2024
Contact: fabiangnatzig@gmx.de
"""
import logging
import time

import numpy as np
from rplidar import RPLidar
log = logging.getLogger("log")

WALL_ANGLE_DELTA = 1.5


class Lidar:
    """
    Class for LIDAR-sensor.
    """

    def __init__(self, port: str):
        self._port = port
        self._measurements = []
        self._target_measurements = []
        self._wall_measurements = {"0": None,
                                   "45": None,
                                   "90": None,
                                   "135": None,
                                   "180": None,
                                   "225": None,
                                   "270": None,
                                   "315": None}
        self._run = True
        self._ready = False
        try:
            self._sensor = RPLidar(port)
        except Exception as ex:
            print(ex)

    def measurement(self):
        """
        Measures the object from the LIDAR sensor.
        :return: None
        """
        log.info(f"{self._sensor.get_info()}, {self._sensor.get_health()}")
        self._ready = True

        for i, scan in enumerate(self._sensor.iter_scans(scan_type='express')):
            self._measurements = scan
            self.get_target_angle_measurements(scan)
            self.get_wall_measurements(scan)

            if not self._run:
                break

        self._sensor.stop()
        self._sensor.stop_motor()
        self._sensor.disconnect()

    def get_target_angle_measurements(self, measurements):
        """
        Get the angle and the distance of the specific target.
        :param measurements: The measurements of the last LIDAR-scan.
        :return: None
        """
        target_measurements = []
        small = []
        big = []

        target = (0, None)

        for _, angle, distance in measurements:
            if 45 < angle < 315:
                continue

            if angle <= 45:
                small.append((angle, distance))
            else:
                big.append((angle, distance))

        small.sort()
        big.sort()

        target_measurements.extend(big)
        target_measurements.extend(small)

        if target_measurements:
            distance_values = []
            for angle, distance in target_measurements:
                distance_values.append(distance)

            diff_distance = np.diff(distance_values)
            detected_borders = np.where(np.abs(diff_distance) > 75)[0]
            detected_angles = []
            detected_distances = []

            for value in detected_borders:
                detected_angles.append(target_measurements[value][0])
                detected_distances.append(target_measurements[value][1])

            if len(detected_angles) == 2:
                target = self.get_angle(detected_angles[0], detected_angles[1]), sum(detected_distances)/len(detected_distances)

            elif len(detected_angles) > 2:
                target = self.get_angle(detected_angles[0], detected_angles[-1]),sum(detected_distances)/len(detected_distances)

            elif len(detected_angles) == 0:
                target = 0, None

            else:
                target = detected_angles[0], detected_distances[0]

        self._target_measurements = target

    def get_wall_measurements(self, measurements):
        """
        Sets the wall measurements for specific angles.
        :param measurements: The measurements of the last LIDAR-scan.
        :return: None
        """
        for _, angle, distance in measurements:
            if 360 - WALL_ANGLE_DELTA >= angle <= 0 + WALL_ANGLE_DELTA:
                self._wall_measurements["0"] = distance
            elif 45 - WALL_ANGLE_DELTA <= angle <= 45 + WALL_ANGLE_DELTA:
                self._wall_measurements["45"] = distance
            elif 90 - WALL_ANGLE_DELTA <= angle <= 90 + WALL_ANGLE_DELTA:
                self._wall_measurements["90"] = distance
            elif 135 - WALL_ANGLE_DELTA <= angle <= 135 + WALL_ANGLE_DELTA:
                self._wall_measurements["135"] = distance
            elif 180 - WALL_ANGLE_DELTA <= angle <= 180 + WALL_ANGLE_DELTA:
                self._wall_measurements["180"] = distance
            elif 225 - WALL_ANGLE_DELTA <= angle <= 225 + WALL_ANGLE_DELTA:
                self._wall_measurements["225"] = distance
            elif 270 - WALL_ANGLE_DELTA <= angle <= 270 + WALL_ANGLE_DELTA:
                self._wall_measurements["270"] = distance
            elif 315 - WALL_ANGLE_DELTA <= angle <= 315 + WALL_ANGLE_DELTA:
                self._wall_measurements["315"] = distance

    @property
    def measurements(self):
        """
        Returns the measurement property.
        :return: The measurement property.
        """
        return self._measurements

    @property
    def run(self):
        """
        Returns the run value.
        :return: The run value.
        """
        return self._run

    @run.setter
    def run(self, value: bool):
        """
        Sets the run value.
        :param value: The new run value.
        :return: None
        """
        self._run = value

    @property
    def ready(self):
        """
        Returns the ready value.
        :return: The ready value.
        """
        return self._ready

    @ready.setter
    def ready(self, value: bool):
        """
        Sets the ready value.
        :param value: The new ready value.
        :return: None
        """
        self._ready = value

    @property
    def target_measurements(self):
        """
        Returns the target measurement property.
        :return: The target measurement property.
        """
        return self._target_measurements

    @property
    def wall_measurements(self):
        """
        Returns the wall measurements property.
        :return: The wall measurements property.
        """
        return self._wall_measurements

    @staticmethod
    def get_angle(first: float, second: float):
        """
        Get the angle between 315 and 45 degree.
        @param first: First angle.
        @param second: Second angle.
        @return: The angle between.
        """
        midpoint = (first + second) / 2

        if abs(first - second) > 180:
            midpoint += 180

        return midpoint
