import math
from abc import ABCMeta

from melee import FrameData

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import AngleUtils, Trajectory
from Utils.enums import STALL_MODE


class StallChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, force_charge=None) -> Trajectory: ...

    @classmethod
    def create_stall_drift_trajectory(cls, game_state, smashbot_state, start_x_velocity, start_y_velocity):
        frames = Trajectory.create_trajectory_frames(smashbot_state.character, start_y_velocity)
        air_speed = cls._min_stall_speed(smashbot_state.character)
        mobility = FrameData.INSTANCE.get_air_mobility(smashbot_state.character)

        num_required = int(max(air_speed - start_x_velocity, 0) // mobility)
        frames = frames[:num_required]
        first_charge = smashbot_state.stall_is_charged(game_state)
        while len(frames) < num_required:
            frames.append(frames[-1])

        new_x_velocity = frames[-1].max_horizontal_velocity if len(frames) > 0 else start_x_velocity
        for i in range(5):
            frames += cls.create_trajectory(game_state, smashbot_state, new_x_velocity, first_charge).frames
            if cls._double_jumps_gained() > 0:
                new_frames = Trajectory.create_jump_trajectory_frames(smashbot_state.character)
            else:
                new_frames = Trajectory.create_trajectory_frames(smashbot_state.character, frames[-1].vertical_velocity)
            num_required = int((air_speed - frames[-1].max_horizontal_velocity) // mobility)
            new_frames = new_frames[:num_required]
            while len(new_frames) < num_required:
                new_frames.append(frames[-1])
            frames += new_frames
            first_charge = False

        return Trajectory(smashbot_state.character, 0, 0, -999, 999, False, frames)

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
        if smashbot_state.facing != (smashbot_state.position.x < 0):
            return False

        diff_x = abs(smashbot_state.position.x) - game_state.get_stage_edge()
        angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(angle)) > 0:
            angle = AngleUtils.get_x_reflection(angle)
        trajectory = cls.create_trajectory(game_state, smashbot_state, smashbot_state.get_inward_x_velocity())
        displacement = trajectory.get_displacement_after_frames(smashbot_state.get_inward_x_velocity(), len(trajectory.frames), angle, smashbot_state.get_knockback_magnitude(opponent_state))

        # Should not stall if too close unless we want to
        if diff_x <= 40 + displacement[0] and stall_mode == STALL_MODE.SMART:
            return False

        # Should not stall if moving too slowly
        if abs(smashbot_state.speed_air_x_self) < cls._min_stall_speed(smashbot_state.character):
            return False

        # Stall if we are high enough
        return smashbot_state.position.y > -displacement[1] - \
               FrameData.INSTANCE.dj_height(smashbot_state) * (cls._double_jumps_gained() + smashbot_state.jumps_left) - \
               cls._get_primary_recovery(game_state, smashbot_state).get_max_height() - FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)

    @classmethod
    def _get_primary_recovery(cls, game_state, smashbot_state) -> Trajectory: ...

    @classmethod
    def _double_jumps_gained(cls) -> int: ...

    @classmethod
    def _min_stall_speed(cls, character) -> float: ...

    def __init__(self):
        Chain.__init__(self)
        self.used_move = False