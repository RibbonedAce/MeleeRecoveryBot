from melee.enums import Character

from Chains.Abstract import SideSlide
from Utils import Trajectory


class GerudoDragon(SideSlide):
    TRAJECTORY = Trajectory(Character.GANONDORF, "GerudoDragon")

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY