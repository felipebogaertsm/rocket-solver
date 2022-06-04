# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at felipe.bogaerts@engenharia.ufjf.br.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

"""
Stores Motor class and methods.
"""

from abc import ABC, abstractmethod

from models.propulsion.grain import Grain
from models.propulsion.propellant import Propellant
from models.propulsion.structure import MotorStructure
from utils.isentropic_flow import get_thrust_coefficients, get_thrust_from_cf


class Motor(ABC):
    """
    Abstract rocket motor/engine class. Can be used to model any chemical
    rocket propulsion system, such as Solid, Hybrid and Liquid.
    """

    def __init__(
        self,
        propellant: Propellant,
        structure: MotorStructure,
    ) -> None:
        """
        Instantiates object attributes common to any motor/engine (Solid,
        Hybrid or Liquid).
        """
        self.propellant = propellant
        self.structure = structure

    @abstractmethod
    def get_thrust_coefficient_correction_factor(self) -> float:
        """
        Calculates the thrust coefficient correction factor.
        """
        pass

    @abstractmethod
    def get_thrust_coefficient(self) -> float:
        """
        Calculates the thrust coefficient for a particular instant.
        """
        pass

    def get_thrust(self, cf: float, chamber_pressure: float) -> float:
        """
        Calculates the thrust based on instantaneous thrust coefficient and
        chamber pressure.

        Utilized nozzle throat area from the structure and nozzle classes.
        """
        return get_thrust_from_cf(
            cf,
            chamber_pressure,
            self.structure.nozzle.get_throat_area(),
        )


class SolidMotor(Motor):
    def __init__(
        self,
        grain: Grain,
        propellant: Propellant,
        structure: MotorStructure,
    ) -> None:
        self.grain = grain
        super().__init__(propellant, structure)

        self.cf_ideal = None  # ideal thrust coefficient
        self.cf_real = None  # real thrust coefficient

    def get_thrust_coefficient_correction_factor(
        self, n_kin: float, n_bl: float, n_tp: float
    ) -> float:
        return (
            (100 - (n_kin + n_bl + n_tp))
            * self.structure.nozzle.get_divergent_correction_factor()
            / 100
            * self.propellant.combustion_efficiency
        )

    def get_thrust_coefficient(
        self,
        chamber_pressure: float,
        exit_pressure: float,
        external_pressure: float,
        expansion_ratio: float,
        k_2ph_ex: float,
        n_cf: float,
    ) -> float:
        self.cf_ideal, self.cf_real = get_thrust_coefficients(
            chamber_pressure,
            exit_pressure,
            external_pressure,
            expansion_ratio,
            k_2ph_ex,
            n_cf,
        )
        return self.cf_real
