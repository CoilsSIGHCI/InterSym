# get image stream from raspberry pi camera

import cv2
from picamera2 import Picamera2, Preview
import time

from fastsam import FastSAM, FastSAMPrompt


framePath = "/tmp/frame.png"
modelPath = "./checkpoints/FastSAM-x.pt"
DEVICE = "cpu"


class SegmentConnector:
    def __init__(self):
        self.cap = Picamera2()
        camera_config = self.cap.create_preview_configuration()
        self.cap.configure(camera_config)

    def start(self):
        self.cap.start_preview(Preview.QTGL)
        self.cap.start()
        time.sleep(2)
        self.cap.capture_file(framePath)


