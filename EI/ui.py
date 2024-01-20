def frame(array, real=False, fps="asap"):
    if real:
        from lib import Transmit
        Transmit.display(array)
    else:
        from matplotlib import animation
        import matplotlib.pyplot as plt
        import numpy

        fig, ax = plt.subplots()
        im = ax.imshow(array, animated=True)

        def updatefig(*args):
            im.set_array(numpy.random.rand(64, 128))
            return im,

        ani = animation.FuncAnimation(fig, updatefig, interval=1000 / fps, blit=True)

        plt.show()


def aggregator(left, right, axis=1):
    import numpy
    return numpy.concatenate((left, right), axis=axis)


def tick():
    from widgets.SegmentConnector import SegmentConnector
    from widgets.Waveform import Waveform