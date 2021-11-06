import csv
import math

from melee import FrameData

from Utils.angleutils import AngleUtils
from Utils.trajectoryframe import TrajectoryFrame


class Trajectory:
    @staticmethod
    def create_drift_trajectory(character, start_velocity):
        frames = Trajectory.create_trajectory_frames(character, start_velocity)
        return Trajectory(character, 0, -999, 999, False, frames)

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
    def from_csv_file(character, descent_start, min_ledge_grab, max_ledge_grab, path, requires_extra_height=False, include_fall_frames=True):
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

        return Trajectory(character, descent_start, min_ledge_grab, max_ledge_grab, requires_extra_height, frames)

    def __init__(self, character, descent_start, min_ledge_grab, max_ledge_grab, requires_extra_height, frames):
        self.character = character
        self.descent_start = descent_start
        self.min_ledge_grab = min_ledge_grab
        self.max_ledge_grab = max_ledge_grab
        self.frames = frames
        self.requires_extra_height = requires_extra_height
        self.max_height = self.__get_max_height()
        self.max_distance_at_max_height = self.get_distance_at_height(self.max_height, 0)

    def get_extra_distance(self, smashbot_state, opponent_state, target, ledge=False, frame_delay=0):
        knockback_angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(knockback_angle)) > 0:
            knockback_angle = AngleUtils.get_x_reflection(knockback_angle)
        knockback_magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

        drift_trajectory = Trajectory.create_drift_trajectory(self.character, smashbot_state.speed_y_self)
        displacement = drift_trajectory.get_displacement_after_frames(abs(smashbot_state.speed_air_x_self), frame_delay, knockback_angle, knockback_magnitude)
        position = abs(smashbot_state.position.x) + displacement[0]
        height = smashbot_state.position.y + displacement[1]

        for i in range(frame_delay):
            knockback_magnitude = max(knockback_magnitude - 0.051, 0)

        max_distance = self.get_distance_at_height(0, target[1] - height, ledge, knockback_angle, knockback_magnitude)
        actual_distance = position - target[0]
        # if max_distance - actual_distance > 0:
        #     print(ledge, position, target[0], max_distance - actual_distance)
        return max_distance - actual_distance

    def get_distance_at_height(self, current_velocity, height, ledge=False, knockback_angle=0, knockback_magnitude=0):
        if ledge:
            actual_height = height - FrameData.INSTANCE.get_ledge_box_top(self.character)
            if actual_height < self.min_ledge_grab:
                # print("Too high:", actual_height, self.min_ledge_grab)
                return -100
            elif actual_height > self.max_ledge_grab:
                # print("Too low:", actual_height, self.max_ledge_grab)
                return -100

        return self.get_distance(current_velocity, height, ledge, knockback_angle, knockback_magnitude)

    def get_distance(self, current_velocity, height, ledge=False, knockback_angle=0, knockback_magnitude=0, fade_back_frames=None, start_frame=0):
        if fade_back_frames is None:
            fade_back_frames = set()

        total_distance = -100
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
                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = min(velocity, frame.mid_horizontal_velocity)

            else:
                acceleration = min(frame.forward_acceleration, max(frame.max_horizontal_velocity - velocity, -drag))
                velocity += acceleration
                if frame.mid_horizontal_velocity is not None:
                    velocity = max(velocity, frame.mid_horizontal_velocity)

            knockback_magnitude = max(knockback_magnitude - 0.051, 0)
            extra_velocity = math.cos(math.radians(knockback_angle)) * knockback_magnitude
            actual_distance += velocity + extra_velocity
            actual_height += frame.vertical_velocity + math.sin(math.radians(knockback_angle)) * knockback_magnitude

            if ledge:
                extra_height = ledge_box_top
                if velocity + extra_velocity < 0:
                    extra_height = ledge_box_bottom
                # If a recovery is prone to getting battlefielded, we need a bit more vertical distance
                if self.requires_extra_height:
                    extra_height -= 1
                extra_distance = ledge_box_horizontal + frame.ecb_inward
            else:
                extra_height = frame.ecb_bottom
                extra_distance = 0

            if actual_height + extra_height >= height:
                total_distance = actual_distance + extra_distance
            elif i >= self.descent_start:
                if velocity + extra_velocity < 0:
                    total_distance = actual_distance + extra_distance
                break

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

    def __get_max_height(self):
        max_height = 0
        actual_height = 0

        for frame in self.frames:
            actual_height += frame.vertical_velocity
            max_height = max(actual_height, max_height)

        return max_height
