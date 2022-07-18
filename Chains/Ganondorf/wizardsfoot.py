from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.Ganondorf import DarkDive
from Utils import Trajectory


class WizardsFoot(DescendingBoot):
    TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 12, -999, 999, "Data/Trajectories/wizards_foot.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_primary_recovery(cls):
        return DarkDive.TRAJECTORY