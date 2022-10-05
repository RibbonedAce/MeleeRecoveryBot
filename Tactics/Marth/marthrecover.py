import math

from Chains.Marth import DancingBlade, DolphinSlash
from Tactics.Abstract import AbstractRecover
from Utils import AngleUtils


class MarthRecover(AbstractRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return DolphinSlash

    @classmethod
    def _get_secondary_recovery_class(cls):
        return DolphinSlash

    @classmethod
    def _get_stall_class(cls):
        return DancingBlade

    @classmethod
    def _get_primary_recovery_trajectory(cls, game_state, smashbot_state):
        angle_to_ledge = AngleUtils.correct_for_cardinal(math.degrees(math.atan2(-smashbot_state.position.y, abs(smashbot_state.position.x) - game_state.get_stage_edge())))
        test_angle = min(max(90 - angle_to_ledge, 0), 20)
        return cls._get_primary_recovery_class().create_trajectory(game_state, smashbot_state, smashbot_state.get_inward_x_velocity(), test_angle)