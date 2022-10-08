# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at me@felipebm.com.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

from typing import Callable

import pytest

from rocketsolver.models.atmosphere import Atmosphere


@pytest.fixture()
def test_atmosphere_up_to_karman_line() -> Callable[[Atmosphere], None]:
    def test(atmosphere: Atmosphere) -> None:
        pressure_at_sea_level = atmosphere.get_pressure(y_amsl=0)
        assert pressure_at_sea_level == pytest.approx(101325, rel=1e-3)

        for i in range(int(100e3)):  # 0 up to 100 km
            height = float(i)

            # Test density:
            density = atmosphere.get_density(y_amsl=height)
            assert density >= 0
            # Test gravity:
            gravity = atmosphere.get_gravity(y_amsl=height)
            assert gravity >= 0
            # Test pressure:
            pressure = atmosphere.get_pressure(y_amsl=height)
            assert pressure >= 0
            # Test sonic velocity:
            sonic_v = atmosphere.get_sonic_velocity(y_amsl=height)
            assert sonic_v >= 0
            # Test wind velocity:
            wind_v = atmosphere.get_wind_velocity(y_amsl=height)
            assert len(wind_v) == 2
            # Test viscosity:
            viscosity = atmosphere.get_viscosity(y_amsl=height)
            assert viscosity >= 0

    return test
