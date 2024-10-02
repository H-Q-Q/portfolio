import numpy as np
from scipy.interpolate import make_interp_spline


class Smooth:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.X_Y_Spline = make_interp_spline(x, y)

    def spline(self, x, y):
        X_ = np.linspace(x.min(), x.max(), 500)
        Y_ = self.X_Y_Spline(X_)
        return X_, Y_




