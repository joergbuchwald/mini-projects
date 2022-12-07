import numpy as np
import matplotlib.pyplot as plt

from water import water

f_eng_toolbox = water.WATER(rho=0,mu=0)
T = f_eng_toolbox.example_T
p = np.linspace(start=-1e6, stop=10e6, num=200)
f_exp = water.WATER(rho=4,mu=4)
f_IAPWS = water.WATER(rho=5)

plt.title("exp. density model vs temperature")
plt.plot(T, f_eng_toolbox.rho.value(T), label="eng toolbox")
plt.plot(T, f_exp.rho.value(T, 1e6), label="exp density model")
plt.plot(T, f_IAPWS.rho.value(T, 1e6), label="IAPWS density model")
plt.legend()
plt.xlabel("T / K")
plt.ylabel("rho / kg m$^-3$")
plt.show()
print(f_exp.rho.exprtk_value())

plt.title("derivative of exp. density model with respect to temperature")
plt.plot(T, f_exp.rho.dvaluenum(T, 1e6, variable="temperature"), label="numerical derivative exp")
plt.plot(T, f_exp.rho.dvalue(T, 1e6, variable="temperature"), label="analytical derivative exp")
plt.plot(T, f_IAPWS.rho.dvaluenum(T, 1e6, variable="temperature"), label="numerical derivative IAPWS")
plt.plot(T, f_IAPWS.rho.dvalue(T, 1e6, variable="temperature"), label="analytical derivative IAPWS")
plt.legend()
plt.xlabel("T / K")
plt.ylabel("Drho / kg m$^-3$ K$^-1$")
plt.show()
print(f_exp.rho.exprtk_dvalue())


plt.title("derivative of exp. density model with respect to pressure")
plt.plot(p, f_exp.rho.dvaluenum(300, p, variable="phase_pressure"), label="numerical derivative")
plt.plot(p, f_exp.rho.dvalue(300, p, variable="phase_pressure"), label="analytical derivative")
plt.legend()
plt.xlabel("p / Pa")
plt.ylabel("Drho / kg m$^-3$ Pa$^-1$")
plt.show()
print(f_exp.rho.exprtk_dvalue(variable="phase_pressure"))


plt.title("exp. viscosity model vs temperature")
plt.plot(f_eng_toolbox.example_T, f_eng_toolbox.mu.value(f_eng_toolbox.example_T), label="eng toolbox")
plt.plot(f_exp.example_T, f_exp.mu.value(f_exp.example_T), label="exp viscosity model")
plt.legend()
plt.xlabel("T / K")
plt.ylabel("$\mu$ / Pa s")
plt.show()
print(f_exp.mu.exprtk_value())

plt.title("derivative of exp. viscosity model with respect to temperature")
plt.plot(f_exp.example_T, f_exp.mu.dvaluenum(f_exp.example_T), label="numerical derivative")
plt.plot(f_exp.example_T, f_exp.mu.dvalue(f_exp.example_T), label="analytical derivative")
plt.legend()
plt.xlabel("T / K")
plt.ylabel("$\mu$ / Pa s K$^-1$")
plt.show()
print(f_exp.mu.exprtk_dvalue())
