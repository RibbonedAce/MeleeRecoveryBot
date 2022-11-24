from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from difficultysettings import DifficultySettings
from Utils import Trajectory


class ElementalDive(RecoveryChain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        return cls._get_normal_trajectory()

    @classmethod
    def _get_normal_trajectory(cls) -> Trajectory: ...

    @classmethod
    def _get_reverse_trajectory(cls) -> Trajectory: ...

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

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                # Pick reverse trajectory if we can make it and if we want to
                if DifficultySettings.should_reverse() and self._get_reverse_trajectory().get_extra_distance(game_state, smashbot_state, opponent_state, self.target_coords, self.recovery_target.ledge, 0) > 0:
                    self.trajectory = self._get_reverse_trajectory()
                else:
                    self.trajectory = self._get_normal_trajectory()

            self._perform_fade_back(game_state, smashbot_state, knockback, inward_x_velocity, inward_x)

        self.interruptable = False
        return True

    def _input_fade_back(self, frame, should_fade_back, useful_x_velocity, x):
        if should_fade_back:
            x_input = 1 - x
            # If returning to neutral makes us fade-back faster, do it
            if frame.mid_horizontal_velocity is not None and \
                    frame.mid_horizontal_velocity < useful_x_velocity + frame.backward_acceleration:
                x_input = 0.5
            # Do not fully fade-back if it would make us turn around unintentionally
            if self.trajectory == self._get_normal_trajectory() and self.current_frame == 12:
                x_input = 0.4 + 0.2 * x

        else:
            x_input = x
            # If returning to neutral makes us fade-forward faster, do it
            if frame.mid_horizontal_velocity is not None and \
                    frame.mid_horizontal_velocity > useful_x_velocity + frame.forward_acceleration:
                x_input = 0.5
            # Do not fully fade-forward if it would make us turn around unintentionally
            if self.trajectory == self._get_reverse_trajectory() and self.current_frame == 12:
                x_input = 0.6 - 0.2 * x

        self.controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        return x_input

    def _applicable_states(self):
        return {Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL}