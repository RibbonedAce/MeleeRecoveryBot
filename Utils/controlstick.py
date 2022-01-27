import math

from Utils.angleutils import AngleUtils
from Utils.mathutils import MathUtils


class ControlStick:
    DEAD_ZONE_ESCAPE = 39
    MAX_INPUT = 127
    NUM_EDGE_COORDINATES = 1016

    def __init__(self, x, y):
        ControlStick.__validate_input(x, y)
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coords(self):
        return self.__x, self.__y

    def set_x(self, x):
        ControlStick.__validate_input(x, self.__y)
        self.__x = x

    def set_y(self, y):
        ControlStick.__validate_input(self.__x, y)
        self.__y = y

    def get_next_clockwise_input(self):
        x, y = ControlStick.__get_next_clockwise_input(self.__x, self.__y)
        return ControlStick(x, y)

    def get_next_counter_clockwise_input(self):
        x, y = ControlStick.__get_next_counter_clockwise_input(self.__x, self.__y)
        return ControlStick(x, y)

    def get_next_nth_clockwise_input(self, n):
        x, y = self.get_coords()

        for i in range(n):
            x, y = ControlStick.__get_next_clockwise_input(x, y)
        return ControlStick(x, y)

    def get_next_nth_counter_clockwise_input(self, n):
        x, y = self.get_coords()

        for i in range(n):
            x, y = ControlStick.__get_next_counter_clockwise_input(x, y)
        return ControlStick(x, y)

    def get_most_up_y(self):
        return ControlStick.MAX_INPUT

    def get_most_down_y(self):
        return -ControlStick.MAX_INPUT

    def get_most_right_x(self):
        return ControlStick.MAX_INPUT

    def get_most_left_x(self):
        return -ControlStick.MAX_INPUT

    def to_smashbot_xy(self):
        return ((self.__x + 1) / (ControlStick.MAX_INPUT + 1) + 1) / 2, ((self.__y + 1) / (ControlStick.MAX_INPUT + 1) + 1) / 2

    def to_edge_coordinate(self, negative=False):
        x, y = self.get_coords()

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

        if negative:
            return ControlStick.__negate_coordinate(result)
        return ControlStick.__refit_coordinate(result)

    def to_angle(self):
        return AngleUtils.refit_angle(math.degrees(math.atan2(self.__y, self.__x)))

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
        elif non_cardinal_angle == 0:
            result = coordinate - non_cardinal_angle
        elif 0 < non_cardinal_angle <= near_escape:
            result = coordinate - non_cardinal_angle + ControlStick.DEAD_ZONE_ESCAPE
        return ControlStick.from_edge_coordinate(result)

    @staticmethod
    def from_edge_coordinate(n):
        return ControlStick(ControlStick.MAX_INPUT, 0).get_next_nth_counter_clockwise_input(n % ControlStick.NUM_EDGE_COORDINATES)

    @staticmethod
    def from_corrected_angle(a):
        return ControlStick.from_angle(a).correct_for_cardinal_strict()

    @staticmethod
    def from_angle(a):
        x = round(math.acos(math.radians(a)) * ControlStick.MAX_INPUT)
        y = round(math.asin(math.radians(a)) * ControlStick.MAX_INPUT)

        if not ControlStick.__input_is_valid(x, y):
            if abs(x) > abs(y):
                x -= MathUtils.sign(x)
            else:
                y -= MathUtils.sign(y)

        result = ControlStick(x, y)
        if result.to_angle() < a:
            test_result = result.get_next_counter_clockwise_input()
        else:
            test_result = result.get_next_clockwise_input()

        if abs(test_result.to_angle() - a) < abs(result.to_angle() - a):
            return test_result
        return result

    @staticmethod
    def coordinate_num_to_angle(n):
        return ControlStick.from_edge_coordinate(n).to_angle()

    @staticmethod
    def __get_next_clockwise_input(x, y):
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

        return x, y

    @staticmethod
    def __get_next_counter_clockwise_input(x, y):
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

        return x, y

    @staticmethod
    def __calculate_complement(y):
        return math.floor((1 - (y / ControlStick.MAX_INPUT) ** 2) ** 0.5 * ControlStick.MAX_INPUT)

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

    @staticmethod
    def __negate_coordinate(coordinate):
        fit_coordinate = ControlStick.__refit_coordinate(coordinate)
        if fit_coordinate > ControlStick.NUM_EDGE_COORDINATES // 2:
            return fit_coordinate - ControlStick.NUM_EDGE_COORDINATES
        return fit_coordinate
