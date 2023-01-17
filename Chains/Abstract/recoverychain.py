from abc import ABCMeta
from collections import defaultdict
from typing import Set

from melee import Action, Button, FrameData

from Chains.chain import Chain
from Utils import FrameInput, LogUtils, RecoveryTarget, Trajectory, Vector2
from Utils.enums import FADE_BACK_MODE


class RecoveryChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, character) -> Trajectory: ...

    @classmethod
    def create_default_inputs(cls, smashbot_state, game_state):
        return defaultdict(lambda: FrameInput.forward())

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target=Vector2.zero(), recovery_target=RecoveryTarget.max()):
        Chain.__init__(self)
        self.target = target
        self.recovery_target = recovery_target
        self.current_frame = -1
        self.last_action_frame = -1
        self.trajectory = None

    def _applicable_states(self) -> Set[Action]: ...

    def _input_move(self, button, stick):
        self.interruptable = False
        self.controller.press_button(button)
        self.controller.tilt_analog_unit(Button.BUTTON_MAIN, stick.x, stick.y)
        self.current_frame = 0

        LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "ecb.left", "ecb.right",
                            "ledge_box_horizontal", "ledge_box_top", "ledge", "fade_back", "input", "should_fade_back_this_frame", "recovery_distance",
                            "frame.velocity.neutral", "frame.velocity.up", "frame.velocity.down", "frame.velocity.back", "frame.velocity.forward", "frame.ecb")

        return True

    def _increment_current_frame(self, smashbot_state):
        if smashbot_state.action_frame != self.last_action_frame:
            self.current_frame += 1
            self.last_action_frame = smashbot_state.action_frame

    def _generate_input_frames(self):
        default = defaultdict(lambda: FrameInput.forward())
        # If we do not want to fade back, then do not
        if self.recovery_target.fade_back_mode == FADE_BACK_MODE.NONE:
            return default
        # If we can make it by fading back this frame, do it
        if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY:
            default[self.current_frame] = FrameInput.backward()
            return default
        # If we can make it by holding a fade back starting this frame, do it
        elif self.recovery_target.fade_back_mode == FADE_BACK_MODE.LATE:
            return defaultdict(lambda: FrameInput.backward())

    def _perform_fade_back(self, propagate):
        smashbot_state = propagate[1]
        recovery_distance = None
        should_fade_back = False

        # See if we can fade back on this frame
        if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
            recovery_distance = self.trajectory.get_distance(propagate, target=self.target, ledge=self.recovery_target.ledge, frame_range=range(self.current_frame, 600), input_frames=self._generate_input_frames())
            if abs(smashbot_state.position.x) - recovery_distance <= self.target.x:
                should_fade_back = True

        frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]
        x_input = self._input_fade_back(smashbot_state, frame, should_fade_back)

        LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                            FrameData.INSTANCE.get_ledge_box(smashbot_state.character).horizontal, FrameData.INSTANCE.get_ledge_box(smashbot_state.character).top, self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                            frame.velocity(smashbot_state.get_relative_velocity(), Vector2.zero()), frame.velocity(smashbot_state.get_relative_velocity(), Vector2(0, 1)), frame.velocity(smashbot_state.get_relative_velocity(), Vector2(0, -1)), frame.velocity(smashbot_state.get_relative_velocity(), Vector2(-1, 0)), frame.velocity(smashbot_state.get_relative_velocity(), Vector2(1, 0)), frame.ecb)

    def _input_fade_back(self, smashbot_state, frame, should_fade_back):
        velocity = smashbot_state.get_relative_velocity()
        inward_x = smashbot_state.get_inward_x()
        sort_key = lambda k: frame.velocity(velocity, Vector2(k, 0)).x

        if should_fade_back:
            s_input = min(-1, 0, key=sort_key) * inward_x
        else:
            s_input = max(1, 0, key=sort_key) * inward_x

        self.controller.tilt_analog_unit(Button.BUTTON_MAIN, s_input, 0)
        return s_input
