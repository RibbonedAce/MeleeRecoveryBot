from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import Vector2


class SideSlide(RecoveryChain, metaclass=ABCMeta):
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

            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FOX_ILLUSION, Action.DEAD_FALL}