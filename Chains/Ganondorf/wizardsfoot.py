from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.Ganondorf import DarkDive
from Utils import Trajectory


class WizardsFoot(DescendingBoot):
    TRAJECTORY = Trajectory.from_csv_file(Character.GANONDORF, 0, 12, -999, 999, "Data/Trajectories/wizards_foot.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, force_charge=None):
        return cls.TRAJECTORY

    @classmethod
    def _get_primary_recovery(cls, game_state, smashbot_state):
        return DarkDive.TRAJECTORY