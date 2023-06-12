from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.CaptainFalcon.falcondive import FalconDive
from Utils import Trajectory


class FalconKick(DescendingBoot):
    TRAJECTORY = Trajectory(Character.CPTFALCON, "FalconKick")

    @classmethod
    def create_trajectory(cls, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return FalconDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls, charge):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return cls.TRAJECTORY.length
