from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import StallChain
from Chains.Marth.dolphinslash import DolphinSlash
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class DancingBlade(StallChain):
    TRAJECTORY = Trajectory(Character.MARTH, 0, 1, LEDGE_GRAB_MODE.AFTER, False, [
        TF(lambda v, i: V2(TF.reduce_singular(0.8 * v.x, 0.0025), 0.94), V2(2.11648, 4.64884)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.51202, 5.78777)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2, 6.15807)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.19584, 5.8885)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(3.22828, 6.2429)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(3.11102, 5.82793)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(3.12281, 5.16819)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.67862, 4.29417)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.42915, 2.67359)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.47077, 2.66928)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.50716, 2.85393)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.5386, 3.19158)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.56019, 3.67453)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.56691, 3.57507)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.55321, 3.42991)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.51177, 3.34016)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.44274, 3.2942)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.34217, 3.28966)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.21626, 3.31863)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.17749, 3.37696)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.15576, 3.46041)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.12843, 3.56277)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.10442, 3.67515)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.08996, 3.83192)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.11087, 4.03625)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2.01975, 4.32269)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2, 4.69275)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2, 4.34587)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.0025), TF.reduce_singular(v.y, 0.06, -1.5)), V2(2, 3.81794))
    ])

    WEAK_TRAJECTORY = Trajectory(Character.MARTH, 0, 1, LEDGE_GRAB_MODE.AFTER, False, [TF(lambda v, i: V2(TF.reduce_singular(0.8 * v.x, 0.0025), -0.06), V2(2.11648, 4.64884))] + TRAJECTORY.frames[1:])

    @classmethod
    def create_trajectory(cls, stall_charge):
        if stall_charge:
            return cls.TRAJECTORY
        return cls.WEAK_TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return DolphinSlash.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return len(cls.TRAJECTORY.frames)

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