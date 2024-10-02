import numpy as np
import matplotlib.pyplot as plt

from smoother import Smooth


def main():
    xarray = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    yarray = np.array([20, 30, 5, 12, 39, 48, 50, 3])

    final_graph = Smooth(xarray, yarray)

    plt.plot(final_graph.spline(xarray, yarray)[0], final_graph.spline(xarray, yarray)[1])
    plt.title("Plot Smooth Curve Using the scipy.interpolate.make_interp_spline() Class")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


if __name__ == "__main__":
    main()
