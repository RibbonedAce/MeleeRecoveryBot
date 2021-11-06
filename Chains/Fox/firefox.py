import copy
import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.chain import Chain
from Utils.angleutils import AngleUtils
from Utils.enums import FADE_BACK_MODE
from Utils.mathutils import MathUtils
from Utils.trajectory import Trajectory


class FireFox(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.FOX, 78, -999, 999, "Data/fire_fox.csv", requires_extra_height=True)

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

        trajectory.frames += Trajectory.create_trajectory_frames(Character.FOX, trajectory.frames[71].vertical_velocity)
        return trajectory

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), fade_back=FADE_BACK_MODE.NONE, ledge=False):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.fade_back = fade_back
        self.ledge = ledge
        self.current_frame = -1
        self.min_angle = 0
        self.max_angle = 90
        self.start_x_velocity = 0
        self.trajectory = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FIREFOX_AIR, Action.FIREFOX_WAIT_AIR, Action.SWORD_DANCE_1_AIR, Action.DEAD_FALL]:
            self.interruptable = True
            controller.empty_input()
            return True

        useful_x_velocity = smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x)
        if self.trajectory is None:
            self.trajectory = FireFox.create_trajectory(useful_x_velocity, self.min_angle)
            self.start_x_velocity = useful_x_velocity

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action != Action.FOX_ILLUSION:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            print("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "smashbot_state.ecb_bottom", "smashbot_state.ecb_left", "smashbot_state.ecb_right",
                  "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                  "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward", sep=", ")
            return True

        should_fade_back = False
        angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(angle)) > 0:
            angle = AngleUtils.get_x_reflection(angle)
        magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

        # Calculating and applying angle
        if 0 <= self.current_frame < 42:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

            current_angle = AngleUtils.correct_for_cardinal_strict((self.max_angle + self.min_angle) / 2)
            xy = AngleUtils.angle_to_xy(current_angle)

            controller.tilt_analog(Button.BUTTON_MAIN, (1 - x) + (2 * x - 1) * xy[0], xy[1])

            self.trajectory = FireFox.create_trajectory(self.start_x_velocity, current_angle)
            recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.ledge, angle, magnitude, start_frame=self.current_frame)
            if recovery_distance < 0:
                self.min_angle = current_angle
            elif abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                self.max_angle = current_angle

        elif self.current_frame >= 42:
            self.current_frame += 1

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

            frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]

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

            print(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb_bottom[1], smashbot_state.ecb_left[0], smashbot_state.ecb_right[0],
                  FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.ledge, self.fade_back, x_input, should_fade_back, recovery_distance,
                  frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward, sep=", ")
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True

print(FireFox.create_trajectory(0, 45).get_distance(0, 80, True))