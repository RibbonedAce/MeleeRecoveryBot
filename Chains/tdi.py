from melee.enums import Button

from Chains.chain import Chain
from Utils.angleutils import AngleUtils
from Utils.difficultysettings import DifficultySettings
from Utils.enums import TDI_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils


class TDI(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        # If we do not want to TDI, then do not
        if DifficultySettings.TDI == TDI_MODE.NONE:
            return False

        return smashbot_state.hitlag_left == 2 or PlayerStateUtils.is_being_thrown(smashbot_state)

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True

        # There's three kinds of TDI:
        #   1) Survival TDI
        #   2) Combo TDI
        #   3) Situationally-specific TDI

        stage_edge = GameStateUtils.get_stage_edge(game_state)
        knockback_angle = PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)
        actual_jumps_left = smashbot_state.jumps_left
        if PlayerStateUtils.is_being_thrown(smashbot_state):
            actual_jumps_left = 1

        combo_di_danger = PlayerStateUtils.get_knockback_danger(smashbot_state, opponent_state, stage_edge, FrameDataUtils.get_combo_di_launch_angle(knockback_angle))
        no_di_danger = PlayerStateUtils.get_knockback_danger(smashbot_state, opponent_state, stage_edge, knockback_angle)
        danger_threshold = DifficultySettings.DANGER_THRESHOLD * (actual_jumps_left + 1)

        # Survival TDI
        #   If we're at risk of dying from the hit, then TDI 90 degrees from the direction of the hit
        if knockback_angle > 180 or no_di_danger > danger_threshold:
            angle = FrameDataUtils.get_survival_di(knockback_angle, smashbot_state.position.x)
            inputs = AngleUtils.angle_to_xy(angle)
            controller.tilt_analog(Button.BUTTON_MAIN, inputs[0], inputs[1])
            return True

        # No TDI
        #   If Combo DI is too dangerous, but no DI isn't
        if combo_di_danger > danger_threshold:
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0.5)
            return True

        # Combo TDI
        #   TDI away from the opponent to keep from from following up
        angle = FrameDataUtils.get_combo_di(knockback_angle)
        inputs = AngleUtils.angle_to_xy(angle)
        if self.logger:
            self.logger.log("Notes", " Combo TDI angle: " + str(angle) + " ", concat=True)
        controller.tilt_analog(Button.BUTTON_MAIN, inputs[0], inputs[1])
        # Slide off if on ground
        if smashbot_state.on_ground:
            controller.tilt_analog(Button.BUTTON_C, 0.5, 0)
        return True