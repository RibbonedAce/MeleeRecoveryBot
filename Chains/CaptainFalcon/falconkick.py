from melee import Button, Action

from Chains import Chain
from Chains.CaptainFalcon import FalconDive
from Utils.difficultysettings import DifficultySettings
from Utils.enums import FALCON_KICK_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.utils import Utils


class FalconKick(Chain):
    DISPLACEMENT = (49, -132)

    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        falcon_kick_mode = DifficultySettings.FALCON_KICK
        # If we do not want to Falcon Kick, do not
        if falcon_kick_mode == FALCON_KICK_MODE.NEVER:
            return False

        # Cannot Falcon Kick if still in hit-stun
        if smashbot_state.hitstun_frames_left > 0:
            return False

        # Should not Falcon Kick if facing backwards
        if smashbot_state.facing != (smashbot_state.position.x < 0):
            return False

        knockback = PlayerStateUtils.get_remaining_knockback(smashbot_state, opponent_state)
        diff_x = abs(smashbot_state.position.x) - GameStateUtils.get_stage_edge(game_state) + abs(knockback[0])
        # Should not Falcon Kick if too close unless we want to
        if diff_x <= 20 + FalconKick.DISPLACEMENT[0] and falcon_kick_mode == FALCON_KICK_MODE.SMART:
            return False

        # Falcon Kick if we are high enough
        return smashbot_state.position.y > \
               -FalconKick.DISPLACEMENT[1] - knockback[1] - \
               FrameDataUtils.INSTANCE.dj_height(smashbot_state) * (1 + smashbot_state.jumps_left) - \
               FalconDive.TRAJECTORY.max_height - Utils.LEDGE_GRAB_AREA[1]

    def __init__(self):
        self.falcon_kicked = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        x = PlayerStateUtils.get_inward_x(smashbot_state)

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
