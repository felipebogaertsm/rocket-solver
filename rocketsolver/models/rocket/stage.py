"""
Defines the stage class for the rocket model.
"""

from rocketsolver.models.rocket.fuselage import Fuselage
from rocketsolver.models.propulsion import Motor
from rocketsolver.models.recovery import Recovery


class RocketStage:
    """
    Defines a stage of a rocket.
    """

    def __init__(
        self,
        propulsion: Motor,
        fuselage: Fuselage,
        recovery: Recovery,
        mass_without_motor: float,
    ) -> None:
        """
        Initializes a RocketStage object.

        Args:
            propulsion(Motor): The motor or propulsion system of the rocket.
            recovery(Recovery): The recovery system of the rocket.
            fuselage(Fuselage): The fuselage or body of the rocket.
            mass_without_motor(float): The mass of the rocket without the motor,
                in kg.
        """
        self.propulsion = propulsion
        self.recovery = recovery
        self.fuselage = fuselage
        self.mass_without_motor = mass_without_motor
