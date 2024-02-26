import RPi.GPIO as GPIO
import numpy
from cv2 import imwrite

from display import Transmit, Constants

from widgets.SegmentConnector import SegmentConnector
from ui.ui import aggregator

# make a rectangle
rect_img = numpy.zeros(Constants.screenSize, dtype=numpy.uint8)

verbose = False

# parse argument
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        verbose = True


segment = SegmentConnector(rotate=True)

while True:
    show = segment.start(crop=False)
    aggregator(rect_img, show, 0)
    aggregator(rect_img, show, 1)
    rect_img = rect_img.astype(numpy.uint8)
    print(rect_img.shape)
    Transmit.display(rect_img.tolist())
