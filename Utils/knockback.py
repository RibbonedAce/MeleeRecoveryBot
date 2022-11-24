import math

from Utils import MathUtils


class Knockback:
    DECELERATION = 0.051

    @staticmethod
    def zero():
        return Knockback(0, 0)

    def __init__(self, angle, magnitude):
        self.angle = angle
        self.magnitude = magnitude

    def get_total_displacement(self, num_frames):
        end_magnitude = max(self.magnitude - Knockback.DECELERATION * num_frames, 0)
        total_magnitude = MathUtils.linear_sum(self.magnitude, end_magnitude, -0.051)
        return total_magnitude * math.cos(math.radians(self.angle)), total_magnitude * math.sin(math.radians(self.angle))

    def get_horizontal_displacement(self):
        return math.cos(math.radians(self.angle)) * self.magnitude

    def get_vertical_displacement(self):
        return math.sin(math.radians(self.angle)) * self.magnitude

    def with_advanced_frames(self, num_frames):
        return Knockback(self.angle, max(self.magnitude - Knockback.DECELERATION * num_frames, 0))