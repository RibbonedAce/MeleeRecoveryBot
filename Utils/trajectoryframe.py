from melee import FrameData

from Utils import Angle
from Utils.controlstick import ControlStick
from Utils.mathutils import MathUtils
from Utils.vector2 import Vector2


class TrajectoryFrame:
    @staticmethod
    def default_horizontal(velocity, s_input, forward, backward, max_v, mid_v, min_v):
        normalized_input = ControlStick.normalize_x_input(s_input)
        if normalized_input == 0 and mid_v is not None:
            return mid_v

        acceleration = MathUtils.lerp(backward, forward, (normalized_input + 1) / 2)
        return max(min_v, min(velocity + acceleration, max_v))

    @staticmethod
    def reduce_singular(velocity, amount, end=0):
        return MathUtils.sign(velocity - end) * max(abs(velocity - end) - amount, end) + end

    @staticmethod
    def curved(velocity, angle, curve_back=False):
        frame_degrees = (velocity.to_angle() + angle).get_degrees()
        if frame_degrees > 90 and curve_back:
            frame_degrees = 180 - frame_degrees

        return velocity.from_angle(Angle(frame_degrees), velocity.get_magnitude())

    @staticmethod
    def drift(character, ecb=Vector2(2, 0)):
        gravity = FrameData.INSTANCE.get_gravity(character)
        terminal_velocity = FrameData.INSTANCE.get_terminal_velocity(character)
        air_speed = FrameData.INSTANCE.get_air_speed(character)

        return TrajectoryFrame.drift_manual(character, gravity, terminal_velocity, air_speed, ecb)

    @staticmethod
    def drift_manual(character, gravity, terminal_velocity, air_speed, ecb=Vector2(2, 0)):
        mobility = FrameData.INSTANCE.get_air_mobility(character)
        drag = FrameData.INSTANCE.get_air_friction(character)
        fast_fall_speed = FrameData.INSTANCE.get_fast_fall_speed(character)

        def horizontal_formula(velocity, s_input):
            normalized_input = ControlStick.normalize_x_input(s_input)
            normalized_drag = min(abs(velocity), drag) * -MathUtils.sign(velocity)
            normalized_speed = air_speed * s_input
            normalized_mobility = MathUtils.lerp(mobility / 2, mobility, abs(normalized_input)) * MathUtils.sign(normalized_input)

            if normalized_input > 0 and velocity > normalized_speed:
                new_velocity = max(velocity + normalized_drag, normalized_speed)
            elif normalized_input > 0 and velocity <= normalized_speed:
                new_velocity = min(velocity + normalized_mobility, normalized_speed)
            elif normalized_input < 0 and velocity < normalized_speed:
                new_velocity = min(velocity + normalized_drag, normalized_speed)
            elif normalized_input < 0 and velocity >= normalized_speed:
                new_velocity = max(velocity + normalized_mobility, normalized_speed)
            else:
                new_velocity = velocity + normalized_drag

            return new_velocity

        def vertical_formula(velocity, s_input):
            if s_input < -0.5 and velocity <= 0:
                return -fast_fall_speed
            if velocity <= -terminal_velocity:
                return velocity
            return max(velocity - gravity, -terminal_velocity)

        return TrajectoryFrame(lambda v, i: Vector2(horizontal_formula(v.x, i.x), vertical_formula(v.y, i.y)), ecb)

    @staticmethod
    def reduce(amount, ecb=Vector2(2, 0)):
        return TrajectoryFrame(lambda v, i: v.with_magnitude(max(v.get_magnitude() - amount, 0)), ecb)

    @staticmethod
    def multiply(multiplier, ecb=Vector2(2, 0)):
        return TrajectoryFrame(lambda v, i: v.with_magnitude(v.get_magnitude() * multiplier), ecb)

    @staticmethod
    def fixed(velocity, ecb):
        return TrajectoryFrame(lambda v, i: velocity, ecb)

    @staticmethod
    def angle(magnitude, ecb=Vector2(2, 0)):
        return TrajectoryFrame(lambda v, i: i.with_magnitude(magnitude), ecb)

    @staticmethod
    def repeat():
        return TrajectoryFrame(lambda v, i: v)

    def __init__(self, velocity, ecb=Vector2(2, 0)):
        self.velocity = velocity
        self.ecb = ecb

    def copy(self):
        return TrajectoryFrame(self.velocity, self.ecb)

    def __str__(self):
        return "TrajectoryFrame(vel={}, ecb={})".format(self.velocity, self.ecb)