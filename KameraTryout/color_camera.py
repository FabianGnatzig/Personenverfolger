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

MAX_COLOR_RANGE = 255

NEW_REGION_STRING = "##############################################################"

# pylint: disable=no-member

class ColorCamera:
    """
    Camera class for color detection
    """

    def __init__(self):
        # Define Camera
        self.cam = cv2.VideoCapture(0)

        self.g, self.b, self.r = 0, 0, 0

        self.lower = np.array([self.g, self.b, self.r])
        self.higher = np.array([self.g, self.b, self.r])

        # Show Welcome
        print(Fore.GREEN, NEW_REGION_STRING)
        print("WELCOME")
        print(NEW_REGION_STRING)
        print("Do you want to see the possible farbcodes and sizes? y/n/ov")
        answer = input()
        if answer == "y":
            print("Configuration Started")
            self.configure_camera()

        elif answer == "ov":
            # Get values for filter
            print(NEW_REGION_STRING)
            print("Please input Values")
            print("g:")
            g = input()
            print("b:")
            b = input()
            print("r:")
            r = input()
            self.set_color_range(r, g, b)

    def configure_camera(self):
        """
        A function to configure the camera
        :return: None
        """
        # Define Color and Border
        g_config, b_config, r_config = 0, 0, 0

        # Get Image from Cam
        # pylint: disable=used-before-assignment
        _, config_img = self.cam.read()

        while g_config < MAX_COLOR_RANGE:
            b_config = 0
            while b_config < MAX_COLOR_RANGE:
                r_config = 0
                while r_config < MAX_COLOR_RANGE:
                    # Set color borders to new value
                    lower_start = np.array([g_config, b_config, r_config])
                    higher_start = np.array(
                        [g_config + 32, b_config + 32, r_config + 32]
                    )

                    # Create mask with color borers
                    config_mask = cv2.inRange(config_img, lower_start, higher_start)

                    # Find Contours
                    config_contours, _ = cv2.findContours(
                        config_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                    )

                    # Find big area and show it
                    for contour in config_contours:
                        if cv2.contourArea(contour) > 100:
                            print(f"{g_config}{b_config}{r_config}.jpg")
                            cv2.drawContours(config_img, contour, -1, (255, 0, 0), 3)
                            cv2.imshow(f"{g_config}{b_config}{r_config}.jpg", config_img)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            continue
                    r_config += 32
                b_config += 32
            g_config += 32

        # Get values for filter
        print(NEW_REGION_STRING)
        print("Please input Values")
        print("g:")
        g = input()
        print("b:")
        b = input()
        print("r:")
        r = input()

        self.set_color_range(r, g, b)

    def set_color_range(self, red: str, green: str, blue: str):
        """
        Converts the string parameters to int and set them.
        :param red: The red value parameter.
        :param green: The green value parameter.
        :param blue: The blue value parameter.
        :return: None
        """
        try:
            self.g, self.r, self.b = int(green), int(red), int(blue)

        except TypeError as e:
            logging.error(e)
            self.g, self.b, self.r = 0, 0, 0

        print(f"Your selected base-color is {self.g}/{self.b}/{self.r}")
        print(NEW_REGION_STRING)

        self.lower = np.array([self.g, self.b, self.r])
        self.higher = self.lower + np.array([32, 32, 32])

    def run(self):
        """
        Runs the program as long as no KeyborExeption.
        :return: None
        """
        try:
            while True:
                _, img = self.cam.read()

                # Create Mask
                mask = cv2.inRange(img, self.lower, self.higher)
                mask_cutout = cv2.bitwise_and(img, img, mask=mask)
                cv2.imshow("Mask Cutout", mask_cutout)
                cv2.imshow("Mask", mask)

                start_point, end_point, position = self.rectangle_from_mask(mask)

                print(f"Object at: {position}")
                print(self.get_direction(position, mask.shape))

                # draw the rectangle
                cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)

                cv2.imshow("Image with Rect", img)

                cv2.waitKey(0)
        except KeyboardInterrupt:
            print("FINISHED")

    @staticmethod
    def get_direction(position: tuple, size: tuple):
        """
        Prints the direction to move to.
        :param position: The position of the object.
        :param size: The size of the image.
        :return: The direction to move to.
        """
        object_x, _ = position
        _, size_x = size

        if object_x > size_x * 2/3:
            return "right"
        if object_x < size_x * 1/3:
            return "left"
        return "straight"

    @staticmethod
    def rectangle_from_mask(mask: cv2.Mat) -> tuple:
        """
        Returns a rectangle on size of the existing mask.
        :param mask: The mask of the image.
        :return: The start and endpoint of the rectangle.
        """
        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Set max size of rectangle
        (y1, x1) = mask.shape
        x2, y2 = 0, 0

        # Get size of rectangle
        for cnt in contours:
            (x, y), _ = cv2.minEnclosingCircle(cnt)
            x1 = x if x1 > x else x1
            y1 = y if y1 > y else y1
            x2 = x if x2 < x else x2
            y2 = y if y2 < y else y2

        start_point = int(x1), int(y1)
        end_point = int(x2), int(y2)
        position = x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2
        return start_point, end_point, position
