# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at felipe.bogaerts@engenharia.ufjf.br.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

from typing import List

from solvers import Solver
from utils.odes import solve_cp_seidel


class SRMInternalBallisticsSolver(Solver):
    def solve(
        self,
        chamber_pressure: float,
        external_pressure: float,
        burn_area: float,
        propellant_volume: float,
        nozzle_area: float,
        propellant_density: float,
        k_mix_ch: float,
        R_ch: float,
        T_O: float,
        burn_rate: float,
        d_t: float,
    ) -> List[float]:
        k_1 = solve_cp_seidel(
            chamber_pressure,
            external_pressure,
            burn_area,
            propellant_volume,
            nozzle_area,
            propellant_density,
            k_mix_ch,
            R_ch,
            T_O,
            burn_rate,
        )

        k_2 = solve_cp_seidel(
            chamber_pressure + 0.5 * k_1 * d_t,
            external_pressure,
            burn_area,
            propellant_volume,
            nozzle_area,
            propellant_density,
            k_mix_ch,
            R_ch,
            T_O,
            burn_rate,
        )

        k_3 = solve_cp_seidel(
            chamber_pressure + 0.5 * k_2 * d_t,
            external_pressure,
            burn_area,
            propellant_volume,
            nozzle_area,
            propellant_density,
            k_mix_ch,
            R_ch,
            T_O,
            burn_rate,
        )

        k_4 = solve_cp_seidel(
            chamber_pressure + 0.5 * k_3 * d_t,
            external_pressure,
            burn_area,
            propellant_volume,
            nozzle_area,
            propellant_density,
            k_mix_ch,
            R_ch,
            T_O,
            burn_rate,
        )

        return (
            chamber_pressure + (1 / 6) * (k_1 + 2 * (k_2 + k_3) + k_4) * d_t,
        )