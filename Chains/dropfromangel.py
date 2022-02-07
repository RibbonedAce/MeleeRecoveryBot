from melee.enums import Button

from Chains.chain import Chain


class DropFromAngel(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        return smashbot_state.get_stock_duration(game_state) <= 120 and smashbot_state.invulnerability_left > 0 and smashbot_state.position.y > 1

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0)
        return True
