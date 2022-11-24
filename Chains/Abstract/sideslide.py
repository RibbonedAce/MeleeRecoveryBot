from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain


class SideSlide(RecoveryChain, metaclass=ABCMeta):
    def step_internal(self, game_state, smashbot_state, opponent_state):
        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        inward_x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, (inward_x, 0.5))

        self._increment_current_frame(smashbot_state)
        knockback = smashbot_state.get_relative_knockback(opponent_state)
        inward_x_velocity = smashbot_state.get_inward_x_velocity()

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                self.trajectory = self.create_trajectory(game_state, smashbot_state, inward_x_velocity)

            self._perform_fade_back(game_state, smashbot_state, knockback, inward_x_velocity, inward_x)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FOX_ILLUSION, Action.DEAD_FALL}