from melee.enums import Character

from Chains.Abstract import RecoveryChain
from Utils import Trajectory


class DancingBlade(RecoveryChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.FOX, 0, 15, -999, 999, "Data/Trajectories/fox_illusion.csv")

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        return cls._adjust_trajectory(cls.TRAJECTORY.copy(), x_velocity)

    @classmethod
    def _get_shorten_frame(cls):
        return 19
