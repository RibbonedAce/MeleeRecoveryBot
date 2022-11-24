import math
from abc import ABCMeta

from melee import FrameData

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import Trajectory
from Utils.enums import STALL_MODE


class StallChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, x_velocity, stall_charge) -> Trajectory: ...

    @classmethod
    def create_stall_drift_trajectory(cls, game_state, smashbot_state, opponent_state, start_x_velocity, start_y_velocity):
        frames = Trajectory.create_trajectory_frames(smashbot_state.character, start_y_velocity)
        air_speed = cls._min_stall_speed(smashbot_state.character)
        mobility = FrameData.INSTANCE.get_air_mobility(smashbot_state.character)

        new_x_velocity = max(air_speed, start_x_velocity)
        num_required = int(max(air_speed - start_x_velocity, 0) // mobility)
        frames = frames[:num_required]
        while len(frames) < num_required:
            frames.append(frames[-1])

        frames += cls.create_trajectory(new_x_velocity, smashbot_state.stall_is_charged(game_state)).frames

        new_x_velocity = max(air_speed, frames[-1].max_horizontal_velocity)
        no_charge_trajectory = cls.create_trajectory(new_x_velocity, False)
        stall_displacement = no_charge_trajectory.get_displacement_after_frames(new_x_velocity, len(no_charge_trajectory.frames))
        stall_angle = math.atan2(stall_displacement[1], stall_displacement[0])
        jump_frames = Trajectory.create_jump_trajectory_frames(smashbot_state.character)
        regain_speed_frames = Trajectory.create_trajectory_frames(smashbot_state.character, no_charge_trajectory.frames[-1].vertical_velocity)

        if cls._double_jumps_gained() > 0:
            new_frames = jump_frames
        else:
            new_frames = regain_speed_frames

        num_required = int((air_speed - frames[-1].max_horizontal_velocity) // mobility)
        found_angle = False
        for i in range(len(new_frames)):
            if math.atan2(new_frames[i].vertical_velocity, new_frames[i].max_horizontal_velocity) < stall_angle:
                num_required = max(num_required, i)
                found_angle = True
                break
        if not found_angle:
            num_required = len(new_frames)

        new_frames = new_frames[:num_required]
        while len(new_frames) < num_required:
            new_frames.append(frames[-1])

        frames += new_frames

        num_required = int((air_speed - frames[-1].max_horizontal_velocity) // mobility)

        knockback = smashbot_state.get_relative_knockback(opponent_state)
        displacement = Trajectory(smashbot_state.character, 0, 0, -999, 999, False, frames).height_displacement
        remaining_height = cls.__get_remaining_height(smashbot_state.position.y - displacement, smashbot_state, knockback)

        while remaining_height > 0:
            frames += no_charge_trajectory.frames
            if cls._double_jumps_gained() > 0:
                new_frames = jump_frames[:num_required]
            else:
                new_frames = regain_speed_frames[:num_required]

            while len(new_frames) < num_required:
                new_frames.append(frames[-1])

            frames += new_frames

            displacement = Trajectory(smashbot_state.character, 0, 0, -999, 999, False, frames).height_displacement
            remaining_height = cls.__get_remaining_height(smashbot_state.position.y - displacement, smashbot_state, knockback)

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

        # Should not stall if moving too slowly
        if abs(smashbot_state.speed_air_x_self) < cls._min_stall_speed(smashbot_state.character):
            return False

        knockback = smashbot_state.get_relative_knockback(opponent_state)

        # Should not stall if not high enough to recover after
        if cls.__get_remaining_height(smashbot_state.position.y, smashbot_state, knockback) <= 0:
            return False

        # Should not stall if too close unless we want to
        if stall_mode == STALL_MODE.SMART:
            diff_x = abs(smashbot_state.position.x) - game_state.get_stage_edge()
            trajectory = cls.create_trajectory(smashbot_state.get_inward_x_velocity(), smashbot_state.stall_is_charged(game_state))
            displacement = trajectory.get_displacement_after_frames(smashbot_state.get_inward_x_velocity(), len(trajectory.frames), knockback)[0]
            return diff_x <= 40 + displacement

        return True

    @classmethod
    def _get_recovery_height(cls) -> float: ...

    @classmethod
    def _get_stall_height_loss(cls) -> float: ...

    @classmethod
    def _get_stall_duration(cls) -> int: ...

    @classmethod
    def _double_jumps_gained(cls):
        return 0

    @classmethod
    def _min_stall_speed(cls, character):
        return -100

    @classmethod
    def __get_remaining_height(cls, start_height, smashbot_state, knockback):
        return start_height + cls._get_stall_height_loss() + knockback.get_total_displacement(cls._get_stall_duration())[1] + \
               FrameData.INSTANCE.fast_dj_height(smashbot_state) * (cls._double_jumps_gained() + smashbot_state.jumps_left) + \
               cls._get_recovery_height() + FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)

    def __init__(self):
        Chain.__init__(self)
        self.used_move = False