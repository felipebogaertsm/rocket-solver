"""
Defines classes related to the stages of a rocket.
"""

from abc import ABC, abstractmethod

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


class StageSeparationEvent(ABC):
    """
    Defines a stage separation event.
    """

    def __init__(self, trigger_value: float) -> None:
        """
        Initializes a StageSeparationEvent object.

        Args:
            trigger_value(float): The trigger value for the event.
        """
        self.trigger_value = trigger_value

    @abstractmethod
    def is_active(self, time: float) -> bool:
        """
        Checks if the stage separation event is active based on the given conditions.

        Args:
            time(float): The current time.

        Returns:
            bool: True if the stage separation event is active, False otherwise.
        """


class TimeBasedSeparationEvent(StageSeparationEvent):
    """
    Defines a time-based stage separation event.
    """

    def is_active(self, time: float) -> bool:
        """
        The event is considered active if the time is greater than the
        trigger value.

        Args:
            time(float): The time after the motor has finished producing
                thrust.

        Returns:
            bool: True if the stage separation event is active, False
                otherwise.
        """
        return time >= self.trigger_value
