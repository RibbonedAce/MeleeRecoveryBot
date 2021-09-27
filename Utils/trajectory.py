import csv

from Utils.framedatautils import FrameDataUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.trajectoryframe import TrajectoryFrame


class Trajectory:
    @staticmethod
    def from_csv_file(character, descent_start, min_ledge_grab, max_ledge_grab, path):
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

        frames += FrameDataUtils.create_trajectory_frames(character, frames[-1].vertical_velocity)

        return Trajectory(character, descent_start, min_ledge_grab, max_ledge_grab, frames)

    def __init__(self, character, descent_start, min_ledge_grab, max_ledge_grab, frames):
        self.character = character
        self.descent_start = descent_start
        self.min_ledge_grab = min_ledge_grab
        self.max_ledge_grab = max_ledge_grab
        self.frames = frames
        self.max_height = self.__get_max_height()
        self.max_distance_at_max_height = self.get_distance_at_height(self.max_height)

    def get_distance_at_height(self, height, ledge=False):
        if ledge:
            if height < self.min_ledge_grab:
                return -100
            elif height > self.max_ledge_grab:
                return -100

        return self.get_remaining_distance(0, height, ledge)

    def get_remaining_distance(self, current_velocity, height, ledge=False, fade_back_frames=None, start_frame=0):
        if fade_back_frames is None:
            fade_back_frames = set()

        total_distance = -100
        actual_distance = 0
        actual_height = 0
        drag = FrameDataUtils.INSTANCE.characterdata[self.character]["AirFriction"]
        velocity = current_velocity

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

            if i >= start_frame:
                actual_distance += velocity
                actual_height += frame.vertical_velocity

                ecb_height = 0
                if not ledge:
                    ecb_height = frame.ecb_bottom

                if actual_height + ecb_height >= height:
                    total_distance = actual_distance
                elif i >= self.descent_start:
                    if velocity < 0:
                        total_distance = actual_distance
                    break

        return total_distance

    def get_extra_distance(self, smashbot_state, opponent_state, target, ledge=False, frames=1):
        new_position = PlayerStateUtils.get_position_after_drift(smashbot_state, opponent_state, frames)
        knockback = PlayerStateUtils.get_remaining_knockback(smashbot_state, opponent_state)
        position = abs(new_position[0]) + abs(knockback[0])
        height = new_position[1] + knockback[1]

        max_distance = self.get_distance_at_height(target[1] - height, ledge)
        actual_distance = position - target[0]
        return max_distance - actual_distance

    def __get_max_height(self):
        max_height = 0
        actual_height = 0

        for frame in self.frames:
            actual_height += frame.vertical_velocity
            max_height = max(actual_height, max_height)

        return max_height
