from melee.enums import Character

from Chains.Abstract import SideSlide
from Utils import Trajectory


class RaptorBoost(SideSlide):
    TRAJECTORY = Trajectory(Character.CPTFALCON, "RaptorBoost")

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY