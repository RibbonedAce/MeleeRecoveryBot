from melee.enums import Character

from Chains.Abstract import ElementalDive
from Utils import Trajectory


class FalconDive(ElementalDive):
    TRAJECTORY = Trajectory(Character.CPTFALCON, "FalconDive.Normal")
    REVERSE_TRAJECTORY = Trajectory(Character.CPTFALCON, "FalconDive.Reverse")

    @classmethod
    def _get_normal_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_reverse_trajectory(cls):
        return cls.REVERSE_TRAJECTORY