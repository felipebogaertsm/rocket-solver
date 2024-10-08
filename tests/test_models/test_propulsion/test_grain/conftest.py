import pytest

from machwave.models.propulsion.grain import Grain
from machwave.models.propulsion.grain.geometries.bates import BatesSegment

"""
Olympus fixtures are based on the 2022 version of the motor.
"""


@pytest.fixture
def bates_segment_olympus_45():
    return BatesSegment(
        outer_diameter=117e-3,
        core_diameter=45e-3,
        length=200e-3,
        spacing=10e-3,
    )


@pytest.fixture
def bates_segment_olympus_60():
    return BatesSegment(
        outer_diameter=117e-3,
        core_diameter=60e-3,
        length=200e-3,
        spacing=10e-3,
    )


@pytest.fixture
def bates_grain_olympus(bates_segment_olympus_45, bates_segment_olympus_60):
    grain = Grain()

    # Adding 4 45 mm segments and 3 60mm segments:
    grain.add_segment(bates_segment_olympus_45)
    grain.add_segment(bates_segment_olympus_45)
    grain.add_segment(bates_segment_olympus_45)
    grain.add_segment(bates_segment_olympus_45)
    grain.add_segment(bates_segment_olympus_60)
    grain.add_segment(bates_segment_olympus_60)
    grain.add_segment(bates_segment_olympus_60)

    return grain
