import time
import numpy
from .ui import send_frame


def cubic_bezier(t, pos0, pos1, ratio0, ratio1):
    r = (1-t)*((1-t)*((1-t)*pos0+t*pos0)+t*((1-t)*pos0+t*pos1))+t*((1-t)*((1-t)*pos0+t*pos1)+t*((1-t)*pos1+t*pos1))
    return int(r)

def bezier_easing(trans_frame, target_fps, verbose=False):
    timer = time.time()

    for turn in range(10):
        frame = 1
        while frame <= trans_frame:
            pos0 = 0 if turn % 2 == 0 else 127
            pos1 = 127 if turn % 2 == 0 else 0
            pos = cubic_bezier(frame / trans_frame, pos0, pos1, 0.5, 0.5)
            rect_img = numpy.zeros((64, 128), dtype=numpy.uint8)
            for i in range(64):
                rect_img[i][pos] = 255
            send_frame(rect_img.tolist())
            time.sleep(1 / target_fps)
            time_diff = time.time() - timer
            if time_diff < 1 / target_fps:
                time.sleep(1 / target_fps - time_diff)
            elif verbose:
                print("Can't keep up with target fps!")
            frame += 1