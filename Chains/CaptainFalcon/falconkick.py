from melee import Action, Button, FrameData

from Chains.CaptainFalcon.falcondive import FalconDive
from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils.enums import STALL_MODE


class FalconKick(Chain):
    DISPLACEMENT = (49, -132)

    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        falcon_kick_mode = DifficultySettings.STALL
        # If we do not want to Falcon Kick, do not
        if falcon_kick_mode == STALL_MODE.NEVER:
            return False

        # Cannot Falcon Kick if still in hit-stun
        if smashbot_state.hitstun_frames_left > 0:
            return False

        # Should not Falcon Kick if facing backwards
        if smashbot_state.facing != (smashbot_state.position.x < 0):
            return False

        knockback = smashbot_state.get_remaining_knockback(opponent_state)
        diff_x = abs(smashbot_state.position.x) - game_state.get_stage_edge() + abs(knockback[0])
        # Should not Falcon Kick if too close unless we want to
        if diff_x <= 40 + FalconKick.DISPLACEMENT[0] and falcon_kick_mode == STALL_MODE.SMART:
            return False

        # Falcon Kick if we are high enough
        return smashbot_state.position.y > \
               -FalconKick.DISPLACEMENT[1] - knockback[1] - \
               FrameData.INSTANCE.dj_height(smashbot_state) * (1 + smashbot_state.jumps_left) - \
               FalconDive.TRAJECTORY.get_max_height() - FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)

    def __init__(self):
        Chain.__init__(self)
        self.falcon_kicked = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        x = smashbot_state.get_inward_x()

        # If we are not finished with the Falcon Kick
        if not self.falcon_kicked:

            # Do the double jump if not already doing so
            if not smashbot_state.on_ground and smashbot_state.jumps_left > 0:
                self.interruptable = True
                controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
                controller.press_button(Button.BUTTON_Y)
                return True

            # If double jumping, wait until you reach max height
            if smashbot_state.speed_y_self >= 0 and smashbot_state.action == Action.JUMPING_ARIAL_FORWARD:
                self.interruptable = True
                controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
                return True

            # Do the Falcon Kick if the max height has been achieved
            if smashbot_state.speed_y_self < 0:
                self.interruptable = False
                controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0)
                controller.press_button(Button.BUTTON_B)
                self.falcon_kicked = True
                return True

        # If in the middle of Falcon Kick, we are not interruptable
        if smashbot_state.action == Action.SWORD_DANCE_2_HIGH_AIR or smashbot_state.action == Action.SWORD_DANCE_3_MID_AIR:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            return True

        return False
