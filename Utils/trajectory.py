from collections import defaultdict

import ctrajectory
from melee import Character, FrameData

from Utils import Angle
from Utils.frameinput import FrameInput
from Utils.logutils import LogUtils
from Utils.vector2 import Vector2


class Trajectory:
    TOO_LOW_RESULT = -100

    DRIFT_TRAJECTORY_DICTIONARY = {
        Character.CPTFALCON: "Drift.CaptainFalcon",
        Character.FOX: "Drift.Fox",
        Character.FALCO: "Drift.Falco",
        Character.GANONDORF: "Drift.Ganondorf",
        Character.MARTH: "Drift.Marth"}

    @classmethod
    def create_drift_trajectory(cls, character):
        return Trajectory(character, cls.DRIFT_TRAJECTORY_DICTIONARY[character])

    def __init__(self, character, nickname):
        self.character = character
        self.nickname = nickname
        self.length = ctrajectory.get_length(nickname)
        self.max_height = ctrajectory.get_max_height(nickname)
        self.stall_height = ctrajectory.get_stall_height(nickname)
        self.height_displacement = ctrajectory.get_height_displacement(nickname)
        self.requires_extra_height = ctrajectory.get_requires_extra_height(nickname)

    def get_extra_distance(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None, ignore_stage_vertex=False):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        max_distance = self.get_distance(propagate, target, ledge, frame_range, position, velocity, knockback, input_frames, ignore_stage_vertex)
        if max_distance == Trajectory.TOO_LOW_RESULT:
            return Trajectory.TOO_LOW_RESULT

        required_distance = position.x - target.x
        if max_distance - required_distance > 0:
            LogUtils.simple_log("Trajectory Data:", ledge, target.x, max_distance - required_distance)
        return max_distance - required_distance

    def get_distance(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None, ignore_stage_vertex=False):
        game_state, smashbot_state, opponent_state = propagate
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        ledge_box = FrameData.INSTANCE.get_ledge_box(self.character)
        relative_target = Vector2(position.x - target.x, target.y - position.y)
        if ignore_stage_vertex:
            stage_vertex = None
        else:
            stage_vertex = game_state.get_relative_stage_vertex(position)

        return ctrajectory.get_distance(self.nickname, relative_target, stage_vertex, ledge, frame_range, velocity, knockback, input_frames, ledge_box)

    def get_distance_traveled_above_target(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None, ignore_stage_vertex=False):
        game_state, smashbot_state, opponent_state = propagate
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        relative_target = Vector2(position.x - target.x, target.y - position.y)
        stage_vertex = game_state.get_relative_stage_vertex(position)
        if ignore_stage_vertex:
            stage_vertex = None

        return ctrajectory.get_distance_traveled_above_target(self.nickname, relative_target, stage_vertex, frame_range, velocity, knockback, input_frames)

    def get_displacement_after_frames(self, propagate, target=Vector2.zero(), ledge=False, frame_range=None, position=None, velocity=None, knockback=None, input_frames=None, ignore_stage_vertex=False):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)
        if frame_range is None:
            frame_range = range(self.length)

        result = ctrajectory.get_displacement_after_frames(self.nickname, frame_range, velocity, knockback, input_frames)
        return Vector2(result[0], result[1])

    def get_velocity_after_frames(self, propagate, target=Vector2.zero(), ledge=False, frame_range=None, position=None, velocity=None, knockback=None, input_frames=None, ignore_stage_vertex=False):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)
        if frame_range is None:
            frame_range = range(self.length)

        result = ctrajectory.get_velocity_after_frames(self.nickname, frame_range, velocity, input_frames)
        return Vector2(result[0], result[1])

    def get_stall_displacement_angle(self, propagate, target=Vector2.zero(), ledge=False, frame_range=None, position=None, velocity=None, knockback=None, input_frames=None, jumps_gained=0, ignore_stage_vertex=False):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)
        if frame_range is None:
            frame_range = range(self.length)

        dj_speed = FrameData.INSTANCE.get_dj_speed(self.character)
        drift_trajectory = self.create_drift_trajectory(self.character)

        return Angle(ctrajectory.get_stall_displacement_angle(self.nickname, drift_trajectory.nickname, frame_range, velocity, knockback, input_frames, jumps_gained, dj_speed))

    def get_fade_back_input(self, velocity, frame_num, should_fade_back):
        return ctrajectory.get_fade_back_input(self.nickname, velocity, frame_num, should_fade_back)

    def __fill_out_empties(self, propagate, position, velocity, knockback, input_frames):
        game_state, smashbot_state, opponent_state = propagate

        if position is None:
            position = smashbot_state.get_relative_position()
        if velocity is None:
            velocity = smashbot_state.get_relative_velocity()
        if knockback is None:
            knockback = smashbot_state.get_relative_knockback(opponent_state)
        if input_frames is None:
            input_frames = defaultdict(FrameInput.forward)

        return position, velocity, knockback, input_frames