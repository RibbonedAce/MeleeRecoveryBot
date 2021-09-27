import math

import melee

from Data import AttackData, OtherCharacterData
from Utils.angleutils import AngleUtils
from Utils.trajectoryframe import TrajectoryFrame


class FrameDataUtils:
    INSTANCE = melee.framedata.FrameData()

    @staticmethod
    def create_trajectory_frames(character, start_velocity):
        character_data = FrameDataUtils.INSTANCE.characterdata[character]
        gravity = -character_data["Gravity"]
        mobility = character_data["AirMobility"]
        speed = character_data["AirSpeed"]
        velocity = start_velocity
        frames = []
        term_velocity = min(-character_data["TerminalVelocity"], start_velocity)

        while velocity != term_velocity or len(frames) == 0:
            velocity = max(velocity + gravity, term_velocity)
            frames.append(TrajectoryFrame(
                vertical_velocity=velocity,
                forward_acceleration=mobility,
                backward_acceleration=-mobility,
                min_horizontal_velocity=speed,
                max_horizontal_velocity=-speed))

        return frames

    @staticmethod
    def get_hit_lag_duration(opponent_state, damage):
        d = math.floor(damage)
        e = 1

        attack = AttackData.get_attack(opponent_state)
        # Electric attack hit-stun multiplier
        if attack is not None and attack["Effect"] == "Electric":
            e = 1.5

        return (d / 3 + 3) * e

    @staticmethod
    def get_duration_stuck(opponent_state):
        attack = AttackData.get_attack(opponent_state)
        # Don't assume anything if we can't figure out the attack
        if attack is None:
            return 0

        # If opponent is falling when using an aerial attack, assume that they will land the next frame
        landing_lag = attack["Landing Lag"]
        if landing_lag > 0 and opponent_state.speed_y_self < 0:
            return landing_lag

        # If it's a grounded move or a rising aerial, assume they will go through all of it
        return attack["IASA"] - opponent_state.action_frame

    @staticmethod
    def get_attack_magnitude(smashbot_state, opponent_state):
        attack = AttackData.get_attack(opponent_state)
        # If attack not configured, then return a "moderately powerful" attack
        if attack is None:
            return 3

        p = smashbot_state.percent
        d = attack["Damage"]
        w = OtherCharacterData.get_weight(smashbot_state.character)
        s = attack["KB Growth"]
        b = attack["Base KB"]

        # Set knockback moves
        if attack["Set KB"] != 0:
            p = 10
            d = attack["Set KB"]

        # Weight-independent moves (e.g. throws)
        if not attack["Weight Dependent"]:
            w = 100

        return (((((p / 10 + p * d / 20) * 200 / (w + 100) * 1.4) + 18) * s / 100) + b) * 0.03

    @staticmethod
    def get_attack_angle(opponent_state):
        attack = AttackData.get_attack(opponent_state)
        # If attack not configured, then return 45 degrees
        angle = 45
        if attack is not None:
            angle = attack["Angle"]
        if not opponent_state.facing:
            angle = AngleUtils.get_x_reflection(angle)

        return angle

    @staticmethod
    def get_survival_di(angle, position):
        # Find when to DI left or right
        add_angle = True
        if angle > 180:
            add_angle = position < 0
        else:
            if 90 <= angle <= 180:
                add_angle = not add_angle
            if 73 <= angle <= 107:
                add_angle = not add_angle

        result = AngleUtils.refit_angle(angle - 90)
        if add_angle:
            result = AngleUtils.refit_angle(angle + 90)

        return FrameDataUtils.correct_for_cardinal(result)

    @staticmethod
    def get_combo_di(angle):
        # Find when to DI left or right
        add_angle = False
        if 90 <= angle < 270:
            add_angle = not add_angle
        if angle > 180:
            add_angle = not add_angle

        result = AngleUtils.refit_angle(angle - 90)
        if add_angle:
            result = AngleUtils.refit_angle(angle + 90)

        return FrameDataUtils.correct_for_cardinal(result)

    @staticmethod
    def get_survival_di_launch_angle(angle, position):
        di_angle = FrameDataUtils.get_survival_di(angle, position)
        subtract_angle = 90 <= angle < 180 or angle >= 270

        max_angle = angle + 90
        if subtract_angle:
            max_angle = angle - 90
        influence = math.cos(math.radians(di_angle - max_angle))

        result = angle + 18 * influence
        if subtract_angle:
            result = angle - 18 * influence
        return result

    @staticmethod
    def get_combo_di_launch_angle(angle):
        di_angle = FrameDataUtils.get_combo_di(angle)
        subtract_angle = angle < 90 or 180 <= angle < 270

        max_angle = angle + 90
        if subtract_angle:
            max_angle = angle - 90
        influence = math.cos(math.radians(di_angle - max_angle))

        result = angle + 18 * influence
        if subtract_angle:
            result = angle - 18 * influence
        return result

    @staticmethod
    def correct_for_cardinal(angle):
        # Correct angle based on the cardinal dead-zones
        non_cardinal_angle = (angle + 17) % 90 - 17
        if -17 <= non_cardinal_angle < -8:
            return angle - non_cardinal_angle - 18
        if -8 <= non_cardinal_angle <= 8:
            return angle - non_cardinal_angle
        if 8 < non_cardinal_angle <= 17:
            return angle - non_cardinal_angle + 18
        return angle
