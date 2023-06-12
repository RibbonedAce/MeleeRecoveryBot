from abc import ABCMeta

from melee import FrameData

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import Trajectory
from Utils.enums import STALL_MODE


class StallChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, stall_charge) -> Trajectory: ...

    @classmethod
    def min_stall_speed(cls, character):
        return -100

    @classmethod
    def double_jumps_gained(cls):
        return 0

    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        stall_mode = DifficultySettings.STALL
        # If we do not want to stall, do not
        if stall_mode == STALL_MODE.NEVER:
            return False

        # Cannot stall if still in hit-stun
        if smashbot_state.hitstun_frames_left > 0:
            return False

        # Should not stall if facing backwards
        if not smashbot_state.is_facing_inwards() and not cls._can_use_backwards():
            return False

        position = smashbot_state.get_relative_position()
        velocity = smashbot_state.get_relative_velocity()
        knockback = smashbot_state.get_relative_knockback(opponent_state)

        if not cls.position_is_good(propagate, smashbot_state.stall_is_charged(game_state), position, velocity, knockback):
            return False

        # Should not stall if too close unless we want to
        if stall_mode == STALL_MODE.SMART:
            diff_x = position.x - game_state.get_stage_edge()
            diff_y = -position.y
            trajectory = cls.create_trajectory(smashbot_state.stall_is_charged(game_state))
            displacement = trajectory.get_displacement_after_frames(propagate)
            return diff_x >= 40 + displacement.x or diff_y >= 40 + displacement.y

        return True

    @classmethod
    def position_is_good(cls, propagate, charge, position, velocity, knockback):
        smashbot_state = propagate[1]

        # Should not stall if still rising
        if velocity.y > 0:
            return False

        # Should not stall if not high enough to recover after
        if cls.__get_remaining_height(smashbot_state, charge, knockback) + position.y <= 0:
            return False

        # Should not stall if moving too slowly
        if velocity.x < cls.min_stall_speed(smashbot_state.character):
            return False

        stall_angle = cls.create_trajectory(charge).get_stall_displacement_angle(propagate, velocity=velocity, jumps_gained=cls.double_jumps_gained())
        return velocity.x < 0 or velocity.to_angle().get_y() < stall_angle.get_y()

    @classmethod
    def _get_recovery_height(cls) -> float: ...

    @classmethod
    def _get_stall_height_loss(cls, charge) -> float: ...

    @classmethod
    def _get_stall_duration(cls) -> int: ...

    @classmethod
    def _can_use_backwards(cls):
        return True

    @classmethod
    def __get_remaining_height(cls, smashbot_state, charge, knockback):
        return cls._get_stall_height_loss(charge) + knockback.get_total_displacement(cls._get_stall_duration()).y + \
               FrameData.INSTANCE.fast_dj_height(smashbot_state.character) * (cls.double_jumps_gained() + smashbot_state.jumps_left) + \
               cls._get_recovery_height() + FrameData.INSTANCE.get_ledge_box(smashbot_state.character).top - 2 - 2 * FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character)

    def __init__(self):
        Chain.__init__(self)
        self.used_move = False