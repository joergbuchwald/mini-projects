import numpy as np

class watermodel(object):
    def __init__(self):
        pass
    def rho(self,temperature,phase_pressure):
        return 1000.1 * (1 - (-6*10**-6 * (temperature-273.15)**4 + 0.001667 * (temperature-273.15)**3 + -0.197796 * (temperature-273.15)**2 + 16.86446 * (temperature-273.15) - 64.319951)/10**6 * (temperature-293.15) + 4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
    def drho_dT(self,temperature,phase_pressure):
        return -1000.1 * ((-6*10**-6 * (temperature-273.15)**4 + 0.001667 * (temperature-273.15)**3 + -0.197796 * (temperature-273.15)**2 + 16.86446 * (temperature-273.15) - 64.319951)/10**6+(-6*10**-6 * 4 * (temperature-273.15)**3 + 0.001667 * 3 * (temperature-273.15)**2 + -0.197796 * 2 * (temperature-273.15) + 16.86446 )/10**6*(temperature-293.15))
    def drho_dp(self,temperature,phase_pressure):
        return np.maximum(np.sign(phase_pressure),0)* 1000.1 * 4.65e-10
    def numDrho_dT(self,temperature,phase_pressure):
        return np.gradient(self.rho(temperature,phase_pressure),temperature)
    def numDrho_dp(self,temperature,phase_pressure):
        return np.gradient(self.rho(temperature,phase_pressure),phase_pressure)
    def rho2(self,temperature,phase_pressure):
        return 1.0187339257193984*(5.38784232e-06*temperature**3 - 8.61928859e-03*temperature**2 +  3.44638154e+00*temperature + 5.92596450e+02) * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
    def drho2_dp(self,temperature,phase_pressure):
        return 1.0187339257193984*(5.38784232e-06*temperature**3 - 8.61928859e-03*temperature**2 +  3.44638154e+00*temperature + 5.92596450e+02) * np.maximum(np.sign(phase_pressure),0) * 4.65e-10
    def drho2_dT(self,temperature,phase_pressure):
        return 1.0187339257193984*(3*5.38784232e-06*temperature**2 - 2*8.61928859e-03*temperature +  3.44638154e+00) * np.exp(4.65e-10 * (np.maximum(phase_pressure, 0.0) - 1e5))
    def numDrho2_dT(self,temperature,phase_pressure):
        return np.gradient(self.rho2(temperature,phase_pressure),temperature)
    def numDrho2_dp(self,temperature,phase_pressure):
        return np.gradient(self.rho2(temperature,phase_pressure),phase_pressure)
    def mu(self,temperature):
        return -2.01570959e-09 * temperature**3 + 2.11402803e-06 * temperature**2 - 7.43932150e-04 * temperature +  8.82066680e-02
    def dmu_dT(self,temperature):
        return -2.01570959e-09 * 3 * temperature**2 + 2.11402803e-06 * 2 * temperature - 7.43932150e-04
    def numDmu_dT(self,temperature):
        return np.gradient(self.mu(temperature),temperature)
    def mu2(self, temperature):
        A=2.414*10**(-5)
        B=247.8
        C=140
        return A*10**(B/(temperature-C))
    def mu3(self, temperature):
        return 4.2844e-5+1/(0.157 * (temperature-208.157) * (temperature-208.157)-91.296)
    def dmu2_dT(self, temperature):
        A=2.414*10**(-5)
        B=247.8
        C=140
        return -A*B*np.log(10) * 10**(B/(temperature-C))/(temperature-C)**2
    def numDmu2_dT(self,temperature):
        return np.gradient(self.mu2(temperature),temperature)
