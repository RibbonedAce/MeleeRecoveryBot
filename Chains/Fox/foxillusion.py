from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory


class FoxIllusion(SpacieApparition):
    TRAJECTORY = Trajectory.from_csv_file(Character.FOX, 0, 15, -999, 999, "Data/fox_illusion.csv")

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = max(2 / 3 * abs(x_velocity) - 0.05, 0)

        for i in range(19):
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
            result.frames[23-i].forward_acceleration = result.frames[23-i].max_horizontal_velocity - result.frames[21-i].max_horizontal_velocity
            result.frames[23-i].backward_acceleration = result.frames[23-i].min_horizontal_velocity - result.frames[21-i].min_horizontal_velocity
            result.frames.pop(22-i)

        return result
