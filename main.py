"""
Main module to start the programm.
"""

from time import sleep
from picamera2 import Picamera2, Preview # pylint: disable=import-error

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
print(camera_config)
picam2.configure(camera_config)
picam2.start()
picam2.start_preview(Preview.QT)
sleep(2)
picam2.capture_file("test.jpg")
picam2.stop_preview()
print("HelloWorld")
