from colorama import Fore
import cv2
import numpy as np

def configure_camera():
    # Define Color and Border
    g = 0
    b = 0
    r = 0

    lower = np.array([10, 10, 10], dtype="uint8")
    higher = np.array([g, b, r], dtype="uint8")

    while g < 223:
        b = 0
        while b < 223:
            r = 0
            while r < 223:
                # Set color borders to new value
                lower = np.array([g, b, r], dtype="uint8")
                higher = np.array([g + 32, b + 32, r + 32], dtype="uint8")

                # Get Image from Cam
                result, img = cam.read()

                # Create mask with color borers
                mask = cv2.inRange(img, lower, higher)

                # Find Contours
                cont, her = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for c in cont:
                    if cv2.contourArea(c) > 6000:
                        print(f"{g}{b}{r}.jpg")
                        cv2.drawContours(img, c, -1, (255, 0, 0), 3)
                        cv2.imshow(f"{g}{b}{r}.jpg", img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                r += 32
            b += 32
        g += 32


if __name__ == '__main__':

    # Define Camera
    cam = cv2.VideoCapture(0)

    print(Fore.GREEN, "##############################################################")
    print("WELCOME")
    print("##############################################################")
    print("Do you want to see the possible farbcodes and sizes? y/n")
    answare = input()

    if answare == "y":
        print("Configuration Startet")
        configure_camera()

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
        result, img = cam.read()

        mask = cv2.inRange(img, lower, higher)

        mask_cutout = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("Mask Cutout", mask_cutout)
        cv2.imshow("Mask", mask)
        a, b = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        (x1, y1, z) = img.shape
        x2, y2 = 0, 0

        for cnt in a:
            (x, y), z = cv2.minEnclosingCircle(cnt)
            x1 = x if x1 > x else x1
            y1 = y if y1 > y else y1
            x2 = x if x2 < x else x2
            y2 = y if y2 < y else y2

        start_point = int(x1), int(y1)
        end_point = int(x2), int(y2)

        print(f"Object at: {x1+(x2-x1)/2}; {y1+(y2-y1)/2}")

        item5 = cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)

        cv2.imshow("Image with Rect", img)

        cv2.waitKey(0)
