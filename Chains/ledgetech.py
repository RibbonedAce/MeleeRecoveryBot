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

        return abs(smashbot_state.x) <= game_state.get_stage_edge() + 12 and smashbot_state.y < -10

    def __init__(self):
        Chain.__init__(self)
        self.waited = False
        self.teched = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        x = smashbot_state.get_inward_x()

        # Wait one frame to reset the stick to set up SDI
        if not self.waited:
            self.interruptable = False
            controller.empty_input()
            self.waited = True
            return True

        # Input the jump tech if we can
        if not self.teched and smashbot_state.hitlag_left > 1 and smashbot_state.can_tech(game_state):
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            controller.press_button(Button.BUTTON_L)
            controller.press_button(Button.BUTTON_Y)
            self.teched = True
            return True

        # Keep holding until we become actionable
        if smashbot_state.is_wall_teching() and smashbot_state.action_frame == 0:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            controller.press_button(Button.BUTTON_L)
            controller.press_button(Button.BUTTON_Y)
            return True

        # Act normally out of wall jump
        if smashbot_state.is_wall_teching() and smashbot_state.action_frame > 0:
            self.interruptable = True
            controller.empty_input()
            return True

        return False
