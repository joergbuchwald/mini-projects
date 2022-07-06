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

class expansivity_1(template.PROPERTY):
    def value(self, T):
        # source: https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html
        temp = np.array([
            0.0, 4., 10., 20., 30., 40., 50., 60., 70., 80., 90., 140., 200.,
            260.
        ]) + T0
        beta = np.array([
            -5.e-5, 0.003e-4, 8.8e-5, 2.07e-4, 3.03e-4, 3.85e-4, 4.57e-4, 5.22e-4,
            5.82e-4, 6.40e-4, 6.95e-4, 9.75e-4, 1.59e-3, 2.21e-3
        ])
        return np.interp(T, temp, beta)
    def dvalue(self, T):
        return np.gradient(self.value(T),T)
    def exprtk_value(self):
        raise NotImplementedError
    def exprtk_dvalue(self):
        raise NotImplementedError

class expansivity_2(template.PROPERTY):
    def value(self, temperature):
        # use only one-liner to keep it parsable:
        return  1.23809241e-10 * temperature**3 - 1.42082200e-07 * temperature**2 + 6.07557105e-05 * temperature - 8.53641540e-03
    def dvalue(self, temperature):
        # use only one-liner to keep it parsable:
        return 1.23809241e-10 * 3 * temperature**2 - 1.42082200e-07 * 2 * temperature + 6.07557105e-05
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
