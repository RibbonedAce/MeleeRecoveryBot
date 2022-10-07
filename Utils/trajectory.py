import csv
import math

from melee import FrameData

from Utils.angleutils import AngleUtils
from Utils.logutils import LogUtils
from Utils.trajectoryframe import TrajectoryFrame


class Trajectory:
    TOO_LOW_RESULT = -100

    @staticmethod
    def create_drift_trajectory(character, start_velocity):
        frames = Trajectory.create_trajectory_frames(character, start_velocity)
        return Trajectory(character, 0, 0, -999, 999, False, frames)

    @staticmethod
    def create_trajectory_frames(character, start_velocity):
        gravity = -FrameData.INSTANCE.get_gravity(character)
        mobility = FrameData.INSTANCE.get_air_mobility(character)
        speed = FrameData.INSTANCE.get_air_speed(character)
        velocity = start_velocity
        frames = []
        term_velocity = min(-FrameData.INSTANCE.get_terminal_velocity(character), start_velocity)

        while velocity != term_velocity or len(frames) == 0:
            velocity = max(velocity + gravity, term_velocity)
            frames.append(TrajectoryFrame(
                vertical_velocity=velocity,
                forward_acceleration=mobility,
                backward_acceleration=-mobility,
                max_horizontal_velocity=speed,
                min_horizontal_velocity=-speed))

        return frames

    @staticmethod
    def create_jump_trajectory_frames(character):
        gravity = -FrameData.INSTANCE.get_gravity(character)
        mobility = FrameData.INSTANCE.get_air_mobility(character)
        velocity = FrameData.INSTANCE.get_dj_speed(character)[1]
        frames = []
        term_velocity = -FrameData.INSTANCE.get_terminal_velocity(character)

        while velocity != term_velocity or len(frames) == 0:
            if len(frames) == 0:
                speed = FrameData.INSTANCE.get_air_speed(character)
            else:
                speed = FrameData.INSTANCE.get_dj_speed(character)[0]

            velocity = max(velocity + gravity, term_velocity)
            frames.append(TrajectoryFrame(
                vertical_velocity=velocity,
                forward_acceleration=mobility,
                backward_acceleration=-mobility,
                max_horizontal_velocity=speed,
                min_horizontal_velocity=-speed))

        return frames

    @staticmethod
    def from_csv_file(character, ascent_start, descent_start, min_ledge_grab, max_ledge_grab, path, requires_extra_height=False, include_fall_frames=True):
        frames = []
        with open(path) as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            # Build a series of nested dicts for faster read access
            for row in csv_reader:
                mid_horizontal_velocity = None
                if row["mid_horizontal_velocity"] != "":
                    mid_horizontal_velocity = float(row["mid_horizontal_velocity"])

                # Pull out the frame
                frame = TrajectoryFrame(
                    float(row["vertical_velocity"]),
                    float(row["forward_acceleration"]),
                    float(row["backward_acceleration"]),
                    float(row["max_horizontal_velocity"]),
                    mid_horizontal_velocity,
                    float(row["min_horizontal_velocity"]),
                    float(row["ecb_bottom"]),
                    float(row["ecb_inward"]))

                frames.append(frame)

        if include_fall_frames:
            frames += Trajectory.create_trajectory_frames(character, frames[-1].vertical_velocity)

        return Trajectory(character, ascent_start, descent_start, min_ledge_grab, max_ledge_grab, requires_extra_height, frames)

    def __init__(self, character, ascent_start, descent_start, min_ledge_grab, max_ledge_grab, requires_extra_height, frames):
        self.character = character
        self.ascent_start = ascent_start
        self.descent_start = descent_start
        self.min_ledge_grab = min_ledge_grab
        self.max_ledge_grab = max_ledge_grab
        self.frames = frames
        self.requires_extra_height = requires_extra_height

    def copy(self):
        return Trajectory(self.character, self.ascent_start, self.descent_start, self.min_ledge_grab, self.max_ledge_grab, self.requires_extra_height, [f.copy() for f in self.frames])

    def get_max_height(self):
        max_height = 0
        actual_height = 0

        for frame in self.frames:
            actual_height += frame.vertical_velocity
            max_height = max(actual_height, max_height)

        return max_height


    def get_extra_distance(self, game_state, smashbot_state, opponent_state, target, ledge=False, frame_delay=0, start_frame=0, stall_class=None):
        knockback_angle = smashbot_state.get_knockback_angle(opponent_state)
        if smashbot_state.position.x > 0:
            knockback_angle = AngleUtils.get_x_reflection(knockback_angle)
        knockback_magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

        velocity = smashbot_state.get_inward_x_velocity()
        if stall_class is None:
            drift_trajectory = Trajectory.create_drift_trajectory(self.character, smashbot_state.speed_y_self)
        else:
            drift_trajectory = stall_class.create_stall_drift_trajectory(game_state, smashbot_state, velocity, smashbot_state.speed_y_self)

        displacement = drift_trajectory.get_displacement_after_frames(velocity, frame_delay, knockback_angle, knockback_magnitude)
        position = abs(smashbot_state.position.x) - displacement[0]
        height = smashbot_state.position.y + displacement[1]
        stage_vertex = self.get_relative_stage_vertex(game_state, position, height)

        for i in range(frame_delay):
            knockback_magnitude = max(knockback_magnitude - 0.051, 0)
            acceleration = min(FrameData.INSTANCE.get_air_mobility(smashbot_state.character),
                               max(FrameData.INSTANCE.get_air_speed(smashbot_state.character) - velocity,
                                   -FrameData.INSTANCE.get_air_friction(smashbot_state.character)))
            velocity += acceleration

        max_distance = self.get_distance_at_height(velocity, target[1] - height, stage_vertex, ledge, knockback_angle, knockback_magnitude, start_frame)
        if max_distance == Trajectory.TOO_LOW_RESULT:
            return Trajectory.TOO_LOW_RESULT
        actual_distance = position - target[0]
        if max_distance - actual_distance > 0:
            LogUtils.simple_log(ledge, position, target[0], max_distance - actual_distance)
        return max_distance - actual_distance

    def get_distance_at_height(self, current_velocity, height, stage_vertex=None, ledge=False, knockback_angle=0, knockback_magnitude=0, start_frame=0):
        if ledge:
            actual_height = height - FrameData.INSTANCE.get_ledge_box_top(self.character)
            if actual_height < self.min_ledge_grab:
                LogUtils.simple_log("Too high:", actual_height, self.min_ledge_grab)
                return Trajectory.TOO_LOW_RESULT
            elif actual_height > self.max_ledge_grab:
                LogUtils.simple_log("Too low:", actual_height, self.max_ledge_grab)
                return Trajectory.TOO_LOW_RESULT

        return self.get_distance(current_velocity, height, stage_vertex, ledge, knockback_angle, knockback_magnitude, start_frame=start_frame)

    def get_last_frame_at_height(self, height):
        actual_height = 0
        frame_number = 500
        need_to_update = True

        for i in range(0, 500):
            actual_height += self.frames[min(i, len(self.frames) - 1)].vertical_velocity
            if actual_height <= height and need_to_update:
                frame_number = i - 1
                need_to_update = False
            elif actual_height > height and not need_to_update:
                need_to_update = True
            if actual_height <= height and i >= self.descent_start:
                break

        return frame_number

    def get_distance(self, current_velocity, height, stage_vertex, ledge=False, knockback_angle=0, knockback_magnitude=0, fade_back_frames=None, start_frame=0):
        if fade_back_frames is None:
            fade_back_frames = set()

        total_distance = Trajectory.TOO_LOW_RESULT
        actual_distance = 0
        actual_height = 0
        drag = FrameData.INSTANCE.get_air_friction(self.character)
        velocity = current_velocity

        ledge_box_top = FrameData.INSTANCE.get_ledge_box_top(self.character)
        ledge_box_bottom = FrameData.INSTANCE.get_ledge_box_bottom(self.character)
        ledge_box_horizontal = FrameData.INSTANCE.get_ledge_box_horizontal(self.character)

        for i in range(start_frame, 600):
            frame = self.frames[min(i, len(self.frames) - 1)]

            if i in fade_back_frames:
                acceleration = max(frame.backward_acceleration, min(frame.min_horizontal_velocity - velocity, drag))
                if frame.min_horizontal_velocity == frame.max_horizontal_velocity:
                    acceleration = frame.min_horizontal_velocity - velocity

                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = min(velocity, frame.mid_horizontal_velocity)

            else:
                acceleration = min(frame.forward_acceleration, max(frame.max_horizontal_velocity - velocity, -drag))
                if frame.min_horizontal_velocity == frame.max_horizontal_velocity:
                    acceleration = frame.max_horizontal_velocity - velocity

                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = max(velocity, frame.mid_horizontal_velocity)

            knockback_magnitude = max(knockback_magnitude - 0.051, 0)
            extra_velocity = math.cos(math.radians(knockback_angle)) * knockback_magnitude
            actual_distance += velocity + extra_velocity
            actual_height += frame.vertical_velocity + math.sin(math.radians(knockback_angle)) * knockback_magnitude

            # If we pineapple, back out early
            if stage_vertex is not None and actual_distance > stage_vertex[0] and actual_height < stage_vertex[1]:
                return Trajectory.TOO_LOW_RESULT

            if ledge:
                extra_height = ledge_box_top
                if velocity + extra_velocity < 0 and actual_height + max(ledge_box_bottom, frame.ecb_bottom) >= height:
                    extra_height = max(ledge_box_bottom, frame.ecb_bottom)
                # If a recovery is prone to getting battlefielded, we need a bit more vertical distance
                if self.requires_extra_height and velocity + extra_velocity >= 0:
                    extra_height -= 2
                extra_distance = ledge_box_horizontal + frame.ecb_inward
            else:
                extra_height = frame.ecb_bottom
                extra_distance = 0

            if i >= self.ascent_start and actual_height + extra_height >= height:
                total_distance = actual_distance + extra_distance
            elif i >= self.descent_start:
                if velocity + extra_velocity < 0 and total_distance != Trajectory.TOO_LOW_RESULT:
                    total_distance = actual_distance + extra_distance
                break

        return total_distance

    def get_relative_stage_vertex(self, game_state, position, height):
        stage_vertex = game_state.get_stage_ride_vertex()
        stage_vertex = (position - stage_vertex[0], stage_vertex[1] - height)
        return stage_vertex

    def get_distance_traveled_above_target(self, current_velocity, target, stage_vertex, knockback_angle=0, knockback_magnitude=0, start_frame=0):
        total_distance = 0
        actual_distance = 0
        actual_height = 0
        drag = FrameData.INSTANCE.get_air_friction(self.character)
        velocity = current_velocity

        for i in range(start_frame, 600):
            frame = self.frames[min(i, len(self.frames) - 1)]

            acceleration = min(frame.forward_acceleration, max(frame.max_horizontal_velocity - velocity, -drag))
            if frame.min_horizontal_velocity == frame.max_horizontal_velocity:
                acceleration = frame.min_horizontal_velocity - velocity

            velocity += acceleration
            if frame.mid_horizontal_velocity is not None:
                velocity = max(velocity, frame.mid_horizontal_velocity)

            knockback_magnitude = max(knockback_magnitude - 0.051, 0)
            extra_velocity = math.cos(math.radians(knockback_angle)) * knockback_magnitude
            actual_distance += velocity + extra_velocity
            actual_height += frame.vertical_velocity + math.sin(math.radians(knockback_angle)) * knockback_magnitude
            extra_height = frame.ecb_bottom

            # If we pineapple, back out early
            if stage_vertex is not None and actual_distance > stage_vertex[0] and actual_height < stage_vertex[1]:
                LogUtils.simple_log("Hit vertex", i, actual_distance, actual_height, target, stage_vertex)
                return Trajectory.TOO_LOW_RESULT

            if actual_height + extra_height < target[1] and i >= self.descent_start:
                if velocity + extra_velocity < 0:
                    total_distance += velocity + extra_velocity
                break

            elif actual_height + extra_height >= target[1] or actual_distance < target[0]:
                total_distance += velocity + extra_velocity

        return total_distance

    def get_displacement_after_frames(self, current_velocity, num_frames, knockback_angle=0, knockback_magnitude=0, fade_back_frames=None):
        if fade_back_frames is None:
            fade_back_frames = set()

        actual_distance = 0
        actual_height = 0
        drag = FrameData.INSTANCE.get_air_friction(self.character)
        velocity = current_velocity

        for i in range(num_frames):
            frame = self.frames[min(i, len(self.frames) - 1)]

            if i in fade_back_frames:
                acceleration = max(frame.backward_acceleration, min(frame.min_horizontal_velocity - velocity, drag))
                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = min(velocity, frame.mid_horizontal_velocity)

            else:
                acceleration = min(frame.forward_acceleration, max(frame.max_horizontal_velocity - velocity, -drag))
                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = max(velocity, frame.mid_horizontal_velocity)

            knockback_magnitude = max(knockback_magnitude - 0.051, 0)
            actual_distance += velocity + math.cos(math.radians(knockback_angle)) * knockback_magnitude
            actual_height += frame.vertical_velocity + math.sin(math.radians(knockback_angle)) * knockback_magnitude

        return actual_distance, actual_height
