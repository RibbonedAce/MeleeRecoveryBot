class TrajectoryFrame:
    def __init__(self,
                 vertical_velocity,
                 forward_acceleration,
                 backward_acceleration,
                 max_horizontal_velocity,
                 mid_horizontal_velocity,
                 min_horizontal_velocity,
                 ecb_bottom):
        self.vertical_velocity = vertical_velocity
        self.forward_acceleration = forward_acceleration
        self.backward_acceleration = backward_acceleration
        self.max_horizontal_velocity = max_horizontal_velocity
        self.mid_horizontal_velocity = mid_horizontal_velocity
        self.min_horizontal_velocity = min_horizontal_velocity
        self.ecb_bottom = ecb_bottom