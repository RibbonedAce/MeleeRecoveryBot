from Utils.enums import FRAME_INPUT_TYPE
from Utils.vector2 import Vector2


class FrameInput:
    @classmethod
    def forward(cls):
        return FrameInput(FRAME_INPUT_TYPE.FADE_FORWARD)

    @classmethod
    def backward(cls):
        return FrameInput(FRAME_INPUT_TYPE.FADE_BACKWARD)

    @classmethod
    def direct(cls, s_input):
        return FrameInput(FRAME_INPUT_TYPE.DIRECT, s_input)

    def __init__(self, f_type, s_input=Vector2.zero()):
        self.f_type = f_type
        self.s_input = s_input