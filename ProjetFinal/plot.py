import numpy as np
import matplotlib.pyplot as plt


def plot_diagrams(y, y_name, x, x_name):
    """
    Plot is based on 2 numpy ndarrays

    :param y: y axis data
    :param y_name: y title
    :param x: x axis data
    :param x_name: x title.
    """
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
        return
    plt.figure().set_figwidth(9)
    plt.plot(x, y)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    # plt.legend()
    plt.show()
