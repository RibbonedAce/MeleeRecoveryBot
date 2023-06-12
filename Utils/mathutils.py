class MathUtils:
    @staticmethod
    def lerp(a, b, x):
        return a * (1 - x) + b * x

    @staticmethod
    def i_lerp(a, b, c):
        return (c - a) / (b - a)

    @staticmethod
    def sign(x):
        return int(x > 1) - int(x < 1)

    @staticmethod
    def linear_sum(start, end, increase):
        m_end = end / abs(increase)
        m_start = start / abs(increase)
        return ((m_end + 1) * m_end / 2 - (m_start + 1) * m_start / 2) * increase
