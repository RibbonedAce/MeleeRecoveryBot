import math
from abc import ABCMeta

from Tactics.Abstract.abstractrecover import AbstractRecover
from Utils import AngleUtils, ControlStick, MathUtils


class SpacieRecover(AbstractRecover, metaclass=ABCMeta):
    @classmethod
    def _get_primary_recovery_trajectory(cls, smashbot_state, stage_edge):
        angle_to_ledge = AngleUtils.correct_for_cardinal(math.degrees(math.atan2(-smashbot_state.position.y, abs(smashbot_state.position.x) - stage_edge)))
        min_angle = ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_angle()
        test_angle = max(angle_to_ledge, min_angle)
        return cls._get_primary_recovery_class().create_trajectory(smashbot_state, smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x), test_angle)