from abc import ABCMeta

from melee import Action, Button

from Chains.Abstract.stallchain import StallChain


class DescendingBoot(StallChain, metaclass=ABCMeta):
    @classmethod
    def _double_jumps_gained(cls):
        return 1

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        x = smashbot_state.get_inward_x()

        # If we are not finished with the stall
        if not self.used_move:

            # Do the double jump if not already doing so
            if not smashbot_state.on_ground and smashbot_state.jumps_left > 0:
                self.interruptable = True
                controller.tilt_analog(Button.BUTTON_MAIN, x, smashbot_state.get_inward_x())
                controller.press_button(Button.BUTTON_Y)
                return True

            # If double jumping, wait until you reach max height
            if smashbot_state.speed_y_self >= 0 and smashbot_state.action == Action.JUMPING_ARIAL_FORWARD:
                self.interruptable = True
                controller.tilt_analog(Button.BUTTON_MAIN, x, smashbot_state.get_inward_x())
                return True

            # Do the stall if the max height has been achieved
            if smashbot_state.speed_y_self < 0:
                self.interruptable = False
                controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0)
                controller.press_button(Button.BUTTON_B)
                self.used_move = True
                return True

        # If in the middle of stall, we are not interruptable
        if smashbot_state.action == Action.SWORD_DANCE_2_HIGH_AIR or smashbot_state.action == Action.SWORD_DANCE_3_MID_AIR:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, smashbot_state.get_inward_x())
            return True

        return False
