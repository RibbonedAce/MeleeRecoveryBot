from collections import defaultdict

from melee import FrameData

from Utils.enums import FRAME_INPUT_TYPE, LEDGE_GRAB_MODE
from Utils.frameinput import FrameInput
from Utils.logutils import LogUtils
from Utils.trajectoryframe import TrajectoryFrame
from Utils.vector2 import Vector2


class Trajectory:
    TOO_LOW_RESULT = -100

    @staticmethod
    def create_drift_trajectory(character):
        return Trajectory(character, 0, 0, LEDGE_GRAB_MODE.ALWAYS, False, [TrajectoryFrame.drift(character)])

    def __init__(self, character, ascent_start, descent_start, ledge_grab_mode, requires_extra_height, frames):
        self.character = character
        self.ascent_start = ascent_start
        self.descent_start = descent_start
        self.ledge_grab_mode = ledge_grab_mode
        self.frames = frames
        self.requires_extra_height = requires_extra_height
        self.max_height = self.__calculate_max_height()
        self.height_displacement = self.__calculate_height_displacement()

    def get_extra_distance(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        max_distance = self.get_distance(propagate, target, ledge, frame_range, position, velocity, knockback, input_frames)
        if max_distance == Trajectory.TOO_LOW_RESULT:
            return Trajectory.TOO_LOW_RESULT

        required_distance = position.x - target.x
        if max_distance - required_distance > 0:
            LogUtils.simple_log("Trajectory Data:", ledge, position, target.x, max_distance - required_distance)
        return max_distance - required_distance

    def get_distance(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None):
        game_state, smashbot_state, opponent_state = propagate
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        ledge_box = FrameData.INSTANCE.get_ledge_box(self.character)
        relative_target = Vector2(position.x - target.x, target.y - position.y)
        stage_vertex = game_state.get_relative_stage_vertex(position)

        total_distance = Trajectory.TOO_LOW_RESULT
        actual_distance = 0
        actual_height = 0

        for i in frame_range:
            frame = self.frames[min(i, len(self.frames) - 1)]
            s_input = self.__get_stick_input(input_frames[i], frame, velocity)

            velocity = frame.velocity(velocity, s_input)
            knockback = knockback.with_advanced_frames(1)
            actual_x_velocity = velocity.x + knockback.get_x()

            actual_distance += actual_x_velocity
            actual_height += velocity.y + knockback.get_y()

            # If we pineapple, back out early
            if stage_vertex is not None and actual_distance > stage_vertex.x and actual_height < stage_vertex.y:
                LogUtils.simple_log("Hit vertex", i, actual_distance, actual_height, stage_vertex)
                return Trajectory.TOO_LOW_RESULT

            if ledge:
                extra_height = ledge_box.top
                if actual_x_velocity < 0 and actual_height + max(ledge_box.bottom, frame.ecb.y) >= relative_target.y:
                    extra_height = max(ledge_box.bottom, frame.ecb.y)
                # If a recovery is prone to getting battlefielded, we need a bit more vertical distance
                if self.requires_extra_height and actual_x_velocity >= 0:
                    extra_height -= 2
                extra_distance = ledge_box.horizontal + frame.ecb.x
            else:
                extra_height = frame.ecb.y
                extra_distance = 0

            if i >= self.ascent_start and actual_height + extra_height >= relative_target.y and (not ledge or
                    self.ledge_grab_mode == LEDGE_GRAB_MODE.ALWAYS or
                    self.ledge_grab_mode == LEDGE_GRAB_MODE.AFTER and i >= len(self.frames) - 1 or
                    self.ledge_grab_mode == LEDGE_GRAB_MODE.DURING and i < len(self.frames) - 1):
                total_distance = actual_distance + extra_distance
            elif i >= len(self.frames) - 1 and ledge and self.ledge_grab_mode == LEDGE_GRAB_MODE.DURING and \
                    actual_height + max(ledge_box.bottom, frame.ecb.y) > relative_target.y:
                return Trajectory.TOO_LOW_RESULT
            elif i >= self.descent_start and actual_height + extra_height < relative_target.y:
                if actual_x_velocity < 0 and total_distance != Trajectory.TOO_LOW_RESULT:
                    total_distance = actual_distance + extra_distance
                break

        return total_distance

    def get_distance_traveled_above_target(self, propagate, target=Vector2.zero(), ledge=False, frame_range=range(600), position=None, velocity=None, knockback=None, input_frames=None):
        game_state, smashbot_state, opponent_state = propagate
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)

        relative_target = Vector2(position.x - target.x, target.y - position.y)
        stage_vertex = game_state.get_relative_stage_vertex(position)

        total_distance = Trajectory.TOO_LOW_RESULT
        actual_distance = 0
        actual_height = 0
        hit_height = False

        for i in frame_range:
            frame = self.frames[min(i, len(self.frames) - 1)]
            s_input = self.__get_stick_input(input_frames[i], frame, velocity)

            velocity = frame.velocity(velocity, s_input)
            knockback = knockback.with_advanced_frames(1)
            actual_x_velocity = velocity.x + knockback.get_x()

            actual_distance += actual_x_velocity
            actual_height += velocity.y + knockback.get_y()

            # If we pineapple, back out early
            if stage_vertex is not None and actual_distance > stage_vertex.x and actual_height < stage_vertex.y:
                LogUtils.simple_log("Hit vertex", i, actual_distance, actual_height, stage_vertex)
                return Trajectory.TOO_LOW_RESULT

            extra_height = frame.ecb.y
            if not hit_height and actual_height + extra_height >= relative_target.y:
                hit_height = True

            if actual_height + extra_height >= relative_target.y:
                total_distance += actual_x_velocity
            elif actual_height + extra_height < relative_target.y and i >= self.descent_start:
                if not hit_height:
                    return Trajectory.TOO_LOW_RESULT
                break

        return total_distance

    def get_displacement_after_frames(self, propagate, target=Vector2.zero(), ledge=False, frame_range=None, position=None, velocity=None, knockback=None, input_frames=None):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)
        if frame_range is None:
            frame_range = range(len(self.frames))

        displacement = Vector2.zero()
        for i in frame_range:
            frame = self.frames[min(i, len(self.frames) - 1)]
            s_input = self.__get_stick_input(input_frames[i], frame, velocity)
            velocity = frame.velocity(velocity, s_input)
            displacement += frame.velocity(velocity, s_input)

        return displacement + knockback.get_total_displacement(len(frame_range))

    def get_velocity_after_frames(self, propagate, target=Vector2.zero(), ledge=False, frame_range=None, position=None, velocity=None, knockback=None, input_frames=None):
        position, velocity, knockback, input_frames = self.__fill_out_empties(propagate, position, velocity, knockback, input_frames)
        if frame_range is None:
            frame_range = range(len(self.frames))

        for i in frame_range:
            frame = self.frames[min(i, len(self.frames) - 1)]
            s_input = self.__get_stick_input(input_frames[i], frame, velocity)
            velocity = frame.velocity(velocity, s_input)

        return velocity

    def __fill_out_empties(self, propagate, position, velocity, knockback, input_frames):
        game_state, smashbot_state, opponent_state = propagate

        if position is None:
            position = smashbot_state.get_relative_position()
        if velocity is None:
            velocity = smashbot_state.get_relative_velocity()
        if knockback is None:
            knockback = smashbot_state.get_relative_knockback(opponent_state)
        if input_frames is None:
            input_frames = defaultdict(lambda: FrameInput.forward())

        return position, velocity, knockback, input_frames

    def __get_stick_input(self, f_input, frame, velocity):
        sort_key = lambda k: frame.velocity(velocity, k).x
        s_input = f_input.s_input
        if f_input.f_type == FRAME_INPUT_TYPE.FADE_FORWARD:
            s_input = max(Vector2(1, 0), Vector2(0, 0), key=sort_key)
        elif f_input.f_type == FRAME_INPUT_TYPE.FADE_BACKWARD:
            s_input = min(Vector2(-1, 0), Vector2(0, 0), key=sort_key)
        return s_input

    def __calculate_max_height(self):
        velocity = Vector2.zero()
        actual_height = 0
        max_height = 0

        for frame in self.frames:
            velocity = frame.velocity(velocity, Vector2(0, 1))
            actual_height += velocity.y
            max_height = max(actual_height, max_height)

        return max_height

    def __calculate_height_displacement(self):
        velocity = Vector2.zero()
        actual_height = 0

        for frame in self.frames:
            velocity = frame.velocity(velocity, Vector2(0, 1))
            actual_height += velocity.y

        return actual_height