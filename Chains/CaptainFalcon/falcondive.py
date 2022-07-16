import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from difficultysettings import DifficultySettings
from Utils import AngleUtils, LogUtils, Trajectory
from Utils.enums import FADE_BACK_MODE


class FalconDive(RecoveryChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 44, -999, 999, "Data/falcon_dive.csv")
    REVERSE_TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 44, 15, 999, "Data/reverse_falcon_dive.csv")

    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0):
        return cls.TRAJECTORY

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.trajectory is None:
            self.trajectory = self.__decide_trajectory(game_state, smashbot_state, opponent_state)

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL]:
            return False

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in [Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL]:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "smashbot_state.ecb.left", "smashbot_state.ecb.right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

            # Check if we should still fade-back
            should_fade_back = False
            useful_x_velocity = smashbot_state.get_inward_x_velocity()
            angle = smashbot_state.get_knockback_angle(opponent_state)
            if math.cos(math.radians(angle)) > 0:
                angle = AngleUtils.get_x_reflection(angle)
            magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

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
                if self.trajectory == self.REVERSE_TRAJECTORY and \
                        smashbot_state.action == Action.FIREFOX_WAIT_AIR and smashbot_state.action_frame == 12:
                    x_input = 0.6 - 0.2 * x

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True

    def __decide_trajectory(self, game_state, smashbot_state, opponent_state):
        # Pick reverse trajectory if we can make it and if we want to
        if DifficultySettings.should_reverse() and \
                self.REVERSE_TRAJECTORY.get_extra_distance(game_state, smashbot_state, opponent_state, self.target_coords, self.recovery_target.ledge, 0) > 0:
            return self.REVERSE_TRAJECTORY
        return self.TRAJECTORY