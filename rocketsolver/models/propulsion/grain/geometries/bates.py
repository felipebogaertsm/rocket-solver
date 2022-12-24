# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at me@felipebm.com.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

import numpy as np

from rocketsolver.utils.geometric import get_cylinder_surface_area

from .. import GrainSegment2D, GrainGeometryError
from rocketsolver.utils.decorators import validate_assertions


class BatesSegment(GrainSegment2D):
    def __init__(
        self,
        outer_diameter: float,
        core_diameter: float,
        length: float,
        spacing: float,
    ) -> None:
        self.core_diameter = core_diameter

        super().__init__(
            length=length,
            outer_diameter=outer_diameter,
            spacing=spacing,
            inhibited_ends=0,
        )

    @validate_assertions(exception=GrainGeometryError)
    def validate(self) -> None:
        super().validate()

        assert self.outer_diameter > self.core_diameter
        assert self.core_diameter > 0

    def get_core_area(self, web_distance: float) -> float:
        length = self.get_length(web_distance=web_distance)
        core_diameter = self.core_diameter + 2 * web_distance
        return get_cylinder_surface_area(length, core_diameter)

    def get_face_area(self, web_distance: float) -> float:
        core_diameter = self.core_diameter + 2 * web_distance
        return np.pi * (
            ((self.outer_diameter**2) - (core_diameter) ** 2) / 4
        )

    def get_web_thickness(self) -> float:
        """
        More details on the web thickness of BATES grains can be found in:
        https://www.nakka-rocketry.net/design1.html
        """
        return 0.5 * (self.outer_diameter - self.core_diameter)

    def get_optimal_length(self) -> float:
        """
        Returns the optimal length for BATES segment.
        More details on the calculation:
        https://www.nakka-rocketry.net/th_grain.html

        :return: Optimal length for neutral burn of BATES segment
        :rtype: float
        """
        return 1e3 * 0.5 * (3 * self.outer_diameter + self.core_diameter)