from numpy import copy


class Utils:
    LEDGE_GRAB_AREA = (12, 19)
    LEDGE_GRAB_AREA_HIGH = (12, 12)

    @staticmethod
    def lerp(a, b, x):
        return a * (1 - x) + b * x

    @staticmethod
    def i_lerp(a, b, c):
        return (c - a) / (b - a)

    @staticmethod
    def location(a, b, c):
        if c < a and c < b:
            return 0
        if c > a and c > b:
            return 1

        ma = max(a, b)
        mi = min(a, b)
        return Utils.i_lerp(mi, ma, c)

    @staticmethod
    def transform_array(array, l, params):
        result = copy(array)
        for i in range(0, len(result.flat), params):
            result.flat[i: i + params] = l(result.flat[i: i + params])
        return result[:, 0: int(array.shape[1] / params)]

    @staticmethod
    def sign(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        return 0
