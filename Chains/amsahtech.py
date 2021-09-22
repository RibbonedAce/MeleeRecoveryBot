import math
from math import sin, cos, radians

from melee import Button, Action

from Chains.chain import Chain
from Utils.angleutils import AngleUtils
from Utils.difficultysettings import DifficultySettings
from Utils.enums import AMSAH_TECH_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.utils import Utils


class AmsahTech(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        tech_mode = DifficultySettings.AMSAH_TECH
        # If we do not want to tech, do not
        if tech_mode == AMSAH_TECH_MODE.NEVER:
            return False

        stage_edge = GameStateUtils.get_stage_edge(game_state)
        # Cannot Amsah tech if can't stick on ground
        if not AmsahTech.can_stick_on_ground(smashbot_state, opponent_state, stage_edge):
            return False

        # Cannot Amsah tech if close to edge (need "- 6" since inputting TDI moves character)
        if abs(smashbot_state.position.x) > stage_edge - 6:
            return False

        can_slide_off = AmsahTech.should_slide_off(smashbot_state, opponent_state, stage_edge)
        # Cannot Amsah tech if in tech lockout unless you can also slide off
        if GameStateUtils.get_smashbot_custom(game_state, "tech_lockout") > smashbot_state.hitlag_left - 2 and not can_slide_off:
            return False

        # If we want to tech no matter what, do it
        if tech_mode == AMSAH_TECH_MODE.ALWAYS:
            return True

        angle = PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)
        x = cos(radians(angle))
        # Should not Amsah tech if close to opponent when tech is finished
        if x > 0 and smashbot_state.position.x > stage_edge - 30 or \
                x < 0 and smashbot_state.position.x < -(stage_edge - 30):
            # Unless we can slide off or Amsah tech is the only way to survive the hit
            if can_slide_off:
                return True
            survival_angle = FrameDataUtils.get_survival_di_launch_angle(angle, smashbot_state.position.x)
            return PlayerStateUtils.get_knockback_danger(smashbot_state, opponent_state, stage_edge, survival_angle) > DifficultySettings.DANGER_THRESHOLD * 2

        return True

    @staticmethod
    def can_stick_on_ground(smashbot_state, opponent_state, stage_edge):
        # Cannot stick on ground if already out of hit-lag (mainly from throws)
        if smashbot_state.hitlag_left != 2:
            return False

        # Cannot stick on ground if in the air
        if smashbot_state.position.y > 3:
            return False

        # Cannot stick on ground if you don't go into knockdown
        if smashbot_state.hitstun_frames_left < 32:
            return False

        angle = PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)
        tech_angle = FrameDataUtils.get_combo_di_launch_angle(angle)
        v_knockback = PlayerStateUtils.get_knockback_magnitude(smashbot_state, opponent_state) * sin(radians(tech_angle))
        # If grounded after ASDI down and 1 gravity frame, can Amsah tech
        if v_knockback > 3 + FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]["Gravity"]:
            return False

        # Cannot stick on ground if close to ledge (need "- 6" because you move when inputting TDI)
        return abs(smashbot_state.x) <= stage_edge - 6

    @staticmethod
    def should_slide_off(smashbot_state, opponent_state, stage_edge):
        # If we do not want to slide off, do not
        if DifficultySettings.AMSAH_TECH != AMSAH_TECH_MODE.SMART:
            return False

        x = smashbot_state.position.x
        angle = FrameDataUtils.get_combo_di_launch_angle(PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state))
        knockback_x = PlayerStateUtils.get_knockback_magnitude(smashbot_state, opponent_state) * math.cos(math.radians(angle))
        # If knockback is too strong, do not slide off
        if abs(knockback_x) > 3.2:
            return False

        # If facing away from knockback, do not slide off
        if smashbot_state.facing == (knockback_x > 0):
            return False

        # There is a point where slide deceleration transfers from normal knockback deceleration to character friction, but the timing
        # is different for each character, so just use whatever decelerates more
        deceleration = max(FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]["Friction"], 0.051)

        frames = 0
        # If we slide off within 30 frames, then it's safe
        while abs(knockback_x) > 0 and frames < 30:
            knockback_x = max(knockback_x - deceleration * Utils.sign(knockback_x), 0)
            x += knockback_x
            frames += 1
            if abs(x) > stage_edge:
                return True

        return False

    def __init__(self):
        self.x = None
        self.y = None
        self.teched = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.x is None or self.y is None:
            inputs = AngleUtils.angle_to_xy(FrameDataUtils.get_combo_di(PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)))
            self.x = inputs[0]
            self.y = inputs[1]

        # Hold direction for tech
        if not self.teched:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, self.x, self.y)
            controller.tilt_analog(Button.BUTTON_C, 0.5, 0)

            # Input the tech
            if smashbot_state.hitlag_left == 1:
                # Slide off instead if possible
                if not AmsahTech.should_slide_off(smashbot_state, opponent_state, GameStateUtils.get_stage_edge(game_state)):
                    controller.press_button(Button.BUTTON_L)
                self.teched = True

            return True

        # Wait for the tech animation to end
        if PlayerStateUtils.is_teching(smashbot_state) or smashbot_state.action == Action.SPOTDODGE:
            self.interruptable = False
            self.teched = True
            controller.release_button(Button.BUTTON_L)
            return True

        return False
