from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory


class FalcoPhantasm(SpacieApparition):
    FULL_TRAJECTORY = Trajectory(Character.FALCO, "FalcoPhantasm.Full")
    LONG_TRAJECTORY = Trajectory(Character.FALCO, "FalcoPhantasm.Long")
    MID_TRAJECTORY = Trajectory(Character.FALCO, "FalcoPhantasm.Mid")
    SLOW_SHORT_TRAJECTORY = Trajectory(Character.FALCO, "FalcoPhantasm.SlowShort")
    FAST_SHORT_TRAJECTORY = Trajectory(Character.FALCO, "FalcoPhantasm.FastShort")

    @classmethod
    def create_trajectory(cls, character):
        return cls.FULL_TRAJECTORY

    @classmethod
    def create_shorten_trajectory(cls, amount):
        if amount == 1:
            return cls.LONG_TRAJECTORY
        if amount == 2:
            return cls.MID_TRAJECTORY
        if amount == 3:
            return cls.SLOW_SHORT_TRAJECTORY
        if amount == 4:
            return cls.FAST_SHORT_TRAJECTORY
        return cls.FULL_TRAJECTORY

    @classmethod
    def _get_shorten_frame(cls):
        return 15