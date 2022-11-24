from abc import ABCMeta
from typing import Set

from melee import Action, Button, FrameData

from Chains.chain import Chain
from Utils import LogUtils, RecoveryTarget, Trajectory
from Utils.enums import FADE_BACK_MODE


class RecoveryChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0) -> Trajectory: ...

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), recovery_target=RecoveryTarget.max()):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.recovery_target = recovery_target
        self.current_frame = -1
        self.last_action_frame = -1
        self.trajectory = None

    def _applicable_states(self) -> Set[Action]: ...

    def _input_move(self, button, stick):
        self.interruptable = False
        self.controller.press_button(button)
        self.controller.tilt_analog(Button.BUTTON_MAIN, stick[0], stick[1])
        self.current_frame = 0

        LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "smashbot_state.ecb.left", "smashbot_state.ecb.right",
                            "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                            "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")

        return True

    def _increment_current_frame(self, smashbot_state):
        if smashbot_state.action_frame != self.last_action_frame:
            self.current_frame += 1
            self.last_action_frame = smashbot_state.action_frame

    def _perform_fade_back(self, game_state, smashbot_state, knockback, useful_x_velocity, inward_x):
        recovery_distance = None
        should_fade_back = False

        # See if we can fade back on this frame
        if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
            recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y), self.recovery_target.ledge, knockback, self._generate_fade_back_frames(), self.current_frame)
            if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                should_fade_back = True

        frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]
        x_input = self._input_fade_back(frame, should_fade_back, useful_x_velocity, inward_x)

        LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                            FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                            frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)

    def _generate_fade_back_frames(self):
        # If we do not want to fade back, then do not
        if self.recovery_target.fade_back_mode == FADE_BACK_MODE.NONE:
            return set()
        # If we can make it by fading back this frame, do it
        if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY:
            return {self.current_frame}
        # If we can make it by holding a fade back starting this frame, do it
        elif self.recovery_target.fade_back_mode == FADE_BACK_MODE.LATE:
            return {i for i in range(self.current_frame, 600)}

    def _input_fade_back(self, frame, should_fade_back, useful_x_velocity, inward_x):
        if should_fade_back:
            x_input = 1 - inward_x
            # If returning to neutral makes us fade-back faster, do it
            if frame.mid_horizontal_velocity is not None and \
                    frame.mid_horizontal_velocity < useful_x_velocity + frame.backward_acceleration:
                x_input = 0.5

        else:
            x_input = inward_x
            # If returning to neutral makes us fade-forward faster, do it
            if frame.mid_horizontal_velocity is not None and \
                    frame.mid_horizontal_velocity > useful_x_velocity + frame.forward_acceleration:
                x_input = 0.5

        self.controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        return x_input
