import math

from Utils.angle import Angle
from Utils.mathutils import MathUtils
from Utils.vector2 import Vector2


class ControlStick:
    DEAD_ZONE_ESCAPE = 39
    MAX_INPUT = 127
    NUM_EDGE_COORDINATES = 1016

    @staticmethod
    def from_edge_coordinate(n):
        return ControlStick(ControlStick.MAX_INPUT, 0).get_next_nth_counter_clockwise_input(n % ControlStick.NUM_EDGE_COORDINATES)

    @staticmethod
    def from_corrected_angle(a):
        return ControlStick.from_angle(a).correct_for_cardinal_strict()

    @staticmethod
    def from_angle(angle):
        x = angle.get_x() * ControlStick.MAX_INPUT
        y = angle.get_y() * ControlStick.MAX_INPUT
        m = min(ControlStick.MAX_INPUT / max(abs(x), 1), ControlStick.MAX_INPUT / max(abs(y), 1))
        x = round(x * m)
        y = round(y * m)

        result = ControlStick(x, y)
        if result.to_angle() < angle:
            test_result = result.get_next_counter_clockwise_input()
        else:
            test_result = result.get_next_clockwise_input()

        if abs(test_result.to_angle() - angle) < abs(result.to_angle() - angle):
            return test_result
        return result

    @staticmethod
    def normalize_x_input(p):
        return MathUtils.i_lerp((ControlStick.DEAD_ZONE_ESCAPE - 1) / ControlStick.MAX_INPUT, 1, abs(p)) * MathUtils.sign(p)

    @staticmethod
    def __get_next_clockwise_input(coords):
        x = coords.x
        y = coords.y

        if x <= 0 and y < 0:
            if abs(x) < abs(y):
                x -= 1
                if not ControlStick.__input_is_valid(x, y):
                    y += 1
            else:
                y += 1
                if ControlStick.__input_is_valid(x - 1, y):
                    x -= 1
        elif x < 0 and y >= 0:
            if abs(x) <= abs(y):
                x += 1
                if ControlStick.__input_is_valid(x, y + 1):
                    y += 1
            else:
                y += 1
                if not ControlStick.__input_is_valid(x, y):
                    x += 1
        elif x >= 0 and y <= 0:
            if abs(x) <= abs(y):
                x -= 1
                if ControlStick.__input_is_valid(x, y - 1):
                    y -= 1
            else:
                y -= 1
                if not ControlStick.__input_is_valid(x, y):
                    x -= 1
        else:
            if abs(x) < abs(y):
                x += 1
                if not ControlStick.__input_is_valid(x, y):
                    y -= 1
            else:
                y -= 1
                if ControlStick.__input_is_valid(x + 1, y):
                    x += 1

        return Vector2(x, y)

    @staticmethod
    def __get_next_counter_clockwise_input(coords):
        x = coords.x
        y = coords.y

        if x < 0 and y <= 0:
            if abs(x) <= abs(y):
                x += 1
                if ControlStick.__input_is_valid(x, y - 1):
                    y -= 1
            else:
                y -= 1
                if not ControlStick.__input_is_valid(x, y):
                    x += 1
        elif x <= 0 and y > 0:
            if abs(x) < abs(y):
                x -= 1
                if not ControlStick.__input_is_valid(x, y):
                    y -= 1
            else:
                y -= 1
                if ControlStick.__input_is_valid(x - 1, y):
                    x -= 1
        elif x >= 0 and y < 0:
            if abs(x) < abs(y):
                x += 1
                if not ControlStick.__input_is_valid(x, y):
                    y += 1
            else:
                y += 1
                if ControlStick.__input_is_valid(x + 1, y):
                    x += 1
        else:
            if abs(x) <= abs(y):
                x -= 1
                if ControlStick.__input_is_valid(x, y + 1):
                    y += 1
            else:
                y += 1
                if not ControlStick.__input_is_valid(x, y):
                    x -= 1

        return Vector2(x, y)

    @staticmethod
    def __input_is_valid(x, y):
        try:
            ControlStick.__validate_input(x, y)
            return True
        except ArithmeticError:
            return False

    @staticmethod
    def __validate_input(x, y):
        if abs(x) > ControlStick.MAX_INPUT:
            raise ArithmeticError("x value", x, "is invalid for control stick input")
        if abs(y) > ControlStick.MAX_INPUT:
            raise ArithmeticError("y value", y, "is invalid for control stick input")
        # if (x / ControlStick.MAX_INPUT) ** 2 + (y / ControlStick.MAX_INPUT) ** 2 > 1:
        #     raise ArithmeticError("x and y coordinates", x, ",", y, "are invalid for control stick input")

    @staticmethod
    def __refit_coordinate(coordinate):
        return (coordinate + ControlStick.NUM_EDGE_COORDINATES) % ControlStick.NUM_EDGE_COORDINATES

    def __init__(self, x, y):
        ControlStick.__validate_input(x, y)
        self.x = x
        self.y = y

    def get_coords(self):
        return Vector2(self.x, self.y)

    def get_next_clockwise_input(self):
        coords = ControlStick.__get_next_clockwise_input(self.get_coords())
        return ControlStick(coords.x, coords.y)

    def get_next_counter_clockwise_input(self):
        coords = ControlStick.__get_next_counter_clockwise_input(self.get_coords())
        return ControlStick(coords.x, coords.y)

    def get_next_nth_clockwise_input(self, n):
        coords = self.get_coords()

        for i in range(n):
            coords = ControlStick.__get_next_clockwise_input(coords)
        return ControlStick(coords.x, coords.y)

    def get_next_nth_counter_clockwise_input(self, n):
        coords = self.get_coords()

        for i in range(n):
            coords = ControlStick.__get_next_counter_clockwise_input(coords)
        return ControlStick(coords.x, coords.y)

    def get_most_up_y(self):
        return ControlStick.MAX_INPUT

    def get_most_down_y(self):
        return -ControlStick.MAX_INPUT

    def get_most_right_x(self):
        return ControlStick.MAX_INPUT

    def get_most_left_x(self):
        return -ControlStick.MAX_INPUT

    def to_vector(self):
        return Vector2((self.x + 1) / (ControlStick.MAX_INPUT + 1), (self.y + 1) / (ControlStick.MAX_INPUT + 1))

    def to_edge_coordinate(self):
        x = self.x
        y = self.y

        if x <= 0:
            if y <= 0:
                if abs(x) < abs(y):
                    result = ControlStick.NUM_EDGE_COORDINATES * 3 // 4 + x
                else:
                    result = ControlStick.NUM_EDGE_COORDINATES * 2 // 4 - y
            else:
                if abs(x) < abs(y):
                    result = ControlStick.NUM_EDGE_COORDINATES * 1 // 4 - x
                else:
                    result = ControlStick.NUM_EDGE_COORDINATES * 2 // 4 - y
        else:
            if y <= 0:
                if abs(x) < abs(y):
                    result = ControlStick.NUM_EDGE_COORDINATES * 3 // 4 + x
                else:
                    result = ControlStick.NUM_EDGE_COORDINATES * 0 // 4 + y
            else:
                if abs(x) < abs(y):
                    result = ControlStick.NUM_EDGE_COORDINATES * 1 // 4 - x
                else:
                    result = ControlStick.NUM_EDGE_COORDINATES * 0 // 4 + y

        result = ControlStick.__refit_coordinate(result)
        if result > ControlStick.NUM_EDGE_COORDINATES // 2:
            return result - ControlStick.NUM_EDGE_COORDINATES
        return result

    def to_angle(self):
        return Angle(math.atan2(self.y, self.x), Angle.Mode.RADIANS)

    def correct_for_cardinal(self):
        # Correct angle based on the cardinal dead-zones
        coordinate = self.to_edge_coordinate()
        near_escape = ControlStick.DEAD_ZONE_ESCAPE - 1
        half_escape = ControlStick.DEAD_ZONE_ESCAPE / 2
        quarter_num_edge = ControlStick.NUM_EDGE_COORDINATES / 4

        non_cardinal_angle = (coordinate + near_escape) % quarter_num_edge - near_escape
        result = coordinate

        if -near_escape <= non_cardinal_angle < -half_escape:
            result = coordinate - non_cardinal_angle - ControlStick.DEAD_ZONE_ESCAPE
        if -half_escape <= non_cardinal_angle <= half_escape:
            result = coordinate - non_cardinal_angle
        if half_escape < non_cardinal_angle <= near_escape:
            result = coordinate - non_cardinal_angle + ControlStick.DEAD_ZONE_ESCAPE
        return ControlStick.from_edge_coordinate(result)

    def correct_for_cardinal_strict(self):
        # Correct angle based on the cardinal dead-zones, only going to cardinal if exactly at the right angle
        coordinate = self.to_edge_coordinate()
        near_escape = ControlStick.DEAD_ZONE_ESCAPE - 1
        quarter_num_edge = ControlStick.NUM_EDGE_COORDINATES // 4

        non_cardinal_angle = (coordinate + near_escape) % quarter_num_edge - near_escape
        result = coordinate

        if -near_escape <= non_cardinal_angle < 0:
            result = coordinate - non_cardinal_angle - ControlStick.DEAD_ZONE_ESCAPE
        elif 0 < non_cardinal_angle <= near_escape:
            result = coordinate - non_cardinal_angle + ControlStick.DEAD_ZONE_ESCAPE
        return ControlStick.from_edge_coordinate(result)