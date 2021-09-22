from melee.enums import Button, Action

from Chains.chain import Chain
from Utils.playerstateutils import PlayerStateUtils


class Wiggle(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action == Action.TUMBLING or \
               PlayerStateUtils.is_flying_in_hit_stun(smashbot_state) and smashbot_state.hitstun_frames_left == 0

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_MAIN, game_state.frame % 2, 0.5)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
        return True
