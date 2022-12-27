import math

from Utils.angle import Angle


class Vector2:
    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def from_angle(angle, magnitude=1.0):
        return Vector2(angle.get_x(), angle.get_y()) * magnitude

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_angle_between(self, other):
        return self.to_angle() - other.to_angle()

    def with_magnitude(self, magnitude):
        if self.get_magnitude() == 0:
            return Vector2.zero()
        return self.to_unit() * magnitude

    def to_unit(self):
        return self / self.get_magnitude()

    def to_angle(self):
        return Angle(math.atan2(self.y, self.x), Angle.Mode.RADIANS)

    def rotate(self, angle):
        return self.with_angle(self.to_angle() + angle)

    def with_angle(self, angle):
        return Vector2.from_angle(angle, self.get_magnitude())

    def __str__(self):
        return "Vector2({}, {})".format(self.x, self.y)

    def __add__(self, other):
        if type(other) in {int, float}:
            return Vector2(self.x + other, self.y + other)
        if type(other) is Vector2:
            return Vector2(self.x + other.x, self.y + other.y)

        raise ArithmeticError

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if type(other) in {int, float}:
            return Vector2(self.x * other, self.y * other)

        raise ArithmeticError

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        if type(other) in {int, float, Vector2}:
            return self + other * -1

        raise ArithmeticError

    def __rsub__(self, other):
        return (self - other) * -1

    def __truediv__(self, other):
        if type(other) in {int, float}:
            return self * (1 / other)

        raise ArithmeticError
