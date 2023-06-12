from melee.enums import Character

from Chains.Abstract import FireAnimal
from Utils import Trajectory


class FireFox(FireAnimal):
    TRAJECTORY = Trajectory(Character.FOX, "FireFox")

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY

    @classmethod
    def _get_launch_end_frame(cls):
        return 72