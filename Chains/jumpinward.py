from melee.enums import Button

from Chains.chain import Chain


class JumpInward(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.jumps_left > 0

    def __init__(self):
        Chain.__init__(self)
        self.jumped = False

    def step_internal(self, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        controller = self.controller
        self.interruptable = True

        controller.tilt_analog_unit(Button.BUTTON_MAIN, smashbot_state.get_inward_x(), 0)
        if self.jumped and game_state.frame % 2 == 0:
            controller.release_button(Button.BUTTON_Y)
        else:
            controller.press_button(Button.BUTTON_Y)

        self.jumped = True
        return True