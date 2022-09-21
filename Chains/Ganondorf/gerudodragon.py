from melee.enums import Character

from Chains.Abstract import SideSlide
from Utils import Trajectory


class GerudoDragon(SideSlide):
    TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 30, -999, -64, "Data/Trajectories/gerudo_dragon.csv")

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        return cls.TRAJECTORY