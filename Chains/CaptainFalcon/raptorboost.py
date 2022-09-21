from melee.enums import Character

from Chains.Abstract import SideSlide
from Utils import Trajectory


class RaptorBoost(SideSlide):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 30, -999, -64, "Data/Trajectories/raptor_boost.csv")

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        return cls.TRAJECTORY