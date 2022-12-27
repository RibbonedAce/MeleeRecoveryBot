from melee.enums import Button

from Chains.chain import Chain
from Utils import Angle


# Struggle out of a grab
class Struggle(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.is_grabbed()

    def step_internal(self, propagate):
        # Just naively press and release every button every other frame
        game_state = propagate[0]
        controller = self.controller
        self.interruptable = True

        # Press every button
        if game_state.frame % 2:
            controller.press_button(Button.BUTTON_A)
            controller.press_button(Button.BUTTON_B)
            controller.press_button(Button.BUTTON_X)
            controller.press_button(Button.BUTTON_Y)
            controller.press_button(Button.BUTTON_Z)
        # Release every button
        else:
            controller.release_button(Button.BUTTON_A)
            controller.release_button(Button.BUTTON_B)
            controller.release_button(Button.BUTTON_X)
            controller.release_button(Button.BUTTON_Y)
            controller.release_button(Button.BUTTON_L)
            controller.release_button(Button.BUTTON_R)
            controller.release_button(Button.BUTTON_Z)

        angle = Angle((game_state.frame % 4) / 4, Angle.Mode.ROTATIONS)
        controller.tilt_analog_unit(Button.BUTTON_MAIN, angle.get_x(), angle.get_y())
        controller.tilt_analog_unit(Button.BUTTON_C, angle.get_x(), angle.get_y())

        return True
