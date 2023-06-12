from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import StallChain
from Chains.Marth.dolphinslash import DolphinSlash
from Utils import Trajectory


class DancingBlade(StallChain):
    TRAJECTORY = Trajectory(Character.MARTH, "DancingBlade.Strong")
    WEAK_TRAJECTORY = Trajectory(Character.MARTH, "DancingBlade.Weak")

    @classmethod
    def create_trajectory(cls, stall_charge):
        if stall_charge:
            return cls.TRAJECTORY
        return cls.WEAK_TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return DolphinSlash.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls, charge):
        if charge:
            return cls.TRAJECTORY.height_displacement
        return cls.WEAK_TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return cls.TRAJECTORY.length

    @classmethod
    def min_stall_speed(cls, character):
        return FrameData.INSTANCE.get_air_speed(character) - FrameData.INSTANCE.get_air_mobility(character)

    def step_internal(self, propagate):
        smashbot_state = propagate[1]
        controller = self.controller

        inward_x = smashbot_state.get_inward_x()

        # If we are not finished with the stall
        if not self.used_move:
            # If double jumping, wait until you reach max height
            if smashbot_state.speed_y_self >= 0 and smashbot_state.action == Action.JUMPING_ARIAL_FORWARD:
                self.interruptable = True
                controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x, 0)
                return True

            # Do the stall if the max height has been achieved
            if smashbot_state.speed_y_self < 0:
                self.interruptable = False
                controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x, 0)
                controller.press_button(Button.BUTTON_B)
                self.used_move = True
                return True

        # If in the middle of stall, we are not interruptable
        if smashbot_state.action == Action.SWORD_DANCE_1_AIR:
            self.interruptable = False
            controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x, 0)
            return True

        return False