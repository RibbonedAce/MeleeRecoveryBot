from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from difficultysettings import DifficultySettings
from Utils import Trajectory, Vector2


class ElementalDive(RecoveryChain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, character):
        return cls._get_normal_trajectory()

    @classmethod
    def _get_normal_trajectory(cls) -> Trajectory: ...

    @classmethod
    def _get_reverse_trajectory(cls) -> Trajectory: ...

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, Vector2(0, 1))

        self._increment_current_frame(smashbot_state)

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                # Pick reverse trajectory if we can make it and if we want to
                if DifficultySettings.should_reverse() and self._get_reverse_trajectory().get_extra_distance(propagate, target=self.target, ledge=self.recovery_target.ledge) > 0:
                    self.trajectory = self._get_reverse_trajectory()
                else:
                    self.trajectory = self._get_normal_trajectory()

            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FIREFOX_WAIT_AIR, Action.FIREFOX_GROUND, Action.FIREFOX_AIR, Action.DEAD_FALL}