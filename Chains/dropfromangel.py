from melee.enums import Button

from Chains.chain import Chain


class DropFromAngel(Chain):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        return smashbot_state.get_stock_duration(game_state) <= 120 and smashbot_state.invulnerability_left > 0 and smashbot_state.position.y > 1

    def step_internal(self, propagate):
        controller = self.controller
        self.interruptable = True
        controller.tilt_analog_unit(Button.BUTTON_MAIN, 0, -1)
        return True
