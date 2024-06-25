"""
Created for project "Personenverfolger" for DHBW Heidenheim

Created by Fabian Gnatzig in 2023
Contact: fabiangnatzig@gmx.de
"""
from __future__ import annotations

import logging

import cv2
import numpy as np
from colorama import Fore
from constants import Constants

log = logging.getLogger("log")


# pylint: disable = no-member


class ColorCamera:
    """
    Camera class for color detection
    """

    def __init__(self):
        # Define Camera
        self._cam = cv2.VideoCapture(0)
        self._h, self._s, self._v = 0, 0, 0
        self._lower = Constants.NULL_ARRAY
        self._higher = Constants.NULL_ARRAY
        self._angle = 360.0
        self._run = True

        # Show Welcome
        print(Fore.GREEN, Constants.NEW_REGION_STRING)
        while True:
            print("WELCOME")
            print(Constants.NEW_REGION_STRING)
            print("How do you want to configure? y: see all pictures /"
                  " ov: only insert values (skip config pictures)")
            answer = input()

            if answer == "y":
                print("Configuration Started")
                self._configure_camera()
                return

            if answer == "ov":
                # Get values for filter
                h, s, v = self._get_input_values()
                self._set_color_range(h, s, v)
                return

    @staticmethod
    def _find_color(config_img):
        """
        Find the right color inside the image.
        """
        hsv_img = cv2.cvtColor(config_img, cv2.COLOR_BGR2HSV)
        h, s, v = 0, 0, 0
        while h < Constants.H_COLOR_BORDER:
            s = 0
            while s < Constants.S_COLOR_BORDER:
                v = 0
                while v < Constants.V_COLOR_BORDER:
                    # Set color borders to new value
                    lower_start = np.array([h, s, v])
                    higher_start = lower_start + np.array(
                        [Constants.H_STEP, Constants.S_STEP, Constants.V_STEP]
                    )

                    # Create mask with color borers
                    config_mask = cv2.inRange(hsv_img, lower_start, higher_start)
                    config_mask = cv2.blur(config_mask, (Constants.BLUR, Constants.BLUR))

                    contours = cv2.findContours(config_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    if contours == ((), None):
                        log.debug(f"H:{h}; S:{s}; V:{v} has no contours")
                        v += Constants.V_STEP
                        continue

                    mask_img = cv2.bitwise_and(config_img, config_img, mask=config_mask)
                    horizontal_stack = np.hstack((config_img, mask_img))

                    cv2.imshow(f"H:{h}; S:{s}; V:{v}", horizontal_stack)
                    pressed_key = cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    if pressed_key == Constants.ESC_KEY:
                        return

                    if pressed_key == Constants.ENTER_KEY:
                        log.info(f"H:{h}, S: {s},V: {v}")
                        return

                    v += Constants.V_STEP
                s += Constants.S_STEP
            h += Constants.H_STEP

    @staticmethod
    def _get_input_values():
        """
        Static method to get the color values from user
        """
        while True:
            print(Constants.NEW_REGION_STRING)
            print("Please input Values")
            print("h:")
            h = input()
            print("s:")
            s = input()
            print("v:")
            v = input()

            try:
                return int(h), int(s), int(v)
            except ValueError as e:
                log.error(f"NOT ALL VALUES ARE INTEGERS: {e}")

    def _configure_camera(self):
        """
        A function to configure the camera
        :return: None
        """
        # Get Image from Cam
        # pylint: disable=used-before-assignment
        _, config_img = self._cam.read()
        self._find_color(config_img)
        h, s, v = self._get_input_values()
        self._set_color_range(h, s, v)

    def _set_color_range(self, h: int, s: int, v: int):
        """
        Converts the string parameters to int and set them.
        :param h: The red value parameter.
        :param s: The green value parameter.
        :param v: The blue value parameter.
        :return: None
        """
        self._h, self._s, self._v = h, s, v
        log.info(f"Your selected base-color is {self._h}/{self._s}/{self._v}")
        self._lower = np.array([self._h, self._s, self._v])
        self._higher = self._lower + np.array([Constants.H_STEP, Constants.S_STEP, Constants.V_STEP])

    def run(self):
        """
        Runs the program as long as no KeybordExeption.
        :return: None
        """
        log.info(f"Parameters: {self._lower}, {self._higher}")

        while self._run:
            _, img = self._cam.read()
            original_img = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Create Mask
            mask = cv2.inRange(img, self._lower, self._higher)
            mask = cv2.blur(mask, (Constants.BLUR, Constants.BLUR))
            mask_cutout = cv2.bitwise_and(img, img, mask=mask)

            start_point, end_point, position = self._rectangle_from_mask(mask)

            if position:
                #log.info(f"Object at: {position}")

                x_value = position[0]
                img_width = img.shape[1]
                step = img_width / 90
                angle = x_value / step - 45
                if angle < 0:
                    angle += 360
                self._angle = angle

                #log.info(f"Angle: {angle}")
                cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
            else:
                pass
                #log.info(f"Object not found; Last Angle: {self._angle}")
            converted_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            v_stack = np.vstack((np.hstack((original_img, img)),
                                 np.hstack((mask_cutout, converted_mask))))
            cv2.imshow("Image with Rectangle", v_stack)
            # pressed_key = cv2.waitKey(0)

            if cv2.waitKey(1) == Constants.ESC_KEY:
                log.info("Finished")
                return

    @staticmethod
    def _rectangle_from_mask(mask: cv2.Mat) -> tuple:
        """
        Returns a rectangle on size of the existing mask.
        :param mask: The mask of the image.
        :return: The start and endpoint of the rectangle.
        """
        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Set max size of rectangle
        biggest_area = -1
        biggest = None
        for con in contours:
            area = cv2.contourArea(con)
            if biggest_area < area:
                biggest_area = area
                biggest = con

        if biggest is not None:
            start_point = biggest.min(axis=0)[0]
            end_point = biggest.max(axis=0)[0]
            position = (start_point[0] + (end_point[0] - start_point[0]) / 2,
                        start_point[1] + (end_point[1] - start_point[1]) / 2)
            return start_point, end_point, position

        return None, None, None

    @property
    def angle(self):
        """
        Retruns the angle property.
        :return: The angle property.
        """
        return self._angle

    def stop(self):
        """
        Stops the run method.
        """
        self._run = False