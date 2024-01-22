def send_frame(array, real=False, fps="asap"):
    if real:
        from EI.lib import Transmit
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
    dst_remain = numpy.split(dst, [square], axis=axis)[remain_order]
    if order == 0:
        return numpy.concatenate((square, dst_remain), axis=axis)
    else:
        return numpy.concatenate((dst_remain, square), axis=axis)
