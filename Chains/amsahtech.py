from melee import Action, Button, FrameData, GameState

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import Knockback, MathUtils, Vector2
from Utils.enums import AMSAH_TECH_MODE


class AmsahTech(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return cls.primary_conditions_met(propagate) and not cls.more_sdi_needed(smashbot_state)

    @classmethod
    def primary_conditions_met(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        tech_mode = DifficultySettings.AMSAH_TECH
        # If we do not want to tech, do not
        if tech_mode == AMSAH_TECH_MODE.NEVER:
            return False

        # If cannot tech knockback angle/magnitude, do not tech
        if not cls.__knockback_is_techable(propagate):
            return False

        stage_edge = game_state.get_stage_edge()
        x = smashbot_state.position.x
        # Cannot Amsah tech if close to edge (need "- 6" since inputting TDI moves character)
        if abs(x) > stage_edge - 6:
            return False

        can_slide_off = cls.__should_slide_off(smashbot_state, opponent_state, stage_edge)
        # Cannot Amsah tech if in tech lockout unless you can also slide off
        if GameState.TECH_LOCKOUT[smashbot_state.get_port(game_state)] > smashbot_state.hitlag_left - 2 and not can_slide_off:
            return False

        # If we want to tech no matter what, do it
        if tech_mode == AMSAH_TECH_MODE.ALWAYS:
            return True

        angle = smashbot_state.get_knockback(opponent_state).to_angle()
        angle_x = angle.get_x()
        # Should not Amsah tech if close to opponent when tech is finished
        if angle_x > 0 and x > stage_edge - 30 or \
                angle_x < 0 and x < -(stage_edge - 30):
            # Unless we can slide off or Amsah tech is the only way to survive the hit
            if can_slide_off:
                return True
            survival_angle = angle.to_survival_di_launch(x)
            return smashbot_state.get_knockback_danger(opponent_state, game_state, survival_angle) > DifficultySettings.DANGER_THRESHOLD * 2

        return True

    @classmethod
    def more_sdi_needed(cls, smashbot_state):
        # We can still SDI if we have more hit-lag
        if smashbot_state.hitlag_left != 2:
            return True

        # We should still try to SDI if we are above the ground
        if smashbot_state.position.y + smashbot_state.ecb.bottom.y > 3:
            return True

        return False

    @classmethod
    def __knockback_is_techable(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        # We should not SDI if the total hit-lag is too large (ECB shenanigans)
        if smashbot_state.get_incurred_hit_lag(game_state) > 9:
            return False

        # Cannot stick on ground if you don't go into knockdown
        if smashbot_state.hitstun_frames_left < 32:
            return False

        knockback = smashbot_state.get_knockback(opponent_state)
        knockback = knockback.with_angle(knockback.to_angle().to_combo_di_launch())
        knockback_y = knockback.get_y()
        # If not grounded after ASDI down and 1 gravity frame, can't Amsah tech
        if knockback_y > 3 + FrameData.INSTANCE.get_gravity(smashbot_state.character):
            return False

        return True

    @classmethod
    def __should_slide_off(cls, smashbot_state, opponent_state, stage_edge):
        # If we do not want to slide off, do not
        if DifficultySettings.AMSAH_TECH != AMSAH_TECH_MODE.SMART:
            return False

        x = smashbot_state.position.x
        knockback = smashbot_state.get_knockback(opponent_state)
        knockback = knockback.with_angle(knockback.to_angle().to_combo_di_launch())
        knockback_x = knockback.get_x()
        # If knockback is too strong, do not slide off
        if abs(knockback_x) > 3:
            return False

        # If facing away from knockback, do not slide off
        if smashbot_state.facing == (knockback_x > 0):
            return False

        # There is a point where slide deceleration transfers from normal knockback deceleration to character friction, but the timing
        # is different for each character, so just use whatever decelerates less for now
        deceleration = min(FrameData.INSTANCE.get_friction(smashbot_state.character), Knockback.DECELERATION)

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
        self.s_input = None
        self.teched = False

    def step_internal(self, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]
        controller = self.controller

        if self.s_input is None:
            self.s_input = Vector2.from_angle(smashbot_state.get_knockback(opponent_state).to_angle().to_combo_di())

        # Hold direction for tech
        if not self.teched:
            self.interruptable = False
            controller.tilt_analog_unit(Button.BUTTON_MAIN, self.s_input.x, self.s_input.y)
            controller.tilt_analog_unit(Button.BUTTON_C, 0, -1)

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
