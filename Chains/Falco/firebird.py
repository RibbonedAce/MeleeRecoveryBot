import math

from melee.enums import Character

from Chains.Abstract import FireSpacie
from Utils import MathUtils, Trajectory


class FireBird(FireSpacie):
    TRAJECTORY = Trajectory.from_csv_file(Character.FALCO, 42, 70, -999, 999, "Data/fire_bird.csv", requires_extra_height=True, include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = MathUtils.sign(x_velocity) * max(0.8 * abs(x_velocity) - 0.02, 0)

        for i in range(42):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = MathUtils.sign(x_velocity) * max(abs(x_velocity) - 0.02, 0)

        x_angle = math.cos(math.radians(angle))
        y_angle = math.sin(math.radians(angle))
        magnitude = 4.2
        for i in range(42, 64):
            trajectory.frames[i].vertical_velocity = y_angle * magnitude
            trajectory.frames[i].min_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].max_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].forward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].max_horizontal_velocity
            trajectory.frames[i].backward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].min_horizontal_velocity

            if i > 43:
                magnitude = max(magnitude - 0.17, 0)

        for i in range(64, 84):
            trajectory.frames[i].vertical_velocity = max(trajectory.frames[i - 1].vertical_velocity - 0.17, -3.1)

        trajectory.frames += Trajectory.create_trajectory_frames(Character.FALCO, trajectory.frames[83].vertical_velocity)
        return trajectory