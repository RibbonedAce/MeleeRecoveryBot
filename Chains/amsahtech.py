import math
from math import cos, radians, sin

from melee import Action, Button, FrameData, GameState

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import AngleUtils, MathUtils
from Utils.enums import AMSAH_TECH_MODE


class AmsahTech(Chain):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        tech_mode = DifficultySettings.AMSAH_TECH
        # If we do not want to tech, do not
        if tech_mode == AMSAH_TECH_MODE.NEVER:
            return False

        stage_edge = game_state.get_stage_edge()
        # Cannot Amsah tech if can't stick on ground
        if not cls.__can_stick_on_ground(smashbot_state, opponent_state, stage_edge):
            return False

        # Cannot Amsah tech if close to edge (need "- 6" since inputting TDI moves character)
        if abs(smashbot_state.position.x) > stage_edge - 6:
            return False

        can_slide_off = cls.__should_slide_off(smashbot_state, opponent_state, stage_edge)
        # Cannot Amsah tech if in tech lockout unless you can also slide off
        if GameState.TECH_LOCKOUT[smashbot_state.get_port(game_state)] > smashbot_state.hitlag_left - 2 and not can_slide_off:
            return False

        # If we want to tech no matter what, do it
        if tech_mode == AMSAH_TECH_MODE.ALWAYS:
            return True

        angle = smashbot_state.get_knockback_angle(opponent_state)
        x = cos(radians(angle))
        # Should not Amsah tech if close to opponent when tech is finished
        if x > 0 and smashbot_state.position.x > stage_edge - 30 or \
                x < 0 and smashbot_state.position.x < -(stage_edge - 30):
            # Unless we can slide off or Amsah tech is the only way to survive the hit
            if can_slide_off:
                return True
            survival_angle = AngleUtils.get_survival_di_launch_angle(angle, smashbot_state.position.x)
            return smashbot_state.get_knockback_danger(opponent_state, stage_edge, survival_angle) > DifficultySettings.DANGER_THRESHOLD * 2

        return True

    @classmethod
    def __can_stick_on_ground(cls, smashbot_state, opponent_state, stage_edge):
        # Cannot stick on ground if not already there
        if not smashbot_state.on_ground:
            return False

        # Cannot stick on ground if already out of hit-lag (mainly from throws)
        if smashbot_state.hitlag_left != 2:
            return False

        # Cannot stick on ground if in the air
        if smashbot_state.position.y > 3:
            return False

        # Cannot stick on ground if you don't go into knockdown
        if smashbot_state.hitstun_frames_left < 32:
            return False

        angle = smashbot_state.get_knockback_angle(opponent_state)
        tech_angle = AngleUtils.get_combo_di_launch_angle(angle)
        v_knockback = smashbot_state.get_knockback_magnitude(opponent_state) * sin(radians(tech_angle))
        # If grounded after ASDI down and 1 gravity frame, can Amsah tech
        if v_knockback > 3 + FrameData.INSTANCE.get_gravity(smashbot_state.character):
            return False

        # Cannot stick on ground if close to ledge (need "- 6" because you move when inputting TDI)
        return abs(smashbot_state.x) <= stage_edge - 6

    @classmethod
    def __should_slide_off(cls, smashbot_state, opponent_state, stage_edge):
        # If we do not want to slide off, do not
        if DifficultySettings.AMSAH_TECH != AMSAH_TECH_MODE.SMART:
            return False

        x = smashbot_state.position.x
        angle = AngleUtils.get_combo_di_launch_angle(smashbot_state.get_knockback_angle(opponent_state))
        knockback_x = smashbot_state.get_knockback_magnitude(opponent_state) * math.cos(math.radians(angle))
        # If knockback is too strong, do not slide off
        if abs(knockback_x) > 3.2:
            return False

        # If facing away from knockback, do not slide off
        if smashbot_state.facing == (knockback_x > 0):
            return False

        # There is a point where slide deceleration transfers from normal knockback deceleration to character friction, but the timing
        # is different for each character, so just use whatever decelerates more
        deceleration = max(FrameData.INSTANCE.get_friction(smashbot_state.character), 0.051)

        frames = 0
        # If we slide off within 30 frames, then it's safe
        while abs(knockback_x) > 0 and frames < 30:
            knockback_x = max(knockback_x - deceleration * MathUtils.sign(knockback_x), 0)
            x += knockback_x
            frames += 1
            if abs(x) > stage_edge:
                return True

        return False

    def __init__(self):
        Chain.__init__(self)
        self.x = None
        self.y = None
        self.teched = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.x is None or self.y is None:
            inputs = AngleUtils.angle_to_xy(AngleUtils.get_combo_di(smashbot_state.get_knockback_angle(opponent_state)))
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
                if not self.__should_slide_off(smashbot_state, opponent_state, game_state.get_stage_edge()):
                    controller.press_button(Button.BUTTON_L)
                self.teched = True

            return True

        # Wait for the tech animation to end
        if smashbot_state.is_wall_teching() or smashbot_state.action == Action.SPOTDODGE:
            self.interruptable = False
            self.teched = True
            controller.release_button(Button.BUTTON_L)
            return True

        return False
