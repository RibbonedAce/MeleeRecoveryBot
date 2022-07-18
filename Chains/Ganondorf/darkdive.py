from melee.enums import Character

from Chains.Abstract import ElementalDive
from Utils import Trajectory


class DarkDive(ElementalDive):
    TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 44, -999, 999, "Data/Trajectories/dark_dive.csv")
    REVERSE_TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 44, 16, 999, "Data/Trajectories/reverse_dark_dive.csv")

    @classmethod
    def _get_normal_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_reverse_trajectory(cls):
        return cls.REVERSE_TRAJECTORY