import math

from melee import Action, Button, Character, FrameData

from Chains.CaptainFalcon.falcondive import FalconDive
from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import AngleUtils, Trajectory
from Utils.enums import STALL_MODE


class FalconKick(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 0, 12, -999, 999, "Data/falcon_kick.csv", include_fall_frames=False)

    @classmethod
    def should_use(cls, propagate):
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

        diff_x = abs(smashbot_state.position.x) - game_state.get_stage_edge()
        angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(angle)) > 0:
            angle = AngleUtils.get_x_reflection(angle)
        displacement = cls.TRAJECTORY.get_displacement_after_frames(smashbot_state.get_inward_x_velocity(), len(cls.TRAJECTORY.frames), angle, smashbot_state.get_knockback_magnitude(opponent_state))

        # Should not Falcon Kick if too close unless we want to
        if diff_x <= 40 + displacement[0] and falcon_kick_mode == STALL_MODE.SMART:
            return False

        # Falcon Kick if we are high enough
        return smashbot_state.position.y > -displacement[1] - \
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
