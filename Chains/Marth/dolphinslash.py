import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import AngleUtils, ControlStick, LogUtils, MathUtils, Trajectory, TrajectoryFrame
from Utils.enums import FADE_BACK_MODE


class DolphinSlash(RecoveryChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.MARTH, 5, 20, -999, 999, "Data/Trajectories/dolphin_slash.csv", include_fall_frames=False)
    ANGLES_TO_TEST = [ControlStick.from_angle(0).to_edge_coordinate(True),
                      ControlStick.from_angle(90).to_edge_coordinate(True),
                      ControlStick.from_angle(135).to_edge_coordinate(True)]

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = MathUtils.sign(x_velocity) * max(0.666 * abs(x_velocity) - 0.05, 0)

        for i in range(5):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = MathUtils.sign(x_velocity) * max(abs(x_velocity) - 0.05, 0)

        for i in range(5, 22):
            frame_magnitude = (trajectory.frames[i].max_horizontal_velocity ** 2 + trajectory.frames[i].vertical_velocity ** 2) ** 0.5
            frame_angle = math.degrees(math.atan2(trajectory.frames[i].vertical_velocity, trajectory.frames[i].max_horizontal_velocity))
            frame_angle -= angle
            if frame_angle > 90:
                frame_angle = 180 - frame_angle
            x_angle = math.cos(math.radians(frame_angle))
            y_angle = math.sin(math.radians(frame_angle))

            trajectory.frames[i].vertical_velocity = y_angle * frame_magnitude
            trajectory.frames[i].min_horizontal_velocity = x_angle * frame_magnitude
            trajectory.frames[i].max_horizontal_velocity = x_angle * frame_magnitude
            trajectory.frames[i].forward_acceleration = x_angle * frame_magnitude - trajectory.frames[i - 1].max_horizontal_velocity
            trajectory.frames[i].backward_acceleration = x_angle * frame_magnitude - trajectory.frames[i - 1].min_horizontal_velocity

        for i in range(22, 39):
            trajectory.frames[i].vertical_velocity = trajectory.frames[i - 1].vertical_velocity - 0.06

        gravity = -FrameData.INSTANCE.get_gravity(smashbot_state.character)
        mobility = FrameData.INSTANCE.get_air_mobility(smashbot_state.character)
        speed = trajectory.frames[38].max_horizontal_velocity
        velocity = trajectory.frames[38].vertical_velocity
        term_velocity = -2.5

        while velocity != term_velocity:
            velocity = max(velocity + gravity, term_velocity)
            trajectory.frames.append(TrajectoryFrame(
                vertical_velocity=velocity,
                forward_acceleration=mobility,
                backward_acceleration=-mobility,
                max_horizontal_velocity=speed,
                min_horizontal_velocity=-speed))

        return trajectory

    @classmethod
    def __convert_to_recovery_angle(cls, coord):
        control_stick_angle = ControlStick.coordinate_num_to_angle(coord)
        x_value = math.cos(math.radians(control_stick_angle))
        return MathUtils.i_lerp(0.5, 1, abs(x_value)) * MathUtils.sign(x_value) * 20

    def __init__(self, target_coords, recovery_target):
        RecoveryChain.__init__(self, target_coords, recovery_target)
        self.best_angle = ControlStick.from_angle(0).to_edge_coordinate(True)
        self.best_distance = None
        self.start_x_velocity = 0

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        useful_x_velocity = smashbot_state.get_inward_x_velocity()
        if self.trajectory is None:
            self.trajectory = self.create_trajectory(game_state, smashbot_state, useful_x_velocity, self.__convert_to_recovery_angle(self.ANGLES_TO_TEST[0]))

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.SHINE_RELEASE_AIR, Action.DEAD_FALL]:
            return False

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action != Action.SHINE_RELEASE_AIR:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "smashbot_state.ecb.left", "smashbot_state.ecb.right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        should_fade_back = False
        angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(angle)) > 0:
            angle = AngleUtils.get_x_reflection(angle)
        magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

        # Calculating and applying angle
        if 0 <= self.current_frame < 3:
            self.current_frame += 1

            if self.current_frame == 1:
                controller.release_button(Button.BUTTON_B)

            next_point = self.ANGLES_TO_TEST[min(self.current_frame - 1, len(self.ANGLES_TO_TEST) - 1)]
            current_angle = ControlStick.from_edge_coordinate(next_point).correct_for_cardinal_strict().to_edge_coordinate(True)
            self.trajectory = self.create_trajectory(game_state, smashbot_state, self.start_x_velocity, self.__convert_to_recovery_angle(current_angle))
            fade_back_frames = set()
            if self.recovery_target.fade_back_mode == FADE_BACK_MODE.LATE:
                for i in range(self.current_frame, 600):
                    fade_back_frames.add(i)

            relative_target = (abs(smashbot_state.position.x) - self.target_coords[0], self.target_coords[1] - smashbot_state.position.y)
            stage_vertex = self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y)

            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(useful_x_velocity, relative_target, stage_vertex, angle, magnitude, self.current_frame)
            else:
                recovery_distance = self.trajectory.get_distance(useful_x_velocity, relative_target[1], stage_vertex, self.recovery_target.ledge, angle, magnitude, fade_back_frames, self.current_frame)

            # Record angle
            extra_distance = recovery_distance - (abs(smashbot_state.position.x) - self.target_coords[0])
            LogUtils.simple_log(extra_distance)

            if recovery_distance != Trajectory.TOO_LOW_RESULT:
                # Converge towards minimum distance required
                if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
                    if (self.best_distance is None or extra_distance < self.best_distance) and extra_distance > 0:
                        self.__update_best_angle(current_angle, extra_distance)

                # Converge towards maximum distance
                else:
                    if self.best_distance is None or extra_distance > self.best_distance:
                        self.__update_best_angle(current_angle, extra_distance)

        # Tilt stick in best angle on last frame
        elif self.current_frame == 3:
            self.current_frame += 1
            self.trajectory = self.create_trajectory(game_state, smashbot_state, self.start_x_velocity, self.__convert_to_recovery_angle(self.best_angle))

            if self.best_distance is None:
                self.best_angle = ControlStick.from_edge_coordinate(90).correct_for_cardinal_strict().to_edge_coordinate(True)

            x_input = ControlStick.from_edge_coordinate(self.best_angle).to_smashbot_xy()[0]
            LogUtils.simple_log(x_input)
            controller.tilt_analog(Button.BUTTON_MAIN, (1 - x) + (2 * x - 1) * x_input, 0.5)

        # Tilt stick towards stage to make sure we always face forward
        elif self.current_frame == 4:
            self.current_frame += 1
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)

        # Deciding if we should fade-back
        elif self.current_frame >= 5:
            self.current_frame += 1
            recovery_distance = None

            # See if we can fade back on this frame
            if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
                fade_back_frames = set()
                # If we can make it by fading back this frame, do it
                if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY:
                    fade_back_frames.add(self.current_frame)
                # If we can make it by holding a fade back starting this frame, do it
                elif self.recovery_target.fade_back_mode == FADE_BACK_MODE.LATE:
                    for i in range(self.current_frame, 600):
                        fade_back_frames.add(i)

                recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y), self.recovery_target.ledge, angle, magnitude, fade_back_frames, self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    should_fade_back = True

            frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]

            x_input = x
            if should_fade_back:
                x_input = 1 - x

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle