"""
Copyright (c) 2012-2021, OpenGeoSys Community (http://www.opengeosys.org)
              Distributed under a Modified BSD License.
                See accompanying file LICENSE or
                http://www.opengeosys.org/project/license

"""
# pylint: disable=C0103, R0902, R0914, R0913
import numpy as np
from water.properties import template
from water.properties import gibbsfreeenergy
T0 = 273.15

class density_1(template.PROPERTY):
    def value(self, temperature):
        # source: https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html
        temp = np.array([
            0.1, 1.0, 4., 10., 15., 20., 25., 30., 35., 40., 45., 50., 60.,
            70., 80., 90., 100., 110., 140., 200., 260., 300., 360.
        ]) + T0
        if (np.min(temperature) < temp[0]) or (np.max(temperature) > temp[-1]):
            print("The temperature is not within the defined domain")
        dens = np.array([
            999.85, 999.9, 999.97, 999.7, 999.1, 998.2, 997., 995.6, 994.,
            992.2, 990.2, 988., 983.2, 977.76, 971.8, 965.3, 958.6, 951.0,
            926.1, 865., 783.6, 712.2, 527.6
        ])
        return np.interp(temperature, temp, dens)
    def dvalue(self,temperature):
        return np.gradient(self.value(temperature),temperature)
    def exprtk_value(self):
        raise NotImplementedError
    def exprtk_dvalue(self):
        raise NotImplementedError

class density_2(template.PROPERTY):
    def value(self, temperature, phase_pressure):
        # use only one-liner to keep it parsable:
        return 1000.1 * (1 - (-6*10**-6 * (temperature-T0)**4 + 0.001667 * (temperature-T0)**3 + -0.197796 * (temperature-T0)**2 + 16.86446 * (temperature-T0) - 64.319951)/10**6 * (temperature-293.15) + 4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
    def dvalue(self, temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            # use only one-liner to keep it parsable:
            return -1000.1 * ((-6*10**-6 * (temperature-T0)**4 + 0.001667 * (temperature-T0)**3 + -0.197796 * (temperature-T0)**2 + 16.86446 * (temperature-T0) - 64.319951)/10**6+(-6*10**-6 * 4 * (temperature-T0)**3 + 0.001667 * 3 * (temperature-T0)**2 + -0.197796 * 2 * (temperature-T0) + 16.86446 )/10**6*(temperature-293.15))
        elif variable == "phase_pressure":
            # use only one-liner to keep it parsable:
            return np.maximum(np.sign(phase_pressure),0)* 1000.1 * 4.65e-10
    def dvaluenum(self,temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            return np.gradient(self.value(temperature,phase_pressure),temperature)
        elif variable == "phase_pressure":
            return np.gradient(self.value(temperature,phase_pressure),phase_pressure)
    def exprtk_value(self):
        string = self._getcodeasstring("value", None)
        string = self._convertpythontoexprtk(string)
        return string
    def exprtk_dvalue(self, variable="temperature"):
        string = self._getcodeasstring("dvalue",variable)
        string = self._convertpythontoexprtk(string)
        return string

class density_3(template.PROPERTY):
    def value(self, temperature, phase_pressure):
        # use only one-liner to keep it parsable:
        return (5.38784232e-06*temperature**3 - 8.61928859e-03*temperature**2 +  3.44638154e+00*temperature + 5.92596450e+02) * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
    def dvalue(self, temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            return (3*5.38784232e-06*temperature**2 - 2*8.61928859e-03*temperature +  3.44638154e+00) * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
        elif variable == "phase_pressure":
            return (5.38784232e-06*temperature**3 - 8.61928859e-03*temperature**2 +  3.44638154e+00*temperature + 5.92596450e+02) * np.maximum(np.sign(phase_pressure),0) * 4.65e-10
    def dvaluenum(self,temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),temperature)
        elif variable == "phase_pressure":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),phase_pressure)
    def exprtk_value(self):
        string = self._getcodeasstring("value", None)
        string = self._convertpythontoexprtk(string)
        return string
    def exprtk_dvalue(self, variable="temperature"):
        string = self._getcodeasstring("dvalue",variable)
        string = self._convertpythontoexprtk(string)
        return string

class density_4(template.PROPERTY):
    def value(self, temperature, phase_pressure):
        # use only one-liner to keep it parsable:
        return 1002.6 * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5) - 3.4e-4 * (temperature-T0))
    def dvalue(self, temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            return 1002.6 * (-3.4e-4) * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5) - 3.4e-4 * (temperature-T0))
        elif variable == "phase_pressure":
            return 1002.6 * np.maximum(np.sign(phase_pressure),0) * 4.65e-10 * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5) - 3.4e-4 * (temperature-T0))
    def dvaluenum(self,temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),temperature)
        elif variable == "phase_pressure":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),phase_pressure)
    def exprtk_value(self):
        string = self._getcodeasstring("value", None)
        string = self._convertpythontoexprtk(string)
        return string
    def exprtk_dvalue(self, variable="temperature"):
        string = self._getcodeasstring("dvalue",variable)
        string = self._convertpythontoexprtk(string)
        return string

class density_5(template.PROPERTY):
    def value(self, temperature, phase_pressure):
        # use only one-liner to keep it parsable:
        return 1000.0 * (1 - ((1./4.* 4e-6*(temperature-273.15)**3-1./3.*0.001*(temperature-273.15)**2+1./2.*0.1404*(temperature-273.15)-0.3795)*1e-4) *(temperature-273.15) + 4.5e-10 * (max(phase_pressure, 0.0) - 1.e5))
    def dvalue(self, temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            return -1000.0*((4e-6*(temperature-273.15)**3-0.001*(temperature-273.15)**2+0.1404*(temperature-273.15)-0.3795)*1e-4)
        elif variable == "phase_pressure":
            return max(sgn(phase_pressure),0)* 1000.0 * 4.5e-10
    def dvaluenum(self,temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),temperature)
        elif variable == "phase_pressure":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),phase_pressure)
    def exprtk_value(self):
        string = self._getcodeasstring("value", None)
        string = self._convertpythontoexprtk(string)
        return string
    def exprtk_dvalue(self, variable="temperature"):
        string = self._getcodeasstring("dvalue",variable)
        string = self._convertpythontoexprtk(string)
        return string

class density_6(template.PROPERTY):
    def __init__(self):
        self._ref_T = 1386
        self._ref_p = 1.653e7
        self._sR = 461.526

    def value(self, temperature, phase_pressure):
        tau = self._ref_T / temperature
        pi = phase_pressure / self._ref_p
        return self._ref_p / (self._sR * temperature * gibbsfreeenergy.get_dgamma_dpi(tau, pi))

    def dvalue(self, temperature, phase_pressure, variable="temperature"):
        tau = self._ref_T / temperature
        pi = phase_pressure / self._ref_p
        dgamma_dpi = gibbsfreeenergy.get_dgamma_dpi(tau, pi)
        if variable == "temperature":
            return -(self._ref_p - tau * self._ref_p * gibbsfreeenergy.get_dgamma_dtau_dpi(tau, pi) / dgamma_dpi) / (self._sR * temperature * temperature * dgamma_dpi)
        elif variable == "phase_pressure":
            return -gibbsfreeenergy.get_dgamma_dpi_dpi(tau, pi) / (self._sR * temperature * dgamma_dpi * dgamma_dpi)
    def dvaluenum(self,temperature, phase_pressure, variable="temperature"):
        if variable == "temperature":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),temperature)
        elif variable == "phase_pressure":
            # use only one-liner to keep it parsable:
            return np.gradient(self.value(temperature,phase_pressure),phase_pressure)


