from melee.enums import Button

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import LogUtils
from Utils.enums import TDI_MODE


class TDI(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        # If we do not want to TDI, then do not
        if DifficultySettings.TDI == TDI_MODE.NONE:
            return False

        return smashbot_state.hitlag_left == 2 or smashbot_state.is_being_thrown()

    def step_internal(self, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]
        controller = self.controller
        self.interruptable = True

        # There's three kinds of TDI:
        #   1) Survival TDI
        #   2) Combo TDI
        #   3) Situationally-specific TDI

        stage_edge = game_state.get_stage_edge()
        angle = smashbot_state.get_knockback(opponent_state).to_angle()
        actual_jumps_left = smashbot_state.jumps_left
        if smashbot_state.is_being_thrown():
            actual_jumps_left = 1

        combo_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, angle.to_combo_di_launch())
        no_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, angle)
        danger_threshold = DifficultySettings.DANGER_THRESHOLD * (actual_jumps_left + 1)

        # Survival TDI
        #   If we're at risk of dying from the hit, then TDI 90 degrees from the direction of the hit
        if angle.get_y() < 0 or no_di_danger > danger_threshold:
            s_input = angle.to_survival_di(smashbot_state.position.x)
            controller.tilt_analog_unit(Button.BUTTON_MAIN, s_input.get_x(), s_input.get_y())
            LogUtils.simple_log("Survival TDI")
            return True

        # No TDI
        #   If Combo DI is too dangerous, but no DI isn't
        if combo_di_danger > danger_threshold:
            controller.tilt_analog_unit(Button.BUTTON_MAIN, 0, 0)
            LogUtils.simple_log("No TDI")
            return True

        # Combo TDI
        #   TDI away from the opponent to keep from following up
        angle = angle.to_combo_di()
        controller.tilt_analog_unit(Button.BUTTON_MAIN, angle.get_x(), angle.get_y())
        # Slide off if on ground
        if smashbot_state.on_ground:
            controller.tilt_analog_unit(Button.BUTTON_C, 0, -1)
        LogUtils.simple_log("Combo TDI angle:", angle)
        return True