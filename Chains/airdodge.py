from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import Trajectory, Vector2


class AirDodge(RecoveryChain):
    TRAJECTORY_DICTIONARY = {
        Character.CPTFALCON: Trajectory(Character.CPTFALCON, "AirDodge.CaptainFalcon"),
        Character.FOX: Trajectory(Character.FOX, "AirDodge.Fox"),
        Character.FALCO: Trajectory(Character.FALCO, "AirDodge.Falco"),
        Character.GANONDORF: Trajectory(Character.GANONDORF, "AirDodge.Ganondorf"),
        Character.MARTH: Trajectory(Character.MARTH, "AirDodge.Marth")}

    @classmethod
    def create_trajectory(cls, character):
        return AirDodge.TRAJECTORY_DICTIONARY[character]

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_L, Vector2(0, 1))

        self._increment_current_frame(smashbot_state)

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_L)
                self.trajectory = self.create_trajectory(smashbot_state.character)

            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.AIRDODGE, Action.DEAD_FALL}