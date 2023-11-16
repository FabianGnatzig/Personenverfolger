"""
The test module to check for color detection
"""

# pylint: disable=no-member

from colorama import Fore
import cv2
import numpy as np


def configure_camera():
    """
    A function to configure the camera
    :return:
    """
    # Define Color and Border
    g_config, b_config, r_config = 0, 0, 0

    lower_start = np.array([10, 10, 10], dtype="uint8")
    higher_start = np.array([g_config, b_config, r_config], dtype="uint8")

    # Get Image from Cam
    # pylint: disable=used-before-assignment
    _, config_img = cam.read()

    while g_config < 223:
        b_config = 0
        while b_config < 223:
            r_config = 0
            while r_config < 223:
                # Set color borders to new value
                lower_start = np.array([g_config, b_config, r_config], dtype="uint8")
                higher_start = np.array(
                    [g_config + 32, b_config + 32, r_config + 32], dtype="uint8"
                )

                # Create mask with color borers
                config_mask = cv2.inRange(config_img, lower_start, higher_start)

                # Find Contours
                config_contours, _ = cv2.findContours(
                    config_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                )

                # Find big area and show it
                for contour in config_contours:
                    if cv2.contourArea(contour) > 6000:
                        print(f"{g_config}{b_config}{r_config}.jpg")
                        cv2.drawContours(config_img, contour, -1, (255, 0, 0), 3)
                        cv2.imshow(f"{g_config}{b_config}{r_config}.jpg", config_img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                r_config += 32
            b_config += 32
        g_config += 32


if __name__ == '__main__':

    # Define Camera
    cam = cv2.VideoCapture(0)

    # Show Welcome
    print(Fore.GREEN, "##############################################################")
    print("WELCOME")
    print("##############################################################")
    print("Do you want to see the possible farbcodes and sizes? y/n")
    answer = input()

    if answer == "y":
        print("Configuration Startet")
        configure_camera()

    # Get values for filter
    print(Fore.GREEN, "##############################################################")
    print("Please input Values")
    print("g:")
    g = int(input())
    print("b:")
    b = int(input())
    print("r:")
    r = int(input())
    print(Fore.MAGENTA, f"Your selected base-color is {g}/{b}/{r}")
    print(Fore.GREEN, "##############################################################")

    lower = np.array([g, b, r], dtype="uint8")
    higher = lower + np.array([32, 32, 32], dtype="uint8")

    while True:
        _, img = cam.read()

        # Create Mask
        mask = cv2.inRange(img, lower, higher)
        mask_cutout = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("Mask Cutout", mask_cutout)
        cv2.imshow("Mask", mask)

        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Set max size of rectangle
        (x1, y1, z) = img.shape
        x2, y2 = 0, 0

        # Get size of rectangle
        for cnt in contours:
            (x, y), z = cv2.minEnclosingCircle(cnt)
            x1 = x if x1 > x else x1
            y1 = y if y1 > y else y1
            x2 = x if x2 < x else x2
            y2 = y if y2 < y else y2

        start_point = int(x1), int(y1)
        end_point = int(x2), int(y2)

        print(f"Object at: {x1+(x2-x1)/2}; {y1+(y2-y1)/2}")

        #raw the rectangle
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)

        cv2.imshow("Image with Rect", img)

        cv2.waitKey(0)
