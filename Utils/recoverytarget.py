import random

from Utils.enums import FADE_BACK_MODE, RECOVERY_HEIGHT


class RecoveryTarget:
    __MAX_ONLY = [RECOVERY_HEIGHT.MAX]
    __ALL_HEIGHTS = [RECOVERY_HEIGHT.MAX, RECOVERY_HEIGHT.STAGE, RECOVERY_HEIGHT.LEDGE]
    __NOT_LEDGE = [RECOVERY_HEIGHT.MAX, RECOVERY_HEIGHT.STAGE]
    __NOT_MAX = [RECOVERY_HEIGHT.STAGE, RECOVERY_HEIGHT.LEDGE]
    __STAGE_ONLY = [RECOVERY_HEIGHT.STAGE]

    def __init__(self, height, fade_back_mode, descend, ledge):
        self.height = height
        self.fade_back_mode = fade_back_mode
        self.descend = descend
        self.ledge = ledge

    @staticmethod
    def max():
        return RecoveryTarget(random.choice(RecoveryTarget.__MAX_ONLY), FADE_BACK_MODE.NONE, False, False)

    def is_max(self):
        return self.height in RecoveryTarget.__MAX_ONLY and self.fade_back_mode == FADE_BACK_MODE.NONE and not self.descend and not self.ledge

    @staticmethod
    def ledge_early():
        return RecoveryTarget(random.choice(RecoveryTarget.__ALL_HEIGHTS), FADE_BACK_MODE.EARLY, False, True)

    def is_ledge_early(self):
        return self.height in RecoveryTarget.__ALL_HEIGHTS and self.fade_back_mode == FADE_BACK_MODE.EARLY and not self.descend and self.ledge

    @staticmethod
    def ledge_late():
        return RecoveryTarget(random.choice(RecoveryTarget.__ALL_HEIGHTS), FADE_BACK_MODE.LATE, False, True)

    def is_ledge_late(self):
        return self.height in RecoveryTarget.__ALL_HEIGHTS and self.fade_back_mode == FADE_BACK_MODE.LATE and not self.descend and self.ledge

    @staticmethod
    def ledge_ride():
        return RecoveryTarget(random.choice(RecoveryTarget.__NOT_MAX), FADE_BACK_MODE.NONE, False, True)

    def is_ledge_ride(self):
        return self.height in RecoveryTarget.__NOT_MAX and self.fade_back_mode == FADE_BACK_MODE.NONE and not self.descend and self.ledge

    @staticmethod
    def stage_early():
        return RecoveryTarget(random.choice(RecoveryTarget.__NOT_LEDGE), FADE_BACK_MODE.EARLY, False, False)

    def is_stage_early(self):
        return self.height in RecoveryTarget.__NOT_LEDGE and self.fade_back_mode == FADE_BACK_MODE.EARLY and not self.descend and not self.ledge

    @staticmethod
    def stage_late():
        return RecoveryTarget(random.choice(RecoveryTarget.__NOT_LEDGE), FADE_BACK_MODE.LATE, False, False)

    def is_stage_late(self):
        return self.height in RecoveryTarget.__NOT_LEDGE and self.fade_back_mode == FADE_BACK_MODE.LATE and not self.descend and not self.ledge

    @staticmethod
    def stage_ride():
        return RecoveryTarget(random.choice(RecoveryTarget.__STAGE_ONLY), FADE_BACK_MODE.NONE, False, False)

    def is_stage_ride(self):
        return self.height in RecoveryTarget.__STAGE_ONLY and self.fade_back_mode == FADE_BACK_MODE.NONE and not self.descend and not self.ledge

    @staticmethod
    def sweet_spot():
        return RecoveryTarget(random.choice(RecoveryTarget.__MAX_ONLY), FADE_BACK_MODE.NONE, True, True)

    def is_sweet_spot(self):
        return self.height in RecoveryTarget.__MAX_ONLY and self.fade_back_mode == FADE_BACK_MODE.NONE and self.descend and self.ledge