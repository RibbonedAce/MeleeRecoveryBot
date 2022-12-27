from melee.enums import Action, Button

from Chains.chain import Chain


class Wiggle(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action == Action.TUMBLING or \
               smashbot_state.is_flying_in_hit_stun() and smashbot_state.hitstun_frames_left == 0

    def step_internal(self, propagate):
        game_state = propagate[0]
        controller = self.controller
        self.interruptable = True

        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog_unit(Button.BUTTON_MAIN, 2 * (game_state.frame % 2) - 1, 0)
        controller.tilt_analog_unit(Button.BUTTON_C, 0, 0)
        return True
