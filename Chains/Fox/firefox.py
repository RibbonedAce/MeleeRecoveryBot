import copy
import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils.angleutils import AngleUtils
from Utils.controlstick import ControlStick
from Utils.enums import FADE_BACK_MODE
from Utils.hillclimb import HillClimb
from Utils.logutils import LogUtils
from Utils.mathutils import MathUtils
from Utils.trajectory import Trajectory


class FireFox(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.FOX, 42, 78, -999, 999, "Data/fire_fox.csv", requires_extra_height=True, include_fall_frames=False)

    @staticmethod
    def create_trajectory(x_velocity, angle):
        trajectory = copy.deepcopy(FireFox.TRAJECTORY)
        x_velocity = max(0.8 * abs(x_velocity) - 0.02, 0)

        for i in range(42):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = max(x_velocity - 0.02, 0)

        x_angle = math.cos(math.radians(angle))
        y_angle = math.sin(math.radians(angle))
        magnitude = 3.8
        for i in range(42, 72):
            trajectory.frames[i].vertical_velocity = y_angle * magnitude
            trajectory.frames[i].min_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].max_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].forward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].max_horizontal_velocity
            trajectory.frames[i].backward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].min_horizontal_velocity

            if i > 45:
                magnitude = max(magnitude - 0.1, 0)

        for i in range(72, 92):
            trajectory.frames[i].vertical_velocity = max(trajectory.frames[i - 1].vertical_velocity - 0.23, -2.8)

        trajectory.frames += Trajectory.create_trajectory_frames(Character.FOX, trajectory.frames[91].vertical_velocity)
        return trajectory

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), fade_back=FADE_BACK_MODE.NONE, ledge=False):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.fade_back = fade_back
        self.should_sweet_spot = DifficultySettings.should_sweet_spot()
        self.ledge = ledge
        self.current_frame = -1
        self.last_action_frame = -1
        self.min_angle = self.__determine_initial_min_angle()
        self.max_angle = ControlStick(0, ControlStick.MAX_INPUT).to_edge_coordinate(True)
        self.best_angle = ControlStick(ControlStick.MAX_INPUT, 0).to_edge_coordinate(True)
        self.best_distance = None
        self.start_x_velocity = 0
        self.trajectory = None
        self.hill_climb = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FIREFOX_AIR, Action.FIREFOX_WAIT_AIR, Action.SWORD_DANCE_1_AIR, Action.DEAD_FALL]:
            return False

        useful_x_velocity = smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x)
        if self.trajectory is None:
            self.trajectory = FireFox.create_trajectory(useful_x_velocity, ControlStick.coordinate_num_to_angle(self.min_angle))
            self.start_x_velocity = useful_x_velocity
            self.hill_climb = HillClimb(self.min_angle, self.max_angle, 40)

            # If going for ledge and facing backwards, do not go straight up or down
            if (self.ledge or self.should_sweet_spot) and not smashbot_state.is_facing_inwards():
                self.max_angle -= 1
                if self.min_angle < 0:
                    self.min_angle += 1

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action != Action.FIREFOX_WAIT_AIR:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "smashbot_state.ecb_bottom", "smashbot_state.ecb_left", "smashbot_state.ecb_right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        should_fade_back = False
        angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(angle)) > 0:
            angle = AngleUtils.get_x_reflection(angle)
        magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

        # Calculating and applying angle
        if 0 <= self.current_frame < 42:
            if smashbot_state.action_frame != self.last_action_frame:
                self.current_frame += 1
                self.last_action_frame = smashbot_state.action_frame
            controller.release_button(Button.BUTTON_B)

            min_degrees = ControlStick.coordinate_num_to_angle(self.min_angle)
            max_degrees = ControlStick.coordinate_num_to_angle(self.max_angle)

            current_angle = ControlStick.from_edge_coordinate(round((self.min_angle + self.max_angle) / 2)).correct_for_cardinal_strict().to_edge_coordinate(True)
            if not self.should_sweet_spot and self.fade_back == FADE_BACK_MODE.NONE:
                if self.best_distance is None:
                    current_angle = self.max_angle
                else:
                    current_angle = ControlStick.from_edge_coordinate(round(self.hill_climb.get_next_point())).correct_for_cardinal_strict().to_edge_coordinate(True)

            # Testing cardinal directions
            else:
                if min_degrees % 90 == 0:
                    current_angle = self.min_angle
                elif max_degrees % 90 == 0:
                    current_angle = self.max_angle
            LogUtils.simple_log(self.min_angle, self.max_angle, current_angle, self.best_angle)

            # Test current angle in trial
            self.trajectory = FireFox.create_trajectory(self.start_x_velocity, ControlStick.coordinate_num_to_angle(current_angle))
            fade_back_frames = set()
            if not self.should_sweet_spot and self.fade_back == FADE_BACK_MODE.LATE:
                for i in range(self.current_frame, 600):
                    fade_back_frames.add(i)

            if not self.should_sweet_spot and self.fade_back == FADE_BACK_MODE.NONE:
                recovery_distance = self.trajectory.get_extra_distance(smashbot_state, opponent_state, self.target_coords, start_frame=self.current_frame)
                self.hill_climb.record_custom_result(recovery_distance, current_angle)
            else:
                recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.ledge, angle, magnitude, fade_back_frames=fade_back_frames, start_frame=self.current_frame)
            LogUtils.simple_log(abs(smashbot_state.position.x) - recovery_distance - self.target_coords[0])

            # Adjusting angle after trial
            if self.should_sweet_spot:
                if current_angle < 0 and abs(smashbot_state.position.x) - recovery_distance > self.target_coords[0] or \
                        current_angle >= 0 and recovery_distance == Trajectory.TOO_LOW_RESULT:
                    self.__adjust_min_angle(current_angle)
                else:
                    self.best_angle = current_angle
                    self.__adjust_max_angle(current_angle)
            elif self.fade_back != FADE_BACK_MODE.NONE:
                if recovery_distance != Trajectory.TOO_LOW_RESULT and \
                        abs(smashbot_state.position.x) - recovery_distance > self.target_coords[0]:
                    self.__adjust_max_angle(current_angle)
                else:
                    self.best_angle = current_angle
                    self.__adjust_min_angle(current_angle)
            else:
                if self.best_distance is not None and recovery_distance < self.best_distance:
                    self.__adjust_max_angle(current_angle)
                else:
                    self.best_distance = recovery_distance
                    self.best_angle = current_angle
                    self.__adjust_min_angle(current_angle)

            # Tilt stick in best angle on last frame
            if self.current_frame == 41:
                xy = ControlStick.from_edge_coordinate(self.best_angle).to_smashbot_xy()
                LogUtils.simple_log(xy)
                controller.tilt_analog(Button.BUTTON_MAIN, (1 - x) + (2 * x - 1) * xy[0], xy[1])

        elif self.current_frame >= 42:
            self.current_frame += 1
            frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]

            # Check if we should still fade-back
            recovery_distance = None

            # See if we can fade back on this frame
            if self.fade_back != FADE_BACK_MODE.NONE:
                fade_back_frames = set()
                # If we can make it by fading back this frame, do it
                if self.fade_back == FADE_BACK_MODE.EARLY:
                    fade_back_frames.add(self.current_frame)
                # If we can make it by holding a fade back starting this frame, do it
                elif self.fade_back == FADE_BACK_MODE.LATE:
                    for i in range(self.current_frame, 600):
                        fade_back_frames.add(i)

                recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.ledge, angle, magnitude, fade_back_frames, self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    should_fade_back = True

            if should_fade_back:
                x_input = 1 - x
                # If returning to neutral makes us fade-back faster, do it
                if frame.mid_horizontal_velocity is not None and \
                        frame.mid_horizontal_velocity < useful_x_velocity + frame.backward_acceleration:
                    x_input = 0.5

            else:
                x_input = x
                # If returning to neutral makes us fade-forward faster, do it
                if frame.mid_horizontal_velocity is not None and \
                        frame.mid_horizontal_velocity > useful_x_velocity + frame.forward_acceleration:
                    x_input = 0.5

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb_bottom[1], smashbot_state.ecb_left[0], smashbot_state.ecb_right[0],
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.ledge, self.fade_back, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)

        LogUtils.simple_log("frame number:", self.current_frame, smashbot_state.action_frame)
        self.interruptable = False
        return True

    def __adjust_min_angle(self, current_angle):
        # If cardinal direction does not work
        if ControlStick.coordinate_num_to_angle(self.min_angle) % 90 == 0:
            self.min_angle += 1
        else:
            self.min_angle = current_angle

    def __adjust_max_angle(self, current_angle):
        # If cardinal direction does not work
        if ControlStick.coordinate_num_to_angle(self.max_angle) % 90 == 0:
            self.max_angle -= 1
        else:
            self.max_angle = current_angle

    def __determine_initial_min_angle(self):
        if self.should_sweet_spot:
            return ControlStick(0, -ControlStick.MAX_INPUT).to_edge_coordinate(True)
        return ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(True)

    # TODO: consolidate sweet spot with other recovery targets
    # TODO: adjust chances to be more in line with realistic choice combinations
    # TODO: tune ledge tech SDI
    # TODO: extract constants out of commonly used numbers
    # TODO: do not always just fall to ledge
    # TODO: refactor firefox sweet-spot code into another path