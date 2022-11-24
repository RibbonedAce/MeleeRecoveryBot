from melee.enums import Button

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import AngleUtils, LogUtils
from Utils.enums import TDI_MODE


class TDI(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        # If we do not want to TDI, then do not
        if DifficultySettings.TDI == TDI_MODE.NONE:
            return False

        return smashbot_state.hitlag_left == 2 or smashbot_state.is_being_thrown()

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True

        # There's three kinds of TDI:
        #   1) Survival TDI
        #   2) Combo TDI
        #   3) Situationally-specific TDI

        stage_edge = game_state.get_stage_edge()
        angle = smashbot_state.get_knockback(opponent_state).angle
        actual_jumps_left = smashbot_state.jumps_left
        if smashbot_state.is_being_thrown():
            actual_jumps_left = 1

        combo_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, AngleUtils.get_combo_di_launch_angle(angle))
        no_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, angle)
        danger_threshold = DifficultySettings.DANGER_THRESHOLD * (actual_jumps_left + 1)

        # Survival TDI
        #   If we're at risk of dying from the hit, then TDI 90 degrees from the direction of the hit
        if angle > 180 or no_di_danger > danger_threshold:
            angle = AngleUtils.get_survival_di(angle, smashbot_state.position.x)
            inputs = AngleUtils.angle_to_xy(angle)
            controller.tilt_analog(Button.BUTTON_MAIN, inputs[0], inputs[1])
            LogUtils.simple_log("Survival TDI")
            return True

        # No TDI
        #   If Combo DI is too dangerous, but no DI isn't
        if combo_di_danger > danger_threshold:
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0.5)
            LogUtils.simple_log("No TDI")
            return True

        # Combo TDI
        #   TDI away from the opponent to keep from from following up
        angle = AngleUtils.get_combo_di(angle)
        inputs = AngleUtils.angle_to_xy(angle)
        controller.tilt_analog(Button.BUTTON_MAIN, inputs[0], inputs[1])
        # Slide off if on ground
        if smashbot_state.on_ground:
            controller.tilt_analog(Button.BUTTON_C, 0.5, 0)
        LogUtils.simple_log("Combo TDI angle:", angle)
        return True