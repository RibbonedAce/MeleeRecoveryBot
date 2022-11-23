from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.Ganondorf import DarkDive
from Utils import Trajectory


class WizardsFoot(DescendingBoot):
    TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 12, -999, 999, "Data/Trajectories/wizards_foot.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, x_velocity, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return DarkDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return len(cls.TRAJECTORY.frames)
