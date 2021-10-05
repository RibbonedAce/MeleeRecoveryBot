import math

from melee.enums import Button

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils.angleutils import AngleUtils
from Utils.mathutils import MathUtils


class SDI(Chain):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.hitlag_left > 2

    @staticmethod
    def angle_to_cardinal(angle):
        """For the given angle, return the nearest cardinal (8 directions) direction"""
        corrected_angle = AngleUtils.correct_for_cardinal(angle)
        return AngleUtils.angle_to_xy(corrected_angle)

    @staticmethod
    def cardinal_left(cardinal):
        """For the given cardinal, return the cardinal to the left of it"""
        angle = AngleUtils.refit_angle(math.degrees(math.atan2(cardinal[1] * 2 - 1, cardinal[0] * 2 - 1)))
        if angle <= 17 or angle >= 343:
            new_angle = 18
        elif 17 < angle < 73:
            new_angle = 90
        elif 73 <= angle <= 107:
            new_angle = 108
        elif 107 < angle < 163:
            new_angle = 180
        elif 163 <= angle <= 197:
            new_angle = 198
        elif 197 < angle < 253:
            new_angle = 270
        elif 253 <= angle <= 287:
            new_angle = 288
        else:
            new_angle = 0

        return AngleUtils.angle_to_xy(new_angle)

    @staticmethod
    def cardinal_right(cardinal):
        """For the given cardinal, return the cardinal to the left of it"""
        angle = AngleUtils.refit_angle(math.degrees(math.atan2(cardinal[1] * 2 - 1, cardinal[0] * 2 - 1)))
        if angle <= 17 or angle >= 343:
            new_angle = 342
        elif 17 < angle < 73:
            new_angle = 0
        elif 73 <= angle <= 107:
            new_angle = 72
        elif 107 < angle < 163:
            new_angle = 90
        elif 163 <= angle <= 197:
            new_angle = 162
        elif 197 < angle < 253:
            new_angle = 180
        elif 253 <= angle <= 287:
            new_angle = 252
        else:
            new_angle = 270

        return AngleUtils.angle_to_xy(new_angle)

    @staticmethod
    def touching_ground(smashbot_state):
        """Returns whether we're on top of the ground, but not necessarily triggering the on_ground flag

        If we're on the ground, we don't want to DI down, so it's important to know
        """
        # Todo: consider platforms
        return smashbot_state.on_ground or not smashbot_state.off_stage and smashbot_state.position.y < 0.25

    def __init__(self):
        Chain.__init__(self)
        self.cardinal = None
        self.frames = 0
        self.last_input = 0
        self.last_sdi = 0
        self.frame_threshold = 1 / max(DifficultySettings.SDI_AMOUNT, 0.01)

    def step_internal(self, game_state, smashbot_state, opponent_state):
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
            knockback_angle = smashbot_state.get_knockback_angle(opponent_state)
            no_di_danger = smashbot_state.get_knockback_danger(opponent_state, stage_edge, knockback_angle)

            # Situationally-specific SDI
            #   Some hits require specific SDI to get out of a tricky combo. Account for those first, here
            # We're off the stage, or we're hit by a spike, so let's SDI back onto the stage
            if smashbot_state.off_stage or knockback_angle > 180:
                angle = 90 + 90 * MathUtils.sign(smashbot_state.position.x)
                self.cardinal = SDI.angle_to_cardinal(angle)
                if self.logger:
                    self.logger.log("Notes", " Off-stage SDI cardinal: " + str(self.cardinal) + " ", concat=True)

            # Survival SDI
            #   If we're at risk of dying from the hit, then SDI backwards to go further back to cut into the knockback
            elif no_di_danger > DifficultySettings.DANGER_THRESHOLD * (smashbot_state.jumps_left + 1):
                # Which cardinal direction is the most opposite the direction?
                angle = AngleUtils.refit_angle(knockback_angle + 180)
                self.cardinal = SDI.angle_to_cardinal(angle)
                if self.logger:
                    self.logger.log("Notes", " Survival SDI angle: " + str(angle) + " " + str(
                        smashbot_state.speed_y_attack) + " " + str(smashbot_state.speed_x_attack), concat=True)

            # Combo SDI
            #   SDI away from the opponent to keep from from following up
            else:
                angle = math.degrees(math.atan2(smashbot_state.position.y - opponent_state.position.y,
                                                smashbot_state.position.x - opponent_state.position.x))
                angle = AngleUtils.refit_angle(angle)
                self.cardinal = SDI.angle_to_cardinal(angle)
                if self.logger:
                    self.logger.log("Notes", " Combo SDI angle: " + str(angle) + " ", concat=True)

            # If on ground, then we can't SDI up or down
            if smashbot_state.on_ground:
                self.cardinal = (int(angle < 90 or angle > 270), 0.5)

            # If we're not ON the actual ground, but touching it, then don't SDI down
            if SDI.touching_ground(smashbot_state):
                if self.cardinal[1] == 0:
                    self.cardinal = (self.cardinal[0], 0.5)
                    if self.cardinal[0] == 0.5:
                        self.cardinal = (int(angle < 90 or angle > 270), 0.5)

        if self.logger:
            self.logger.log("Notes", " Committed SDI cardinal: " + str(self.cardinal) + " ", concat=True)

        self.frames += 1
        x, y = 0.5, 0.5
        if self.frames >= self.frame_threshold:
            self.frames -= self.frame_threshold

            # If we're on the ground, and want to move horizontally, just alternate neutral and the direction
            #   This will avoid accidentally moving upwards
            if SDI.touching_ground(smashbot_state) and self.cardinal[1] == 0.5:
                # Return to neutral if held in any direction
                if self.last_input != 0:
                    x, y = 0.5, 0.5
                    self.last_input = 0
                # Use cardinal directly if held in neutral last time
                elif self.last_input != 1:
                    x, y = self.cardinal[0], 0.5
                    self.last_input = 1
                    self.last_sdi = 1

            # Use cardinal right if not there before
            elif self.last_input != 2 and self.last_sdi != 2:
                x, y = SDI.cardinal_right(self.cardinal)
                self.last_input = 2
                self.last_sdi = 2
            # Use cardinal left if not there before
            elif self.last_input != 3 and self.last_sdi != 3:
                x, y = SDI.cardinal_left(self.cardinal)
                self.last_input = 3
                self.last_sdi = 3

        else:
            self.last_input = 0

        controller.tilt_analog(Button.BUTTON_MAIN, x, y)
        return True