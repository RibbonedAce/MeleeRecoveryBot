from melee.enums import Button

from Chains.chain import Chain


class JumpInward(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.jumps_left > 0

    def __init__(self):
        Chain.__init__(self)
        self.jumped = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True

        controller.tilt_analog(Button.BUTTON_MAIN, smashbot_state.get_inward_x(), 0.5)
        if self.jumped and game_state.frame % 2 == 0:
            controller.release_button(Button.BUTTON_Y)
        else:
            controller.press_button(Button.BUTTON_Y)

        self.jumped = True
        return True