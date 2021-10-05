from melee import Button

from Chains.chain import Chain


class DriftIn(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return not smashbot_state.on_ground and not smashbot_state.is_wall_teching()

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_MAIN, smashbot_state.get_inward_x(), 0.5)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
        return True
