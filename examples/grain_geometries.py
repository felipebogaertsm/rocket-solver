"""
This example demonstrates the capability of analyzing different grain 
geometries within Machwave.
"""

import os
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from machwave.models.propulsion.grain.geometries import (
    BatesSegment,
    MultiPortGrainSegment,
    ConicalGrainSegment,
    DGrainSegment,
)

np.set_printoptions(precision=2, suppress=True)


def main():
    bates_segment = BatesSegment(
        length=68e-3,
        outer_diameter=41e-3,
        core_diameter=15e-3,
        spacing=0.01,
    )

    multiport_segment = MultiPortGrainSegment(
        length=68e-3,
        outer_diameter=41e-3,
        spacing=0.01,
        port_diameter=3e-3,
        port_radial_count=6,
        port_level_count=4,
    )

    dgrain_segment = DGrainSegment(
        length=68e-3,
        outer_diameter=41e-3,
        spacing=0.01,
        slot_offset=10e-3,
    )

    conical_segment = ConicalGrainSegment(
        length=68e-3,
        outer_diameter=41e-3,
        upper_core_diameter=35e-3,
        lower_core_diameter=5e-3,
        spacing=0.01,
    )

    web_distance = 0

    grain_area = bates_segment.get_burn_area(web_distance=web_distance)
    port_area = bates_segment.get_port_area(web_distance=web_distance)
    print(f"BATES grain area: {grain_area * 1e6:2f} mm^2")
    print(f"BATES grain port area: {port_area * 1e6:2f} mm^2")

    grain_area = dgrain_segment.get_burn_area(web_distance=web_distance)
    port_area = dgrain_segment.get_port_area(web_distance=web_distance)
    print(f"Dgrain grain area: {grain_area * 1e6:2f} mm^2")
    print(f"Dgrain grain port area: {port_area * 1e6:2f} mm^2")
    print(
        f"Dgrain center of gravity: {dgrain_segment.get_center_of_gravity(0)}"
    )
    dgrain_segment.plot_face(web_distance=web_distance)

    grain_area = multiport_segment.get_burn_area(web_distance=web_distance)
    port_area = multiport_segment.get_port_area(web_distance=web_distance)
    print(f"Multiport grain area: {grain_area * 1e6:2f} mm^2")
    print(f"Multiport grain port area: {port_area * 1e6:2f} mm^2")
    print(
        f"Multiport center of gravity: {multiport_segment.get_center_of_gravity(0)}"
    )
    multiport_segment.plot_face(web_distance=web_distance)

    grain_area = conical_segment.get_burn_area(web_distance=web_distance)
    print(f"Conical grain area: {grain_area * 1e6:2f} mm^2")
    port_area = conical_segment.get_port_area(web_distance=web_distance)
    print(f"Conical grain port area: {port_area * 1e6:2f} mm^2")
    print(
        f"Conical center of gravity: {conical_segment.get_center_of_gravity(0)}"
    )


if __name__ == "__main__":
    main()
