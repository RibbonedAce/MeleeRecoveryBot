from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.CaptainFalcon.falcondive import FalconDive
from Utils import Trajectory


class FalconKick(DescendingBoot):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 12, -999, 999, "Data/Trajectories/falcon_kick.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_primary_recovery(cls):
        return FalconDive.TRAJECTORY
