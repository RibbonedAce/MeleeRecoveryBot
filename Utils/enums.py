from enum import Enum


class FADE_BACK_MODE(Enum):
    NONE = 0
    EARLY = 1
    LATE = 2

class RECOVERY_HEIGHT(Enum):
    MAX = 0
    STAGE = 1
    LEDGE = 2

class AMSAH_TECH_MODE(Enum):
    NEVER = 0
    ALWAYS = 1
    SMART = 2

class RECOVERY_MODE(Enum):
    PRIMARY = 0
    SECONDARY = 1
    AIR_DODGE = 2

class TDI_MODE(Enum):
    NONE = 0
    SMART = 1

class STALL_MODE(Enum):
    NEVER = 0
    ALWAYS = 1
    SMART = 2

class FAST_FALL_MODE(Enum):
    NEVER = 0
    ALWAYS = 1