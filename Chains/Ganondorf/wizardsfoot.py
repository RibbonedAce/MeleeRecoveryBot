from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.Ganondorf import DarkDive
from Utils import Trajectory


class WizardsFoot(DescendingBoot):
    TRAJECTORY = Trajectory(Character.GANONDORF, "WizardsFoot")

    @classmethod
    def create_trajectory(cls, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return DarkDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls, charge):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return cls.TRAJECTORY.length
