from Utils.mathutils import MathUtils
from Utils.vector2 import Vector2


class Knockback:
    DECELERATION = 0.051

    @classmethod
    def zero(cls):
        return Knockback(Vector2.zero())

    def __init__(self, vector):
        self.vector = vector

    def get_total_displacement(self, num_frames):
        magnitude = self.vector.get_magnitude()
        end_magnitude = max(magnitude - Knockback.DECELERATION * num_frames, 0)
        return self.vector.with_magnitude(MathUtils.linear_sum(magnitude, end_magnitude, -Knockback.DECELERATION))

    def get_x(self):
        return self.vector.x

    def get_y(self):
        return self.vector.y

    def to_angle(self):
        return self.vector.to_angle()

    def with_angle(self, angle):
        return Knockback(self.vector.with_angle(angle))

    def get_magnitude(self):
        return self.vector.get_magnitude()

    def with_magnitude(self, magnitude):
        return Knockback(self.vector.with_magnitude(magnitude))

    def with_advanced_frames(self, num_frames):
        return Knockback(self.vector.with_magnitude(max(self.vector.get_magnitude() - Knockback.DECELERATION * num_frames, 0)))

    def __str__(self):
        return "Knockback{x=" + str(self.get_x()) + ", y=" + str(self.get_y()) + "}"