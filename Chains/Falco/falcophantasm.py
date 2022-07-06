from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory


class FalcoPhantasm(SpacieApparition):
    TRAJECTORY = Trajectory.from_csv_file(Character.FALCO, 0, 24, -999, 999, "Data/falco_phantasm.csv")

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = max(2 / 3 * abs(x_velocity) - 0.05, 0)

        for i in range(15):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = max(x_velocity - 0.05, 0)

        return trajectory

    @classmethod
    def create_shorten_trajectory(cls, amount):
        result = cls.TRAJECTORY.copy()

        for i in range(amount):
            result.frames[19-i].forward_acceleration = result.frames[19-i].max_horizontal_velocity - result.frames[17-i].max_horizontal_velocity
            result.frames[19-i].backward_acceleration = result.frames[19-i].min_horizontal_velocity - result.frames[17-i].min_horizontal_velocity
            result.frames.pop(18-i)

        return result