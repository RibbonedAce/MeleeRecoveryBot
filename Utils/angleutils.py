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