import math

from melee.enums import Button

from Chains.amsahtech import AmsahTech
from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import Angle, LogUtils, MathUtils, Vector2


class SDI(Chain):
    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.hitlag_left > 2

    @classmethod
    def __cardinal_left(cls, cardinal):
        # For the given cardinal, return the cardinal to the left of it
        degrees = cardinal.to_angle().get_degrees()
        if degrees <= 17 or degrees >= 343:
            new_degrees = 18
        elif 17 < degrees < 73:
            new_degrees = 90
        elif 73 <= degrees <= 107:
            new_degrees = 108
        elif 107 < degrees < 163:
            new_degrees = 180
        elif 163 <= degrees <= 197:
            new_degrees = 198
        elif 197 < degrees < 253:
            new_degrees = 270
        elif 253 <= degrees <= 287:
            new_degrees = 288
        else:
            new_degrees = 0

        return Vector2.from_angle(Angle(new_degrees))

    @classmethod
    def __cardinal_right(cls, cardinal):
        # For the given cardinal, return the cardinal to the right of it
        degrees = cardinal.to_angle().get_degrees()
        if degrees <= 17 or degrees >= 343:
            new_degrees = 342
        elif 17 < degrees < 73:
            new_degrees = 0
        elif 73 <= degrees <= 107:
            new_degrees = 72
        elif 107 < degrees < 163:
            new_degrees = 90
        elif 163 <= degrees <= 197:
            new_degrees = 162
        elif 197 < degrees < 253:
            new_degrees = 180
        elif 253 <= degrees <= 287:
            new_degrees = 252
        else:
            new_degrees = 270

        return Vector2.from_angle(Angle(new_degrees))

    @classmethod
    def __touching_ground(cls, smashbot_state):
        # Returns whether we're on top of the ground, but not necessarily triggering the on_ground flag
        # If we're on the ground, we don't want to DI down, so it's important to know
        # Todo: consider platforms
        return smashbot_state.on_ground or not smashbot_state.off_stage and smashbot_state.position.y < 0.25

    def __init__(self):
        Chain.__init__(self)
        self.cardinal = None
        self.frames = 0
        self.last_input = 0
        self.last_sdi = 0
        self.frame_threshold = 1 / max(DifficultySettings.SDI_AMOUNT, 0.01)

    def step_internal(self, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]
        controller = self.controller
        self.interruptable = True

        # There's three kinds of SDI:
        #   1) Survival SDI
        #   2) Combo SDI
        #   3) Situationally-specific SDI

        # SDI implementation
        # We break up SDI into 8 possible directions. 4 cardinal directions and 4 diagonals
        #   Every SDI targets one of these 8 directions and wiggles back and forth across the direction

        if self.cardinal is None:
            stage_edge = game_state.get_stage_edge()
            knockback = smashbot_state.get_knockback(opponent_state)
            no_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, knockback)

            # Situationally-specific SDI
            #   We're off the stage, or we're hit by a spike, so let's SDI back onto the stage
            if smashbot_state.off_stage or knockback.get_y() < 0:
                angle = Angle(90 + 90 * MathUtils.sign(smashbot_state.position.x))
                LogUtils.simple_log("Off-stage SDI cardinal:", angle)

            #   SDI down so that we can Amsah tech
            elif AmsahTech.primary_conditions_met(propagate) and AmsahTech.more_sdi_needed(smashbot_state):
                angle = Angle(-90)
                LogUtils.simple_log("Amsah Tech SDI cardinal:", angle)

            # Survival SDI
            #   If we're at risk of dying from the hit, then SDI backwards to go further back to cut into the knockback
            elif no_di_danger > DifficultySettings.DANGER_THRESHOLD * (smashbot_state.jumps_left + 1):
                # Which cardinal direction is the most opposite the direction?
                angle = knockback.to_angle() + Angle.circle() / 2
                LogUtils.simple_log("Survival SDI angle:", angle, smashbot_state.speed_y_attack, smashbot_state.speed_x_attack)

            # Combo SDI
            #   SDI away from the opponent to keep from following up
            else:
                angle = knockback.to_angle()
                if smashbot_state.on_ground:
                    angle = Angle(math.atan2(smashbot_state.position.y - opponent_state.position.y, smashbot_state.position.x - opponent_state.position.x), Angle.Mode.RADIANS)
                LogUtils.simple_log("Combo SDI angle:", angle)

            self.cardinal = Vector2.from_angle(angle.correct_for_cardinal())
            # If on ground, then we can't SDI up or down
            if smashbot_state.on_ground:
                self.cardinal = Vector2(MathUtils.sign(angle.get_x()), 0)

        LogUtils.simple_log("Committed SDI cardinal:", self.cardinal)

        self.frames += 1
        s_input = Vector2.zero()
        if self.frames >= self.frame_threshold:
            self.frames -= self.frame_threshold

            # If we're on the ground, and want to move horizontally, just alternate neutral and the direction
            #   This will avoid accidentally moving upwards
            if self.__touching_ground(smashbot_state) and self.cardinal.y == 0:
                # Return to neutral if held in any direction
                if self.last_input != 0:
                    s_input = Vector2.zero()
                    self.last_input = 0
                # Use cardinal directly if held in neutral last time
                elif self.last_input != 1:
                    s_input = Vector2(self.cardinal.x, 0)
                    self.last_input = 1
                    self.last_sdi = 1

            # Use cardinal right if not there before
            elif self.last_input != 2 and self.last_sdi != 2:
                s_input = self.__cardinal_right(self.cardinal)
                self.last_input = 2
                self.last_sdi = 2
            # Use cardinal left if not there before
            elif self.last_input != 3 and self.last_sdi != 3:
                s_input = self.__cardinal_left(self.cardinal)
                self.last_input = 3
                self.last_sdi = 3

        else:
            self.last_input = 0

        controller.tilt_analog_unit(Button.BUTTON_MAIN, s_input.x, s_input.y)
        return True