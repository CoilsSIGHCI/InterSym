import cv2
from EI.hw import is_raspberry_pi

on_device = is_raspberry_pi()


def send_frame(array):
    if on_device:
        from EI.display import Transmit
        Transmit.display(array)

    else:
        cv2.imshow("frame", array)
        cv2.waitKey(0)


def aggregator(dst, square, order, axis=1):
    import numpy
    remain_order = 1 - order
    # split the dst into by half
    dst_remain = numpy.split(dst, 2, axis=axis)[remain_order]
    # make square b&w if it's not
    if len(square.shape) > 2:
        square = square.mean(axis=2)
    # center crop the image to the size of the dst
    side = min(square.shape[0], square.shape[1])
    col_start = (square.shape[1] - side) // 2
    row_start = (square.shape[0] - side) // 2
    square = square[row_start:row_start + side, col_start:col_start + side]
    arrays = (square, dst_remain) if order == 0 else (dst_remain, square)
    dst[:, :] = numpy.concatenate(arrays, axis=axis)
