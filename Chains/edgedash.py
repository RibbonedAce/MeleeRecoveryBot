from melee.enums import Action, Button

from Chains.chain import Chain
from Utils.logutils import LogUtils


class EdgeDash(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action in [Action.EDGE_HANGING, Action.EDGE_CATCHING]

    def __init__(self):
        Chain.__init__(self)
        self.has_stalled = False
        self.let_go_frame = 0

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        LogUtils.simple_log("Distance to edge:", smashbot_state.position.y + smashbot_state.ecb.bottom.y)

        # If we just grabbed the edge, just wait
        if smashbot_state.action == Action.EDGE_CATCHING:
            self.interruptable = False
            controller.empty_input()
            return True

        # If we are on the ground, we're done
        if smashbot_state.on_ground:
            return False

        # If we are able to let go of the edge, do it
        if smashbot_state.action == Action.EDGE_HANGING:
            # If we already pressed back last frame, let go
            if controller.prev.c_stick != (0.5, 0.5):
                controller.empty_input()
                return True
            self.interruptable = False
            self.let_go_frame = game_state.frame
            controller.tilt_analog(Button.BUTTON_C, smashbot_state.get_outward_x(), 0.5)
            return True

        x = smashbot_state.get_inward_x()

        # Once we're falling, jump
        if smashbot_state.action == Action.FALLING:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            controller.press_button(Button.BUTTON_Y)
            controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
            return True

        # Jumping, stay in the chain and DI in
        if smashbot_state.action == Action.JUMPING_ARIAL_FORWARD:
            # Wait until we are safely above stage
            if smashbot_state.position.y + smashbot_state.ecb.bottom.y > 0 and \
                    abs(smashbot_state.position.x) < game_state.get_stage_edge():
                self.interruptable = False
                controller.tilt_analog(Button.BUTTON_MAIN, x, 0.35)
                controller.press_button(Button.BUTTON_L)
                return True
            else:
                self.interruptable = False
                controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
                return True

        return False
