class TrajectoryFrame:
    def __init__(self,
                 vertical_velocity=0,
                 forward_acceleration=0,
                 backward_acceleration=0,
                 max_horizontal_velocity=0,
                 mid_horizontal_velocity=None,
                 min_horizontal_velocity=0,
                 ecb_bottom=0,
                 ecb_inward=2):
        self.vertical_velocity = vertical_velocity
        self.forward_acceleration = forward_acceleration
        self.backward_acceleration = backward_acceleration
        self.max_horizontal_velocity = max_horizontal_velocity
        self.mid_horizontal_velocity = mid_horizontal_velocity
        self.min_horizontal_velocity = min_horizontal_velocity
        self.ecb_bottom = ecb_bottom
        self.ecb_inward = ecb_inward

    def copy(self):
        return TrajectoryFrame(
            self.vertical_velocity,
            self.forward_acceleration,
            self.backward_acceleration,
            self.max_horizontal_velocity,
            self.mid_horizontal_velocity,
            self.min_horizontal_velocity,
            self.ecb_bottom,
            self.ecb_inward
        )

    def __str__(self):
        return "TrajectoryFrame(vert={}, acl_f={}, acl_b={}, max_h={}, mid_h={}, min_h={}, ecb_b={}, ecb_i={})".format(
            self.vertical_velocity,
            self.forward_acceleration,
            self.backward_acceleration,
            self.max_horizontal_velocity,
            self.mid_horizontal_velocity,
            self.min_horizontal_velocity,
            self.ecb_bottom,
            self.ecb_inward)
