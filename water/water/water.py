"""
Copyright (c) 2012-2021, OpenGeoSys Community (http://www.opengeosys.org)
              Distributed under a Modified BSD License.
                See accompanying file LICENSE or
                http://www.opengeosys.org/project/license

"""

# pylint: disable=C0103, R0902, R0914, R0913
import numpy as np
from water.properties import (density, viscosity, conductivity, specificheatcapacity, expansivity)

class WATER:
    """
    class defining water related properties at atmospheric
    and arbitrary pressure
    """
    def __init__(self, rho=1, mu=0, K=0, c=0, a=0):
        self.densities = [density.density_1,
                density.density_2,
                density.density_3,
                density.density_4,
                density.density_5,
                density.density_6]
        self.viscosities = [viscosity.viscosity_1,
                viscosity.viscosity_2,
                viscosity.viscosity_3,
                viscosity.viscosity_4,
                viscosity.viscosity_5]
        self.conductivities = [conductivity.conductivity_1, conductivity.conductivity_2, conductivity.conductivity_3]
        self.specificheatcapacities = [specificheatcapacity.specificheatcapacity_1, specificheatcapacity.specificheatcapacity_2]
        self.expansivities = [expansivity.expansivity_1, expansivity.expansivity_2, expansivity.expansivity_3]
        self.rho = self.densities[rho]()
        self.mu = self.viscosities[mu]()
        self.K = self.conductivities[K]()
        self.c = self.specificheatcapacities[c]()
        self.a = self.expansivities[a]()

        self.example_p = np.linspace(start=0, stop=10e6, num=100)
        self.example_T = np.linspace(start=273.15, stop=373.15, num=100)
