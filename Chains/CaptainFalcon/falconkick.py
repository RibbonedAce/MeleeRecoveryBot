from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.CaptainFalcon.falcondive import FalconDive
from Utils import Trajectory


class FalconKick(DescendingBoot):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 12, -999, 999, "Data/Trajectories/falcon_kick.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, x_velocity, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return FalconDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return len(cls.TRAJECTORY.frames)
