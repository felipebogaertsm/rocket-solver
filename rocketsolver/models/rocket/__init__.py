import numpy as np

from rocketsolver.models.rocket.stage import RocketStage


class Rocket:
    def __init__(
        self,
        stages: list[RocketStage] | None = None,
    ) -> None:
        """
        Initializes a Rocket object.

        Args:
            stages (list[RocketStage] | None): The list of stages of the rocket.
        """
        self.stages: list[RocketStage] = stages or []

    @property
    def stage_count(self) -> int:
        """
        Get the number of stages of the rocket.

        Returns:
            int: The number of stages of the rocket.
        """
        return len(self.stages)

    def get_launch_mass(self) -> float:
        """
        Calculates the total mass of the rocket at launch.

        Returns:
            float: The total mass of the rocket at launch, in kg.
        """
        return np.sum(
            [
                stage.mass_without_motor + stage.propulsion.get_launch_mass()
                for stage in self.stages
            ]
        )

    def get_dry_mass(self) -> float:
        """
        Calculates the dry mass of the rocket.

        Returns:
            float: The dry mass of the rocket, in kg.
        """
        return np.sum(
            [
                stage.mass_without_motor + stage.propulsion.get_dry_mass()
                for stage in self.stages
            ]
        )
