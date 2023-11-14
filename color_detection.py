
"""
Detects the position of an object
"""

import cv2
import numpy as np

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)

    start_point = (5, 5)
    end_point = (100, 100)
    color = (0, 0, 255)
    color2 = (0, 0, 0)
    lower = np.array([80, 10, 10], dtype="uint8")
    higher = np.array([255, 40, 40], dtype="uint8")

    while True:

        result, img = cam.read()
        #item = cv2.rectangle(img, start_point, end_point, color, 2)
        test2 = cv2.imread("test.png")
        mask = cv2.inRange(img, lower, higher)

        test2 = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("testdEc", test2)
        cv2.imshow("testdEc2", mask)
        a, b = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(a)
        cv2.drawContours(img, a, -1, (0,255,0), 3)
        #cv2.imshow("TESTC", img)

        (x1, y1, z) = img.shape
        x2, y2 = 0, 0

        print(img.shape)
        #print(x1, y1, x2, y2)

        for cnt in a:
            (x, y), z = cv2.minEnclosingCircle(cnt)
            x1 = x if x1 > x else x1
            y1 = y if y1 > y else y1
            x2 = x if x2 < x else x2
            y2 = y if y2 < y else y2

        print(x1, y1, x2, y2)
        start_point = int(x1), int(y1)
        end_point = int(x2), int(y2)

        item5 = cv2.rectangle(img, start_point, end_point, color, 2)

        cv2.imshow("Test", img)

        cv2.waitKey(0)
