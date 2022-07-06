from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory


class FalcoPhantasm(SpacieApparition):
    TRAJECTORY = Trajectory.from_csv_file(Character.FALCO, 0, 24, -999, 999, "Data/falco_phantasm.csv")

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        return cls._adjust_trajectory(cls.TRAJECTORY.copy(), x_velocity)

    @classmethod
    def _get_shorten_frame(cls):
        return 15