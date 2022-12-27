import math

from Utils.mathutils import MathUtils


class Angle:
    class Mode:
        DEGREES = 1
        RADIANS = math.pi / 180
        ROTATIONS = 1 / 360

    @staticmethod
    def circle():
        return Angle.non_fit(1, Angle.Mode.ROTATIONS)

    @staticmethod
    def non_fit(amount, mode):
        angle = Angle(amount, mode)
        angle.amount = amount
        return angle

    @staticmethod
    def from_input(s_input, threshold, magnitude):
        return Angle(MathUtils.i_lerp(threshold, 1, abs(s_input.x)) * MathUtils.sign(s_input.x) * -magnitude)

    def __init__(self, amount, mode=Mode.DEGREES):
        self.amount = amount % (mode / Angle.Mode.ROTATIONS)
        self.mode = mode

    def get_degrees(self):
        return self.amount * Angle.Mode.DEGREES / self.mode

    def get_radians(self):
        return self.amount * Angle.Mode.RADIANS / self.mode

    def get_rotations(self):
        return self.amount * Angle.Mode.ROTATIONS / self.mode

    def get_x(self):
        return math.cos(self.get_radians())

    def get_y(self):
        return math.sin(self.get_radians())

    def convert(self, mode):
        return Angle(self.amount * mode / self.mode, mode)

    def x_reflection(self):
        return Angle.circle() / 2 - self

    def y_reflection(self):
        return self * -1

    def correct_for_cardinal(self):
        # Correct angle based on the cardinal dead-zones
        degrees = self.get_degrees()
        non_cardinal_angle = (degrees + 17) % 90 - 17

        if -17 <= non_cardinal_angle < -8:
            degrees = degrees - non_cardinal_angle - 18
        elif -8 <= non_cardinal_angle <= 8:
            degrees = degrees - non_cardinal_angle
        elif 8 < non_cardinal_angle <= 17:
            degrees = degrees - non_cardinal_angle + 18

        return Angle(degrees).convert(self.mode)

    def correct_for_cardinal_strict(self):
        # Correct angle based on the cardinal dead-zones, only going to cardinal if exactly at the right angle
        degrees = self.get_degrees()
        non_cardinal_angle = (degrees + 17) % 90 - 17

        if -17 <= non_cardinal_angle < 0:
            degrees = degrees - non_cardinal_angle - 18
        elif non_cardinal_angle == 0:
            degrees = degrees - non_cardinal_angle
        elif 0 < non_cardinal_angle <= 17:
            degrees = degrees - non_cardinal_angle + 18

        return Angle(degrees).convert(self.mode)

    def to_survival_di(self, position):
        # Find when to DI left or right
        degrees = self.get_degrees()
        add_angle = True

        if degrees > 180:
            add_angle = position < 0
        else:
            if 90 <= degrees <= 180:
                add_angle = not add_angle
            if 73 <= degrees <= 107:
                add_angle = not add_angle

        if add_angle:
            return Angle(degrees + 90).correct_for_cardinal().convert(self.mode)
        return Angle(degrees - 90).correct_for_cardinal().convert(self.mode)

    def to_survival_di_launch(self, position):
        di_degrees = self.to_survival_di(position).get_degrees()
        degrees = self.get_degrees()
        subtract_angle = 90 <= degrees < 180 or degrees >= 270

        max_degrees = degrees + 90
        if subtract_angle:
            max_degrees = degrees - 90
        influence_degrees = 18 * math.cos(math.radians(di_degrees - max_degrees))

        if subtract_angle:
            return Angle(degrees - influence_degrees).convert(self.mode)
        return Angle(degrees + influence_degrees).convert(self.mode)

    def to_combo_di(self):
        # Find when to DI left or right
        degrees = self.get_degrees()
        add_angle = False

        if 90 <= degrees < 270:
            add_angle = not add_angle
        if degrees > 180:
            add_angle = not add_angle

        if add_angle:
            return Angle(degrees + 90).correct_for_cardinal().convert(self.mode)
        return Angle(degrees - 90).correct_for_cardinal().convert(self.mode)

    def to_combo_di_launch(self):
        di_degrees = self.to_combo_di().get_degrees()
        degrees = self.get_degrees()
        subtract_angle = degrees < 90 or 180 <= degrees < 270

        max_degrees = degrees + 90
        if subtract_angle:
            max_degrees = degrees - 90
        influence_degrees = math.cos(math.radians(di_degrees - max_degrees))

        if subtract_angle:
            return Angle(degrees - 18 * influence_degrees).convert(self.mode)
        return Angle(degrees + 18 * influence_degrees).convert(self.mode)

    def __add__(self, other):
        if type(other) in {int, float}:
            return Angle(self.amount + other, self.mode)
        if type(other) is Angle:
            return Angle(self.amount + other.convert(self.mode).amount, self.mode)

        raise ArithmeticError

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if type(other) in {int, float}:
            return Angle(self.amount * other, self.mode)
        if type(other) is Angle:
            return Angle(self.amount * other.get_rotations(), self.mode)

        raise ArithmeticError

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        if type(other) in {int, float, Angle}:
            return self + other * -1

        raise ArithmeticError

    def __rsub__(self, other):
        return (self - other) * -1

    def __truediv__(self, other):
        if type(other) in {int, float}:
            return self * (1 / other)
        if type(other) is Angle:
            return self * (1 / other.get_rotations())

        raise ArithmeticError

    def __rtruediv__(self, other):
        if type(other) in {int, float}:
            return other / self.get_rotations()
        if type(other) is Angle:
            return other / self

        raise ArithmeticError

    def __mod__(self, other):
        if type(other) in {int, float}:
            return Angle(self.amount % other, self.mode)
        if type(other) is Angle:
            return Angle(self.amount % other.convert(self.mode).amount, self.mode)

        raise ArithmeticError

    def __rmod__(self, other):
        if type(other) in {int, float}:
            return other % self.get_rotations()
        if type(other) is Angle:
            return other % self

        raise ArithmeticError

    def __idiv__(self, other):
        if type(other) in {int, float}:
            return Angle(self.amount // other, self.mode)
        if type(other) is Angle:
            return Angle(self.amount // other.get_rotations(), self.mode)

        raise ArithmeticError

    def __gt__(self, other):
        if type(other) in {int, float}:
            return self.get_rotations() > other
        if type(other) is Angle:
            return self.amount > other.convert(self.mode).amount

        raise ArithmeticError

    def __lt__(self, other):
        if type(other) in {int, float}:
            return self.get_rotations() < other
        if type(other) is Angle:
            return self.amount < other.convert(self.mode).amount

        raise ArithmeticError

    def __ge__(self, other):
        if type(other) in {int, float}:
            return self.get_rotations() >= other
        if type(other) is Angle:
            return self.amount >= other.convert(self.mode).amount

        raise ArithmeticError
    def __le__(self, other):
        if type(other) in {int, float}:
            return self.get_rotations() <= other
        if type(other) is Angle:
            return self.amount <= other.convert(self.mode).amount

        raise ArithmeticError

    def __abs__(self):
        return Angle(abs(self.amount), self.mode)
