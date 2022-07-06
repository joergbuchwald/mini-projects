"""
Copyright (c) 2012-2021, OpenGeoSys Community (http://www.opengeosys.org)
              Distributed under a Modified BSD License.
                See accompanying file LICENSE or
                http://www.opengeosys.org/project/license

"""
# pylint: disable=C0103, R0902, R0914, R0913
import numpy as np
from properties import template
T0 = 273.15

class conductivity_1(template.PROPERTY):
    def value(self, T):
        # source: https://www.engineeringtoolbox.com/water-liquid-gas-thermal-conductivity-temperature-pressure-d_2012.html
        temp = np.array([0.01, 10., 20., 30., 40., 50., 60., 70., 80., 90., 99.6])+T0
        K = np.array([
            0.556, 0.579, 0.598, 0.614, 0.629, 0.641, 0.651, 0.660, 0.667,
            0.673, 0.677
        ])
        return np.interp(T, temp, K)
    def dvalue(self, T):
        return np.gradient(self.value(T),T)
    def exprtk_value(self):
        raise NotImplementedError
    def exprtk_dvalue(self):
        raise NotImplementedError

class conductivity_2(template.PROPERTY):
    def value(self, temperature):
        # use only one-liner to keep it parsable:
        return  3.65759470e-08 * temperature**3 - 4.51285141e-05 * temperature**2 + 1.88275537e-02 * temperature - 1.96475421e+00
    def dvalue(self, temperature):
        # use only one-liner to keep it parsable:
        return 3.65759470e-08 * 3 * temperature**2 - 4.51285141e-05 * 2 * temperature + 1.88275537e-02
    def dvaluenum(self,temperature):
        return np.gradient(self.value(temperature),temperature)
    def exprtk_value(self):
        string = self._getcodeasstring("value", None)
        string = self._convertpythontoexprtk(string)
        return string
    def exprtk_dvalue(self, variable="temperature"):
        string = self._getcodeasstring("dvalue",None)
        string = self._convertpythontoexprtk(string)
        return string
