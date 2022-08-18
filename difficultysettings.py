import random

from Utils import MathUtils, RecoveryTarget
from Utils.enums import AMSAH_TECH_MODE, FAST_FALL_MODE, RECOVERY_MODE, STALL_MODE, TDI_MODE


class DifficultySettings:
    TARGET_MAX_WEIGHT = 1
    TARGET_LEDGE_EARLY_WEIGHT = 1
    TARGET_LEDGE_LATE_WEIGHT = 1
    TARGET_LEDGE_RIDE_WEIGHT = 1
    TARGET_STAGE_EARLY_WEIGHT = 1
    TARGET_STAGE_LATE_WEIGHT = 1
    TARGET_STAGE_RIDE_WEIGHT = 1
    TARGET_SWEET_SPOT_WEIGHT = 1

    PRIMARY_RECOVERY_WEIGHT = 1
    SECONDARY_RECOVERY_WEIGHT = 1
    AIR_DODGE_WEIGHT = 1
    HOLD_DRIFT_CHANCE = 0.5
    REVERSE_RECOVERY_CHANCE = 1
    LEDGE_TECH_CHANCE = 1
    SDI_AMOUNT = 1
    DANGER_THRESHOLD = 30
    FAST_FALL = FAST_FALL_MODE.ALWAYS
    STALL = STALL_MODE.SMART
    TDI = TDI_MODE.SMART
    AMSAH_TECH = AMSAH_TECH_MODE.SMART
    METEOR_CANCEL_FRAME = 8

    @staticmethod
    def get_recovery_target():
        total = DifficultySettings.TARGET_MAX_WEIGHT + \
                DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT + \
                DifficultySettings.TARGET_LEDGE_LATE_WEIGHT + \
                DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT + \
                DifficultySettings.TARGET_STAGE_EARLY_WEIGHT + \
                DifficultySettings.TARGET_STAGE_LATE_WEIGHT + \
                DifficultySettings.TARGET_STAGE_RIDE_WEIGHT + \
                DifficultySettings.TARGET_SWEET_SPOT_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.TARGET_MAX_WEIGHT
        if num < 0:
            return RecoveryTarget.max()

        num -= DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT
        if num < 0:
            return RecoveryTarget.ledge_early()

        num -= DifficultySettings.TARGET_LEDGE_LATE_WEIGHT
        if num < 0:
            return RecoveryTarget.ledge_late()

        num -= DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT
        if num < 0:
            return RecoveryTarget.ledge_ride()

        num -= DifficultySettings.TARGET_STAGE_EARLY_WEIGHT
        if num < 0:
            return RecoveryTarget.stage_early()

        num -= DifficultySettings.TARGET_STAGE_LATE_WEIGHT
        if num < 0:
            return RecoveryTarget.stage_late()

        num -= DifficultySettings.TARGET_STAGE_RIDE_WEIGHT
        if num < 0:
            return RecoveryTarget.stage_ride()

        return RecoveryTarget.sweet_spot()

    @staticmethod
    def get_recovery_mode():
        total = DifficultySettings.SECONDARY_RECOVERY_WEIGHT + \
                DifficultySettings.AIR_DODGE_WEIGHT + \
                DifficultySettings.PRIMARY_RECOVERY_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.AIR_DODGE_WEIGHT
        if num < 0:
            return RECOVERY_MODE.AIR_DODGE

        num -= DifficultySettings.SECONDARY_RECOVERY_WEIGHT
        if num < 0:
            return RECOVERY_MODE.SECONDARY

        return RECOVERY_MODE.PRIMARY

    @staticmethod
    def should_ledge_tech():
        return random.random() < DifficultySettings.LEDGE_TECH_CHANCE

    @staticmethod
    def should_reverse():
        return random.random() < DifficultySettings.REVERSE_RECOVERY_CHANCE

    @staticmethod
    def should_hold_drift():
        return random.random() < DifficultySettings.HOLD_DRIFT_CHANCE

    @staticmethod
    def __random_float(start, stop):
        return MathUtils.lerp(start, stop, random.random())

    @staticmethod
    def initialize_difficulty(difficulty):
        if difficulty == 0:
            DifficultySettings.TARGET_MAX_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_EARLY_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_RIDE_WEIGHT = 0
            DifficultySettings.TARGET_SWEET_SPOT_WEIGHT = 0

            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 0
            DifficultySettings.AIR_DODGE_WEIGHT = 0
            DifficultySettings.HOLD_DRIFT_CHANCE = 0
            DifficultySettings.REVERSE_RECOVERY_CHANCE = 0
            DifficultySettings.LEDGE_TECH_CHANCE = 0
            DifficultySettings.SDI_AMOUNT = 0
            DifficultySettings.DANGER_THRESHOLD = -5
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.NEVER
            DifficultySettings.STALL = STALL_MODE.NEVER
            DifficultySettings.TDI = TDI_MODE.NONE
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.NEVER
            DifficultySettings.METEOR_CANCEL_FRAME = 100

        elif difficulty == 1:
            DifficultySettings.TARGET_MAX_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_EARLY_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_RIDE_WEIGHT = 0
            DifficultySettings.TARGET_SWEET_SPOT_WEIGHT = 0

            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 0
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 0
            DifficultySettings.HOLD_DRIFT_CHANCE = 0
            DifficultySettings.REVERSE_RECOVERY_CHANCE = 0
            DifficultySettings.LEDGE_TECH_CHANCE = 0
            DifficultySettings.SDI_AMOUNT = 0
            DifficultySettings.DANGER_THRESHOLD = -5
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.NEVER
            DifficultySettings.STALL = STALL_MODE.ALWAYS
            DifficultySettings.TDI = TDI_MODE.SMART
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.NEVER
            DifficultySettings.METEOR_CANCEL_FRAME = 30

        elif difficulty == 2:
            DifficultySettings.TARGET_MAX_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT = 0.5
            DifficultySettings.TARGET_LEDGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_EARLY_WEIGHT = 0.5
            DifficultySettings.TARGET_STAGE_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_SWEET_SPOT_WEIGHT = 0.5

            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 0
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 1
            DifficultySettings.HOLD_DRIFT_CHANCE = 1
            DifficultySettings.REVERSE_RECOVERY_CHANCE = 0
            DifficultySettings.LEDGE_TECH_CHANCE = 0.5
            DifficultySettings.SDI_AMOUNT = 0.2
            DifficultySettings.DANGER_THRESHOLD = 15
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.ALWAYS
            DifficultySettings.STALL = STALL_MODE.SMART
            DifficultySettings.TDI = TDI_MODE.SMART
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.ALWAYS
            DifficultySettings.METEOR_CANCEL_FRAME = 15

        elif difficulty == 3:
            DifficultySettings.TARGET_MAX_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_LATE_WEIGHT = 0.5
            DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_EARLY_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_LATE_WEIGHT = 0.5
            DifficultySettings.TARGET_STAGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_SWEET_SPOT_WEIGHT = 1

            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 1
            DifficultySettings.HOLD_DRIFT_CHANCE = 0.5
            DifficultySettings.REVERSE_RECOVERY_CHANCE = 0.25
            DifficultySettings.LEDGE_TECH_CHANCE = 1
            DifficultySettings.SDI_AMOUNT = 0.4
            DifficultySettings.DANGER_THRESHOLD = 30
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.ALWAYS
            DifficultySettings.STALL = STALL_MODE.SMART
            DifficultySettings.TDI = TDI_MODE.SMART
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.SMART
            DifficultySettings.METEOR_CANCEL_FRAME = 8

        else:
            DifficultySettings.TARGET_MAX_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_EARLY_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_LATE_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_EARLY_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_LATE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_RIDE_WEIGHT = 1
            DifficultySettings.TARGET_SWEET_SPOT_WEIGHT = 1

            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 0.5
            DifficultySettings.HOLD_DRIFT_CHANCE = 0.5
            DifficultySettings.REVERSE_RECOVERY_CHANCE = 1
            DifficultySettings.LEDGE_TECH_CHANCE = 1
            DifficultySettings.SDI_AMOUNT = 1
            DifficultySettings.DANGER_THRESHOLD = 30
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.ALWAYS
            DifficultySettings.STALL = STALL_MODE.SMART
            DifficultySettings.TDI = TDI_MODE.SMART
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.SMART
            DifficultySettings.METEOR_CANCEL_FRAME = 8