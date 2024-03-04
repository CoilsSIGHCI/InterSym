import pathlib
from datetime import datetime

import RPi.GPIO as GPIO
import numpy
from cv2 import imwrite

from EI.widgets.GenericSpectrum import GenericSpectrum
from display import Transmit, Constants

from widgets.SegmentConnector import SegmentConnector
from ui.UI import aggregator

# make a rectangle
rect_img = numpy.zeros(Constants.screenSize, dtype=numpy.uint8)

verbose = False

# parse argument
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        verbose = True


segment = SegmentConnector(rotate=True)
spectrum = GenericSpectrum()

while True:
    segment_figure = segment.start(crop=False)
    aggregator(rect_img, segment_figure, 0)
    spectrum_figure = spectrum.start()
    aggregator(rect_img, spectrum_figure, 1)
    rect_img = rect_img.astype(numpy.uint8)
    time_string = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
    pathlib.Path(f"/tmp/InterSym/{time_string}").mkdir(parents=True)
    imwrite(f"/tmp/InterSym/{time_string}/segment.png", segment_figure)
    imwrite(f"/tmp/InterSym/{time_string}/spectrum.png", spectrum_figure)
    imwrite("/tmp/current.png", rect_img)
    Transmit.display(rect_img.tolist())
