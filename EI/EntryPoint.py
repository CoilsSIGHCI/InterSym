import RPi.GPIO as GPIO
import numpy
from cv2 import imwrite

from display import Transmit, Constants

from widgets.SegmentConnector import SegmentConnector
from ui.ui import aggregator

# make a rectangle
rect_img = numpy.zeros((64, 128), dtype=numpy.uint8)

verbose = False

# parse argument
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        verbose = True


segment = SegmentConnector()

while True:
    show = segment.start()
    aggregator(rect_img, show, 0)
    # write the rec_img to file for debug purpose
    imwrite("/tmp/rect_img.png", rect_img)
    # Transmit.display(rect_img.tolist())
