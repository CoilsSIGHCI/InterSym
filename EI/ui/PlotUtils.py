import numpy as np


def figure_to_matrix(fig):
    canvas = fig.canvas
    canvas.draw()
    width, height = canvas.get_width_height()
    image_array = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    image_array = image_array.reshape(height, width, 3)

    return image_array


def romanize(x):
    if x == 0:
        return "0"
    if x < 0:
        return "-" + romanize(-x)
    result = ""
    for r, n in (("M", 1000), ("CM", 900), ("D", 500), ("CD", 400), ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
                 ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1)):
        result += r * (x // n)
        x %= n
    return result
