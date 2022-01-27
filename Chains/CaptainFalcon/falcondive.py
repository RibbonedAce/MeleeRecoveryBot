import math

from melee.enums import Action, Button, Character

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils.angleutils import AngleUtils
from Utils.enums import FADE_BACK_MODE
from Utils.mathutils import MathUtils
from Utils.trajectory import Trajectory


class FalconDive(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 44, -999, 999, "Data/falcon_dive.csv")
    REVERSE_TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 44, 15, 999, "Data/reverse_falcon_dive.csv")

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    @staticmethod
    def get_trajectory(reverse=False):
        trajectory = FalconDive.TRAJECTORY
        if reverse:
            trajectory = FalconDive.REVERSE_TRAJECTORY
        return trajectory

    def __init__(self, target_coords=(0, 0), fade_back=FADE_BACK_MODE.NONE, ledge=False):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.fade_back = fade_back
        self.ledge = ledge
        self.current_frame = -1
        self.trajectory = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.trajectory is None:
            self.trajectory = self.__decide_trajectory(smashbot_state, opponent_state)

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL]:
            self.interruptable = True
            controller.empty_input()
            return True

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in [Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL]:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            # print("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "smashbot_state.ecb_bottom[1]", "smashbot_state.ecb_left[0]", "smashbot_state.ecb_right[0]",
            #       "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
            #       "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward", sep=", ")
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

            # Check if we should still fade-back
            should_fade_back = False
            useful_x_velocity = smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x)
            angle = smashbot_state.get_knockback_angle(opponent_state)
            if math.cos(math.radians(angle)) > 0:
                angle = AngleUtils.get_x_reflection(angle)
            magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

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
                # Do not fully fade-back if it would make us turn around unintentionally
                if self.trajectory == FalconDive.TRAJECTORY and \
                        smashbot_state.action == Action.FIREFOX_WAIT_AIR and smashbot_state.action_frame == 12:
                    x_input = 0.4 + 0.2 * x

            else:
                x_input = x
                # If returning to neutral makes us fade-forward faster, do it
                if frame.mid_horizontal_velocity is not None and \
                        frame.mid_horizontal_velocity > useful_x_velocity + frame.forward_acceleration:
                    x_input = 0.5
                # Do not fully fade-forward if it would make us turn around unintentionally
                if self.trajectory == FalconDive.REVERSE_TRAJECTORY and \
                        smashbot_state.action == Action.FIREFOX_WAIT_AIR and smashbot_state.action_frame == 12:
                    x_input = 0.6 - 0.2 * x

            # print(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb_bottom[1], smashbot_state.ecb_left[0], smashbot_state.ecb_right[0],
            #       FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.ledge, self.fade_back, x_input, should_fade_back, recovery_distance,
            #       frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward, sep=", ")
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True

    def __decide_trajectory(self, smashbot_state, opponent_state):
        # Pick reverse trajectory if we can make it and if we want to
        if DifficultySettings.should_reverse() and \
                FalconDive.REVERSE_TRAJECTORY.get_extra_distance(smashbot_state, opponent_state, self.target_coords, self.ledge, 0) > 0:
            return FalconDive.REVERSE_TRAJECTORY
        return FalconDive.TRAJECTORY