import cv2


def send_frame(array, real=False, fps="asap"):
    if real:
        from EI.display import Transmit
        Transmit.display(array)

    # TODO: Add support for display preview
    else:
        from matplotlib import animation
        import matplotlib.pyplot as plt
        import numpy

        fig, ax = plt.subplots()
        im = ax.imshow(array, animated=True)

        def updatefig(*args):
            im.set_array(numpy.random.rand(64, 128))
            return im,

        plt.show()


def aggregator(dst, square, order, axis=1):
    import numpy
    remain_order = 1 - order
    # split the dst into by half
    dst_remain = numpy.split(dst, 2, axis=axis)[remain_order]
    # make square b&w if it's not
    if len(square.shape) > 2:
        square = square.mean(axis=2)
    # resample the square to fit the dst
    if axis == 1:
        square = cv2.resize(square, (dst.shape[0], dst.shape[0]))
    else:
        square = cv2.resize(square, (dst.shape[1], dst.shape[1]))
    if order == 0:
        return numpy.concatenate((square, dst_remain), axis=axis)
    else:
        return numpy.concatenate((dst_remain, square), axis=axis)
