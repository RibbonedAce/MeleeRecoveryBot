from melee.enums import Character

from Chains.Abstract import FireAnimal
from Utils import Trajectory


class FireBird(FireAnimal):
    TRAJECTORY = Trajectory(Character.FALCO, "FireBird")

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY

    @classmethod
    def _get_launch_end_frame(cls):
        return 64