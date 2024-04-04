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

H_COLOR_BORDER = 360
S_COLOR_BORDER = 100
V_COLOR_BORDER = 100
BLUR = 15


NEW_REGION_STRING = "##############################################################"

# pylint: disable=no-member


class ColorCamera:
    """
    Camera class for color detection
    """

    def __init__(self):
        # Define Camera
        self.cam = cv2.VideoCapture(0)

        self.h, self.s, self.v = 0, 0, 0

        self.value = np.array([0, 0, 0])
        self.lower = np.array([0, 0, 0])
        self.higher = np.array([0, 0, 0])

        # Show Welcome
        print(Fore.GREEN, NEW_REGION_STRING)
        while True:
            print("WELCOME")
            print(NEW_REGION_STRING)
            print("How do you want to configure? y: see all pictures / ov: only insert values (skip config pictures)")
            answer = input()

            if answer == "y":
                print("Configuration Started")
                self.configure_camera()
                return

            elif answer == "ov":
                # Get values for filter
                h, s, v = self.get_input_values()
                self.set_color_range(h, s, v)
                return

    @staticmethod
    def find_color(config_img):
        hsv_img = cv2.cvtColor(config_img, cv2.COLOR_BGR2HSV)
        h, s, v = 0, 0, 0
        while h < H_COLOR_BORDER:
            s = 0
            while s < S_COLOR_BORDER:
                v = 0
                while v < V_COLOR_BORDER:
                    # Set color borders to new value
                    lower_start = np.array(
                        [h, s, v]
                    )
                    higher_start = np.array(
                        [h + 20, s + 25, v + 25]
                    )

                    # Create mask with color borers
                    config_mask = cv2.inRange(hsv_img, lower_start, higher_start)
                    config_mask = cv2.blur(config_mask, (BLUR, BLUR))

                    # Find Contours
                    config_contours, _ = cv2.findContours(
                        config_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                    )

                    # Find big area and show it
                    for contour in config_contours:
                        if cv2.contourArea(contour) > 100:
                            cv2.drawContours(hsv_img, contour, -1, (255, 0, 0), 3)
                            continue

                    mask_img = cv2.bitwise_and(config_img, config_img, mask=config_mask)
                    horizontal_stack = np.hstack((config_img, mask_img))

                    cv2.imshow(f"H:{h}; S:{s}; V:{v}", horizontal_stack)
                    pressed_key = cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    if pressed_key == 27:
                        return

                    v += 25
                s += 25
            h += 20

    @staticmethod
    def get_input_values():
        while True:
            print(NEW_REGION_STRING)
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
                print(f"NOT ALL VALUES ARE INTEGERS: {e}")

    def configure_camera(self):
        """
        A function to configure the camera
        :return: None
        """
        # Get Image from Cam
        # pylint: disable=used-before-assignment
        _, config_img = self.cam.read()
        self.find_color(config_img)
        h, s, v = self.get_input_values()
        self.set_color_range(h, s, v)

    def set_color_range(self, h: int, s: int, v: int):
        """
        Converts the string parameters to int and set them.
        :param h: The red value parameter.
        :param s: The green value parameter.
        :param v: The blue value parameter.
        :return: None
        """
        self.h, self.s, self.v = h, s, v
        print(f"Your selected base-color is {self.h}/{self.s}/{self.v}")
        print(NEW_REGION_STRING)
        self.value = np.array([self.h, self.s, self.v])
        self.lower = self.value
        self.higher = self.value + np.array([20, 25, 25])

    def run(self):
        """
        Runs the program as long as no KeyborExeption.
        :return: None
        """

        while True:
            _, img = self.cam.read()
            original_img = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Create Mask
            mask = cv2.inRange(img, self.lower, self.higher)
            mask = cv2.blur(mask, (BLUR, BLUR))
            mask_cutout = cv2.bitwise_and(img, img, mask=mask)

            start_point, end_point, position = self.rectangle_from_mask(mask)

            print(f"Object at: {position}")

            x_value = position[0]
            img_width = img.shape[1]
            step = img_width / 90
            angle = x_value / step - 45
            print(f"Angle == {angle}")

            print(self.get_direction(position, mask.shape))

            # draw the rectangle
            cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)

            converted_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

            h1_stack = np.hstack((original_img, img))
            h2_stack = np.hstack((mask_cutout, converted_mask))
            v_stack = np.vstack((h1_stack, h2_stack))

            cv2.imshow("Image with Rectangle", v_stack)

            pressed_key = cv2.waitKey(0)

            if pressed_key == 27:
                print("Finished")
                return

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
            position = start_point[0] + (end_point[0] - start_point[0]) / 2, start_point[1] + (end_point[1] - start_point[1]) / 2
            return start_point, end_point, position

        return (0, 0), (1, 1), (0, 0)
