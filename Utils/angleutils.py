import math


class AngleUtils:
    """
    Keeps angles between 0 and 360
    """

    @staticmethod
    def refit_angle(angle):
        return (angle + 360) % 360

    @staticmethod
    def get_other_quadrant_end(angle):
        return AngleUtils.refit_angle(90 - angle + 180 * (angle // 90))

    @staticmethod
    def get_x_reflection(angle):
        return AngleUtils.refit_angle(180 - angle)

    @staticmethod
    def get_y_reflection(angle):
        return AngleUtils.refit_angle(360 - angle)

    @staticmethod
    def angle_to_xy(angle):
        radians = math.radians(angle)
        return (math.cos(radians) + 1) / 2, (math.sin(radians) + 1) / 2

    @staticmethod
    def correct_for_cardinal(angle):
        # Correct angle based on the cardinal dead-zones
        non_cardinal_angle = (angle + 17) % 90 - 17
        if -17 <= non_cardinal_angle < -8:
            return angle - non_cardinal_angle - 18
        if -8 <= non_cardinal_angle <= 8:
            return angle - non_cardinal_angle
        if 8 < non_cardinal_angle <= 17:
            return angle - non_cardinal_angle + 18
        return angle

    @staticmethod
    def correct_for_cardinal_strict(angle):
        # Correct angle based on the cardinal dead-zones, only going to cardinal if exactly at the right angle
        non_cardinal_angle = (angle + 17) % 90 - 17
        if -17 <= non_cardinal_angle < 0:
            return angle - non_cardinal_angle - 18
        if non_cardinal_angle == 0:
            return angle - non_cardinal_angle
        if 0 < non_cardinal_angle <= 17:
            return angle - non_cardinal_angle + 18
        return angle

    @staticmethod
    def get_survival_di(angle, position):
        # Find when to DI left or right
        add_angle = True
        if angle > 180:
            add_angle = position < 0
        else:
            if 90 <= angle <= 180:
                add_angle = not add_angle
            if 73 <= angle <= 107:
                add_angle = not add_angle

        result = AngleUtils.refit_angle(angle - 90)
        if add_angle:
            result = AngleUtils.refit_angle(angle + 90)

        return AngleUtils.correct_for_cardinal(result)

    @staticmethod
    def get_combo_di(angle):
        # Find when to DI left or right
        add_angle = False
        if 90 <= angle < 270:
            add_angle = not add_angle
        if angle > 180:
            add_angle = not add_angle

        result = AngleUtils.refit_angle(angle - 90)
        if add_angle:
            result = AngleUtils.refit_angle(angle + 90)

        return AngleUtils.correct_for_cardinal(result)

    @staticmethod
    def get_survival_di_launch_angle(angle, position):
        di_angle = AngleUtils.get_survival_di(angle, position)
        subtract_angle = 90 <= angle < 180 or angle >= 270

        max_angle = angle + 90
        if subtract_angle:
            max_angle = angle - 90
        influence = math.cos(math.radians(di_angle - max_angle))

        result = angle + 18 * influence
        if subtract_angle:
            result = angle - 18 * influence
        return result

    @staticmethod
    def get_combo_di_launch_angle(angle):
        di_angle = AngleUtils.get_combo_di(angle)
        subtract_angle = angle < 90 or 180 <= angle < 270

        max_angle = angle + 90
        if subtract_angle:
            max_angle = angle - 90
        influence = math.cos(math.radians(di_angle - max_angle))

        result = angle + 18 * influence
        if subtract_angle:
            result = angle - 18 * influence
        return result