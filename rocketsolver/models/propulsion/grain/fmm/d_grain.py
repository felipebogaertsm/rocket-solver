# -*- coding: utf-8 -*-
# Author: Felipe Bogaerts de Mattos
# Contact me at felipe.bogaerts@engenharia.ufjf.br.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

import numpy as np

from . import FMMGrainSegment


class DGrainSegment(FMMGrainSegment):
    def __init__(
        self,
        outer_diameter: float,
        length: float,
        slot_offset: float,
        spacing: float,
    ) -> None:
        self.outer_diameter = outer_diameter
        self.length = length
        self.slot_offset = slot_offset
        self.spacing = spacing

        super().__init__()

    def validate(self) -> None:
        assert self.outer_diameter > 0
        assert self.length > 0
        assert self.slot_offset > 0

    def get_outer_diameter(self) -> float:
        return self.outer_diameter

    def get_segment_length(self, web_thickness: float) -> float:
        return self.length - 2 * web_thickness

    def map_to_area(self, value):
        return (self.outer_diameter**2) * (value / (self.map_dim**2))

    def map_to_length(self, value: float) -> float:
        return self.outer_diameter * (value / self.map_dim)

    def get_face_map(self) -> np.ndarray:
        slot_offset_normalized = self.normalize(self.slot_offset)
        map_x = self.get_maps()[0]
        core_map = self.get_empty_face_map()
        core_map[map_x > slot_offset_normalized] = 0
        return core_map