import RPi.GPIO as GPIO
import time
import numpy
import _thread
from lib import Transmit, Constants

from widgets.SegmentConnector import SegmentConnector
from ui import aggregator

# make a rectangle
rect_img = numpy.zeros((64, 128), dtype=numpy.uint8)
pair = ["vision", "empty"]

# draw a line in the middle


verbose = False

# parse argument
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        verbose = True


trans_frame = 30
timer = time.time()
target_fps = 30


def dispatcher():
    def vision():
        while True:
            try:
                order = pair.index("vision")
            except ValueError:
                continue
            segment = SegmentConnector()
            show = segment.start()
            aggregator(rect_img, show, order)
            Transmit.display(rect_img.tolist())

    _thread.start_new_thread(vision, ("vision", 0))

while True:
    dispatcher()
    time_diff = time.time() - timer
    if time_diff > 10:
        break

time.sleep(1)
Constants.spi.close()
GPIO.cleanup()
