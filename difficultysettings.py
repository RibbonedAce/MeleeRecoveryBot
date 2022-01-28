import random

from Utils.enums import AMSAH_TECH_MODE, FADE_BACK_MODE, FAST_FALL_MODE, RECOVER_HEIGHT, RECOVER_MODE, STALL_MODE, TDI_MODE
from Utils.mathutils import MathUtils


class DifficultySettings:
    FADE_BACK_NONE_WEIGHT = 1
    FADE_BACK_EARLY_WEIGHT = 1
    FADE_BACK_LATE_WEIGHT = 1
    TARGET_STAGE_WEIGHT = 1
    TARGET_LEDGE_WEIGHT = 1
    RECOVER_MAX_WEIGHT = 1
    RECOVER_STAGE_WEIGHT = 1
    RECOVER_LEDGE_WEIGHT = 1
    PRIMARY_RECOVERY_WEIGHT = 1
    SECONDARY_RECOVERY_WEIGHT = 1
    AIR_DODGE_WEIGHT = 1

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
    def get_fade_back_mode():
        total = DifficultySettings.FADE_BACK_EARLY_WEIGHT + \
              DifficultySettings.FADE_BACK_LATE_WEIGHT + \
              DifficultySettings.FADE_BACK_NONE_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.FADE_BACK_EARLY_WEIGHT
        if num < 0:
            return FADE_BACK_MODE.EARLY

        num -= DifficultySettings.FADE_BACK_LATE_WEIGHT
        if num < 0:
            return FADE_BACK_MODE.LATE

        return FADE_BACK_MODE.NONE

    @staticmethod
    def get_target_height():
        total = DifficultySettings.TARGET_LEDGE_WEIGHT + \
                DifficultySettings.TARGET_STAGE_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.TARGET_LEDGE_WEIGHT
        if num < 0:
            return RECOVER_HEIGHT.LEDGE

        return RECOVER_HEIGHT.STAGE

    @staticmethod
    def get_recover_height():
        total = DifficultySettings.RECOVER_LEDGE_WEIGHT + \
                DifficultySettings.RECOVER_STAGE_WEIGHT + \
                DifficultySettings.RECOVER_MAX_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.RECOVER_LEDGE_WEIGHT
        if num < 0:
            return RECOVER_HEIGHT.LEDGE

        num -= DifficultySettings.RECOVER_STAGE_WEIGHT
        if num < 0:
            return RECOVER_HEIGHT.STAGE

        return RECOVER_HEIGHT.MAX

    @staticmethod
    def get_recover_mode():
        total = DifficultySettings.SECONDARY_RECOVERY_WEIGHT + \
                DifficultySettings.AIR_DODGE_WEIGHT + \
                DifficultySettings.PRIMARY_RECOVERY_WEIGHT
        num = DifficultySettings.__random_float(0, total)

        num -= DifficultySettings.AIR_DODGE_WEIGHT
        if num < 0:
            return RECOVER_MODE.AIR_DODGE

        num -= DifficultySettings.SECONDARY_RECOVERY_WEIGHT
        if num < 0:
            return RECOVER_MODE.SECONDARY

        return RECOVER_MODE.PRIMARY

    @staticmethod
    def should_ledge_tech():
        return random.random() < DifficultySettings.LEDGE_TECH_CHANCE

    @staticmethod
    def should_reverse():
        return random.random() < DifficultySettings.REVERSE_RECOVERY_CHANCE

    @staticmethod
    def __random_float(start, stop):
        return MathUtils.lerp(start, stop, random.random())

    @staticmethod
    def initialize_difficulty(difficulty):
        if difficulty == 0:
            DifficultySettings.FADE_BACK_NONE_WEIGHT = 1
            DifficultySettings.FADE_BACK_EARLY_WEIGHT = 0
            DifficultySettings.FADE_BACK_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_WEIGHT = 0
            DifficultySettings.RECOVER_MAX_WEIGHT = 1
            DifficultySettings.RECOVER_STAGE_WEIGHT = 0
            DifficultySettings.RECOVER_LEDGE_WEIGHT = 0
            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 0
            DifficultySettings.AIR_DODGE_WEIGHT = 0

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
            DifficultySettings.FADE_BACK_NONE_WEIGHT = 1
            DifficultySettings.FADE_BACK_EARLY_WEIGHT = 0
            DifficultySettings.FADE_BACK_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_WEIGHT = 0
            DifficultySettings.TARGET_LEDGE_WEIGHT = 1
            DifficultySettings.RECOVER_MAX_WEIGHT = 1
            DifficultySettings.RECOVER_STAGE_WEIGHT = 0
            DifficultySettings.RECOVER_LEDGE_WEIGHT = 1
            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 0
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 0

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
            DifficultySettings.FADE_BACK_NONE_WEIGHT = 1
            DifficultySettings.FADE_BACK_EARLY_WEIGHT = 0.5
            DifficultySettings.FADE_BACK_LATE_WEIGHT = 0
            DifficultySettings.TARGET_STAGE_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_WEIGHT = 1
            DifficultySettings.RECOVER_MAX_WEIGHT = 1
            DifficultySettings.RECOVER_STAGE_WEIGHT = 1
            DifficultySettings.RECOVER_LEDGE_WEIGHT = 1
            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 0
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 1

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
            DifficultySettings.FADE_BACK_NONE_WEIGHT = 1
            DifficultySettings.FADE_BACK_EARLY_WEIGHT = 1
            DifficultySettings.FADE_BACK_LATE_WEIGHT = 0.5
            DifficultySettings.TARGET_STAGE_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_WEIGHT = 1
            DifficultySettings.RECOVER_MAX_WEIGHT = 1
            DifficultySettings.RECOVER_STAGE_WEIGHT = 1
            DifficultySettings.RECOVER_LEDGE_WEIGHT = 1
            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 1
            DifficultySettings.AIR_DODGE_WEIGHT = 1

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
            DifficultySettings.FADE_BACK_NONE_WEIGHT = 1
            DifficultySettings.FADE_BACK_EARLY_WEIGHT = 1
            DifficultySettings.FADE_BACK_LATE_WEIGHT = 1
            DifficultySettings.TARGET_STAGE_WEIGHT = 1
            DifficultySettings.TARGET_LEDGE_WEIGHT = 1
            DifficultySettings.RECOVER_MAX_WEIGHT = 1
            DifficultySettings.RECOVER_STAGE_WEIGHT = 1
            DifficultySettings.RECOVER_LEDGE_WEIGHT = 1
            DifficultySettings.PRIMARY_RECOVERY_WEIGHT = 1
            DifficultySettings.SECONDARY_RECOVERY_WEIGHT = 0.25
            DifficultySettings.AIR_DODGE_WEIGHT = 0.25

            DifficultySettings.REVERSE_RECOVERY_CHANCE = 1
            DifficultySettings.LEDGE_TECH_CHANCE = 1
            DifficultySettings.SWEET_SPOT_CHANCE = 0.25
            DifficultySettings.SDI_AMOUNT = 1
            DifficultySettings.DANGER_THRESHOLD = 30
            DifficultySettings.FAST_FALL = FAST_FALL_MODE.ALWAYS
            DifficultySettings.STALL = STALL_MODE.SMART
            DifficultySettings.TDI = TDI_MODE.SMART
            DifficultySettings.AMSAH_TECH = AMSAH_TECH_MODE.SMART
            DifficultySettings.METEOR_CANCEL_FRAME = 8