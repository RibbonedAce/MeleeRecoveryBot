from melee.enums import Character

from Chains.Abstract import ElementalDive
from Utils import Trajectory


class DarkDive(ElementalDive):
    TRAJECTORY = Trajectory(Character.GANONDORF, "DarkDive.Normal")
    REVERSE_TRAJECTORY = Trajectory(Character.GANONDORF, "DarkDive.Reverse")

    @classmethod
    def _get_normal_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_reverse_trajectory(cls):
        return cls.REVERSE_TRAJECTORY