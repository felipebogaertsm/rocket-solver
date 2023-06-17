"""
Stores the functions used to calculate geometric parameters.
"""

from typing import Optional

import numpy as np
from skimage import measure


def get_circle_area(diameter):
    """
    Returns the area of the circle based on circle diameter.
    """
    return np.pi * 0.25 * diameter ** 2


def get_trapezoidal_area(base_length, tip_length, height):
    return (base_length + tip_length) * height / 2


def get_cylinder_surface_area(length: float, diameter: float) -> float:
    """
    Returns the surface area of a cylinder.
    """
    return np.pi * length * diameter


def get_cylinder_volume(diameter, length):
    return np.pi * length * (diameter ** 2) / 4


def get_contours(
    map: np.ndarray, map_dist: float, *args, **kwargs
) -> np.ndarray:
    return measure.find_contours(
        map, map_dist, fully_connected="low", *args, **kwargs
    )


def get_length(
    contour: np.ndarray, map_size: int, tolerance: Optional[float] = 3.0
):
    """
    Returns the total length of all segments in a contour that aren't within
    'tolerance' of the edge of a circle with diameter 'map_size'
    """
    offset = np.roll(contour.T, 1, axis=1)
    lengths = np.linalg.norm(contour.T - offset, axis=0)

    center_offset = np.array([[map_size / 2, map_size / 2]])
    radius = np.linalg.norm(contour - center_offset, axis=1)

    valid = radius < (map_size / 2) - tolerance

    return np.sum(lengths[valid])