import math

from melee import Button, GameState

from Chains.chain import Chain


class LedgeTech(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

        # Cannot ledge tech if in tech lockout or not in hit-stun
        if GameState.TECH_LOCKOUT[smashbot_state.get_port(game_state)] > smashbot_state.hitlag_left - 2:
            return False

        # Cannot ledge tech if you don't go into knockdown
        if smashbot_state.hitstun_frames_left < 32:
            return False

        return min(abs(smashbot_state.position.x + smashbot_state.ecb_left[0]), abs(smashbot_state.position.x + smashbot_state.ecb_right[0])) <= game_state.get_stage_edge() + 6 and \
               smashbot_state.position.y + smashbot_state.ecb_left[1] < math.sqrt(6)

    def __init__(self):
        Chain.__init__(self)
        self.waited = False
        self.teched = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        x = smashbot_state.get_inward_x()
        y = 0.5
        # Do a diagonal-downward SDI input if slightly above ledge
        if smashbot_state.position.y + smashbot_state.ecb_left[1] > 0:
            y = 0

        # Wait one frame to reset the stick to set up SDI
        if not self.waited:
            self.interruptable = False
            controller.empty_input()
            self.waited = True
            return True

        # Input the jump tech if we can
        if not self.teched and smashbot_state.hitlag_left > 1 and smashbot_state.can_tech(game_state):
            self.interruptable = False

            controller.tilt_analog(Button.BUTTON_MAIN, x, y)
            controller.press_button(Button.BUTTON_L)
            controller.press_button(Button.BUTTON_Y)
            self.teched = True
            return True

        # Keep holding until we become actionable
        if smashbot_state.is_wall_teching() and smashbot_state.action_frame == 0:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, y)
            controller.press_button(Button.BUTTON_L)
            controller.press_button(Button.BUTTON_Y)
            return True

        # Act normally out of wall jump
        if smashbot_state.is_wall_teching() and smashbot_state.action_frame > 0:
            return False

        return False
