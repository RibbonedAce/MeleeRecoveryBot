from melee.enums import Character

from Chains.Abstract import FireAnimal
from Utils import Trajectory


class FireBird(FireAnimal):
    TRAJECTORY = Trajectory.from_csv_file(Character.FALCO, 42, 70, -999, 999, "Data/fire_bird.csv", requires_extra_height=True, include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        return cls._adjust_trajectory(cls.TRAJECTORY.copy(), smashbot_state, x_velocity, angle)

    @classmethod
    def _get_fire_travel_deceleration(cls):
        return 0.17

    @classmethod
    def _get_fire_travel_slow_start_frame(cls):
        return 43

    @classmethod
    def _get_fire_travel_start_speed(cls):
        return 4.2

    @classmethod
    def _get_fire_travel_end_frame(cls):
        return 64