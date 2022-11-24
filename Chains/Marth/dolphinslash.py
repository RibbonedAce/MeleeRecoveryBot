import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import ControlStick, LogUtils, MathUtils, Trajectory, TrajectoryFrame
from Utils.enums import FADE_BACK_MODE


class DolphinSlash(RecoveryChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.MARTH, 5, 20, -999, 999, "Data/Trajectories/dolphin_slash.csv", include_fall_frames=False)
    ANGLES_TO_TEST = (ControlStick.from_angle(0).to_edge_coordinate(True),
                      ControlStick.from_angle(90).to_edge_coordinate(True),
                      ControlStick.from_angle(135).to_edge_coordinate(True))

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
        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        inward_x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, (0.5, 1))

        self._increment_current_frame(smashbot_state)
        knockback = smashbot_state.get_relative_knockback(opponent_state)
        inward_x_velocity = smashbot_state.get_inward_x_velocity()

        # Calculating and applying angle
        if 0 < self.current_frame <= 3:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                self.trajectory = self.create_trajectory(game_state, smashbot_state, inward_x_velocity, self.__convert_to_recovery_angle(self.ANGLES_TO_TEST[1]))

            next_point = self.ANGLES_TO_TEST[min(self.current_frame - 1, len(self.ANGLES_TO_TEST) - 1)]
            current_angle = ControlStick.from_edge_coordinate(next_point).correct_for_cardinal_strict().to_edge_coordinate(True)

            # Test current angle in trial
            self.trajectory = self.create_trajectory(game_state, smashbot_state, self.start_x_velocity, self.__convert_to_recovery_angle(current_angle))
            relative_target = (abs(smashbot_state.position.x) - self.target_coords[0], self.target_coords[1] - smashbot_state.position.y)
            stage_vertex = self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y)

            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(inward_x_velocity, relative_target, stage_vertex, knockback, self.current_frame)
            else:
                recovery_distance = self.trajectory.get_distance(inward_x_velocity, relative_target[1], stage_vertex, self.recovery_target.ledge, knockback, self._generate_fade_back_frames(), self.current_frame)

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
        elif self.current_frame == 4:
            self.trajectory = self.create_trajectory(game_state, smashbot_state, self.start_x_velocity, self.__convert_to_recovery_angle(self.best_angle))

            if self.best_distance is None:
                self.best_angle = ControlStick.from_edge_coordinate(90).correct_for_cardinal_strict().to_edge_coordinate(True)

            x_input = ControlStick.from_edge_coordinate(self.best_angle).to_smashbot_xy()[0]
            LogUtils.simple_log(x_input)
            self.controller.tilt_analog(Button.BUTTON_MAIN, (1 - inward_x) + (2 * inward_x - 1) * x_input, 0.5)

        # Tilt stick towards stage to make sure we always face forward
        elif self.current_frame == 5:
            self.controller.tilt_analog(Button.BUTTON_MAIN, inward_x, 0.5)

        # Deciding if we should fade-back
        elif self.current_frame >= 6:
            self._perform_fade_back(game_state, smashbot_state, knockback, inward_x_velocity, inward_x)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.SHINE_RELEASE_AIR, Action.DEAD_FALL}

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle