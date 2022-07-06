"""
Copyright (c) 2012-2021, OpenGeoSys Community (http://www.opengeosys.org)
              Distributed under a Modified BSD License.
                See accompanying file LICENSE or
                http://www.opengeosys.org/project/license

"""

# pylint: disable=C0103, R0902, R0914, R0913
import numpy as np
T0 = 273.15

class WATER:
    """
    class defining water related properties at atmospheric pressure
    """
    def __init__(self):

    def a_w(self, T):
        """
        thermal expansion coeffient

        Parameters
        ----------
        T : `float` temperature
        """
        temp = [
            0.0, 4., 10., 20., 30., 40., 50., 60., 70., 80., 90., 140., 200.,
            260.
        ]
        for i, tempi in enumerate(temp):
            temp[i] = tempi + T0
        beta = [
            -5.e-5, 0.0, 8.8e-5, 2.07e-4, 3.03e-4, 3.85e-4, 4.57e-4, 5.22e-4,
            5.82e-4, 6.40e-4, 6.95e-4, 9.75e-4, 1.59e-3, 2.21e-3
        ]
        return np.interp(T, temp, beta)

    def rho_w(self, T):
        """
        density

        Parameters
        ----------
        T : `float` temperature
        """
        temp = [
            0.1, 1.0, 4., 10., 15., 20., 25., 30., 35., 40., 45., 50., 60.,
            70., 80., 90., 100., 110., 140., 200., 260., 300., 360.
        ]
        for i, tempi in enumerate(temp):
            temp[i] = tempi + T0
        dens = [
            999.85, 999.9, 999.97, 999.7, 999.1, 998.2, 997., 995.6, 994.,
            992.2, 990.2, 988., 983.2, 977.76, 971.8, 965.3, 958.6, 951.0,
            926.1, 865., 783.6, 712.2, 527.6
        ]
        return np.interp(T, temp, dens)

    def K_w(self, T):
        """
        thermal conductivity

        Parameters
        ----------
        T : `float` temperature
        """
        temp = [0.01, 10., 20., 30., 40., 50., 60., 70., 80., 90., 99.6]
        for i, tempi in enumerate(temp):
            temp[i] = tempi + T0
        K = [
            0.556, 0.579, 0.598, 0.614, 0.629, 0.641, 0.651, 0.660, 0.667,
            0.673, 0.677
        ]
        return np.interp(T, temp, K)

    def c_w(self, T):
        """
        specific heat capacity at constant pressure

        Parameters
        ----------
        T : `float` temperature
        """
        temp = [0.01, 10., 20., 30., 40., 50., 60., 70., 80., 90., 100.]
        for i, tempi in enumerate(temp):
            temp[i] = tempi + T0
        cw = [
            4217., 4191., 4157., 4118., 4074., 4026., 3977., 3925., 3873.,
            3820., 3768
        ]
        return np.interp(T, temp, cw)

    def viscosity(self, T):
        """
        viscosity

        Parameters
        ----------
        T : `float` temperature
        """
        temp = [10., 20., 30., 40., 50., 60., 70., 80., 90., 100.]
        for i, tempi in enumerate(temp):
            temp[i] = tempi + T0
        vis = [
            0.0013, 0.001, 0.0007978, 0.0006531, 0.0005471, 0.0004658,
            0.0004044, 0.000355, 0.000315, 0.00002822
        ]
        return np.interp(T, temp, vis)
