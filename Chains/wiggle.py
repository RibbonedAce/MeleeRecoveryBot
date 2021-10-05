from melee.enums import Action, Button

from Chains.chain import Chain


class Wiggle(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action == Action.TUMBLING or \
               smashbot_state.is_flying_in_hit_stun() and smashbot_state.hitstun_frames_left == 0

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_MAIN, game_state.frame % 2, 0.5)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
        return True
