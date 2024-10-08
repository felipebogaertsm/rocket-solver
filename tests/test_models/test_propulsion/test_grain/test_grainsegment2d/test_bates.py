import pytest

from machwave.models.propulsion.grain.geometries import BatesSegment
from machwave.models.propulsion.grain import GrainGeometryError


def test_bates_segment_geometry_validation():
    # Control group:
    _ = BatesSegment(
        outer_diameter=100e-3,
        core_diameter=30e-3,
        length=120e-3,
        spacing=10e-3,
    )

    # Larger core diameter than outer diameter:
    with pytest.raises(GrainGeometryError):
        _ = BatesSegment(
            outer_diameter=100e-3,
            core_diameter=300e-3,
            length=120e-3,
            spacing=10e-3,
        )

    # Negative core diameter:
    with pytest.raises(GrainGeometryError):
        _ = BatesSegment(
            outer_diameter=100e-3,
            core_diameter=-30e-3,
            length=120e-3,
            spacing=10e-3,
        )

    # Negative length:
    with pytest.raises(GrainGeometryError):
        _ = BatesSegment(
            outer_diameter=100e-3,
            core_diameter=30e-3,
            length=-120e-3,
            spacing=10e-3,
        )

    # Negative spacing:
    with pytest.raises(GrainGeometryError):
        _ = BatesSegment(
            outer_diameter=100e-3,
            core_diameter=30e-3,
            length=120e-3,
            spacing=-10e-3,
        )


def test_olympus_grain_total_length_property(bates_grain_olympus):
    grain = bates_grain_olympus
    total_length = 0

    for segment in grain.segments:
        total_length += segment.length + segment.spacing

    assert grain.total_length == total_length
    assert grain.total_length == 1470e-3


def test_olympus_grain_segment_count(bates_grain_olympus):
    assert bates_grain_olympus.segment_count == 7
    assert bates_grain_olympus.segment_count == len(
        bates_grain_olympus.segments
    )
