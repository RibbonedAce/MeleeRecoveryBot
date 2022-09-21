from melee.enums import Character

from Chains.Abstract import FireAnimal
from Utils import Trajectory


class FireFox(FireAnimal):
    TRAJECTORY = Trajectory.from_csv_file(Character.FOX, 42, 78, -999, 999, "Data/Trajectories/fire_fox.csv", requires_extra_height=True, include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        return cls._adjust_trajectory(cls.TRAJECTORY.copy(), smashbot_state, x_velocity, angle)

    @classmethod
    def _get_fire_travel_deceleration(cls):
        return 0.1

    @classmethod
    def _get_fire_travel_deceleration_start_frame(cls):
        return 45

    @classmethod
    def _get_fire_travel_start_speed(cls):
        return 3.8

    @classmethod
    def _get_fire_travel_end_frame(cls):
        return 72