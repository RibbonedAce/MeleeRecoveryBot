from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import Trajectory, Vector2
from Utils.enums import FADE_BACK_MODE


class SpacieApparition(RecoveryChain, metaclass=ABCMeta):
    @classmethod
    def create_shorten_trajectory(cls, amount) -> Trajectory: ...

    @classmethod
    def _get_shorten_frame(cls) -> int: ...

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, Vector2(smashbot_state.get_inward_x(), 0))

        self._increment_current_frame(smashbot_state)

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)
                self.trajectory = self.create_trajectory(smashbot_state.character)

            # Decide if we should shorten
            shorten_frame = self._get_shorten_frame()
            if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY and shorten_frame <= self.current_frame <= shorten_frame + 3:
                self.trajectory = self.create_shorten_trajectory(shorten_frame + 4 - self.current_frame)
                recovery_distance = self.trajectory.get_distance(propagate, target=self.target, ledge=self.recovery_target.ledge, frame_range=range(self.current_frame, 600))
                if abs(smashbot_state.position.x) - recovery_distance <= self.target.x:
                    self.controller.press_button(Button.BUTTON_B)

            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FOX_ILLUSION, Action.FOX_ILLUSION_START, Action.FOX_ILLUSION_SHORTENED, Action.DEAD_FALL}