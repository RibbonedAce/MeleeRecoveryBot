class MathUtils:
    @staticmethod
    def lerp(a, b, x):
        return a * (1 - x) + b * x

    @staticmethod
    def i_lerp(a, b, c):
        return (c - a) / (b - a)

    @staticmethod
    def sign(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        return 0
