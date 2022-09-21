import math
from abc import ABCMeta

from Tactics.Abstract.abstractrecover import AbstractRecover
from Utils import AngleUtils, ControlStick


class SpacieRecover(AbstractRecover, metaclass=ABCMeta):
    @classmethod
    def _get_primary_recovery_trajectory(cls, game_state, smashbot_state):
        angle_to_ledge = AngleUtils.correct_for_cardinal(math.degrees(math.atan2(-smashbot_state.position.y, abs(smashbot_state.position.x) - game_state.get_stage_edge())))
        min_angle = ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_angle()
        test_angle = max(angle_to_ledge, min_angle)
        return cls._get_primary_recovery_class().create_trajectory(game_state, smashbot_state, smashbot_state.get_inward_x_velocity(), test_angle)