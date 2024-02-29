from time import sleep
from EI.hw import is_raspberry_pi
from EI.hw.spectrum.AS7341 import AS7341
from EI.ui.PlotUtils import figure_to_matrix


class GenericSpectrum:
    def __init__(self):
        self.device = AS7341()
        self.device.AS7341_ATIME_config(100)
        self.device.AS7341_ASTEP_config(999)
        self.device.AS7341_AGAIN_config(6)
        self.device.AS7341_EnableLED(False)

    def start(self, figure_size=(64, 64), verbose=False):
        self.device.AS7341_startMeasure(0)
        self.device.AS7341_ControlLed(True, 10)
        self.device.AS7341_startMeasure(0)
        sleep(1)
        self.device.AS7341_ReadSpectralDataOne()
        if verbose:
            print('channel1(405-425nm):\r\n')
            print('%d\r\n' % self.device.channel1)
            print('channel2(435-455nm):\r\n')
            print('%d\r\n' % self.device.channel2)
            print('channel3(470-490nm):\r\n')
            print('%d\r\n' % self.device.channel3)
            print('channel4(505-525nm):\r\n')
            print('%d\r\n' % self.device.channel4)
        self.device.AS7341_startMeasure(1)
        self.device.AS7341_ReadSpectralDataTwo()
        if verbose:
            print('channel5(545-565nm):\r\n')
            print('%d\r\n' % self.device.channel5)
            print('channel6(580-600nm):\r\n')
            print('%d\r\n' % self.device.channel6)
            print('channel7(620-640nm):\r\n')
            print('%d\r\n' % self.device.channel7)
            print('channel8(670-690nm):\r\n')
            print('%d\r\n' % self.device.channel8)
            print('Clear:\r\n')
            print('%d\r\n' % self.device.CLEAR)
            print('NIR:\r\n')
            print('%d\r\n' % self.device.NIR)

        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import make_interp_spline

        plt.style.use('dark_background')
        figure = plt.figure(figsize=(figure_size[0] / 100, figure_size[1] / 100))
        ax = figure.subplots()
        ax.set_axis_off()
        ax.set_position([0, 0, 1, 1])
        x = np.array([405, 435, 470, 505, 545, 580, 620, 670, 880])
        y = np.array([self.device.channel1, self.device.channel2, self.device.channel3, self.device.channel4,
                      self.device.channel5, self.device.channel6, self.device.channel7, self.device.channel8,
                      self.device.NIR])
        x_smooth = np.linspace(x.min(), x.max(), 64)
        y_smooth = make_interp_spline(x, y)(x_smooth)
        ax.plot(x_smooth, y_smooth, color="white", linewidth=1)

        y_max = y.max()
        text = "{:d}".format(y_max)
        ax.annotate(text, xy=(0, 0.8), xytext=(0, 0.8), xycoords='axes fraction', textcoords='axes fraction')

        if is_raspberry_pi():
            figure.savefig('/tmp/spectrum.png')
        else:
            figure.show()

        render = figure_to_matrix(figure)
        return render

    def stop(self):
        pass


if __name__ == '__main__':
    spectrum = GenericSpectrum()
    spectrum.start()
    spectrum.stop()
