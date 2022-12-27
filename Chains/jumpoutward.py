from melee.enums import Button

from Chains.chain import Chain


class JumpOutward(Chain):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

        # Should not jump outward if not past ledge
        if abs(smashbot_state.position.x) > game_state.get_stage_edge():
            return False

        return smashbot_state.jumps_left > 0

    def __init__(self):
        Chain.__init__(self)
        self.jumped = False

    def step_internal(self, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        controller = self.controller
        self.interruptable = True

        controller.tilt_analog_unit(Button.BUTTON_MAIN, smashbot_state.get_outward_x(), 0)
        if self.jumped and game_state.frame % 2 == 0:
            controller.release_button(Button.BUTTON_Y)
        else:
            controller.press_button(Button.BUTTON_Y)

        self.jumped = True
        return True