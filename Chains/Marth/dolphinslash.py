from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import Angle, ControlStick, FrameInput, LogUtils, MathUtils, Trajectory, TrajectoryFrame as TF, Vector2, Vector2 as V2
from Utils.enums import FADE_BACK_MODE, LEDGE_GRAB_MODE


class DolphinSlash(RecoveryChain):
    @staticmethod
    def __curve_angle(s_input):
        return Angle(MathUtils.i_lerp(0.5, 1, abs(s_input.x)) * MathUtils.sign(s_input.x) * -20)

    TRAJECTORY = Trajectory(Character.MARTH, 5, 20, LEDGE_GRAB_MODE.ALWAYS, False, [
        TF(lambda v, i: V2(TF.reduce_singular(0.666 * v.x, 0.05), -0.085), V2(2.55763, 2.79079)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.17), V2(3.89811, 3.36551)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.255), V2(3.78597, 3.35083)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.34), V2(2.85201, 1.84816)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.425), V2(2.86545, 2.05758)),
        TF(lambda v, i: TF.curved(V2(0.75685, 14.41555), Angle.from_input(i, 0.5, 20), True), V2(2, 2.05758)),
        TF(lambda v, i: TF.curved(V2(0.7145, 15.51062), Angle.from_input(i, 0.5, 20), True), V2(2, 2.05758)),
        TF(lambda v, i: TF.curved(V2(0.67334, 8.65633), Angle.from_input(i, 0.5, 20), True), V2(2, 2.05758)),
        TF(lambda v, i: TF.curved(V2(0.63338, 2.42162), Angle.from_input(i, 0.5, 20), True), V2(2, 2.05758)),
        TF(lambda v, i: TF.curved(V2(0.59462, 2.11897), Angle.from_input(i, 0.5, 20), True), V2(2, 5.60402)),
        TF(lambda v, i: TF.curved(V2(0.55706, 1.83569), Angle.from_input(i, 0.5, 20), True), V2(2, 5.61585)),
        TF(lambda v, i: TF.curved(V2(0.52069, 1.57181), Angle.from_input(i, 0.5, 20), True), V2(2, 5.60775)),
        TF(lambda v, i: TF.curved(V2(0.48552, 1.32731), Angle.from_input(i, 0.5, 20), True), V2(2, 5.48077)),
        TF(lambda v, i: TF.curved(V2(0.45155, 1.10218), Angle.from_input(i, 0.5, 20), True), V2(2, 5.43769)),
        TF(lambda v, i: TF.curved(V2(0.41878, 0.89645), Angle.from_input(i, 0.5, 20), True), V2(2, 5.49179)),
        TF(lambda v, i: TF.curved(V2(0.3872, 0.7101), Angle.from_input(i, 0.5, 20), True), V2(2, 5.58387)),
        TF(lambda v, i: TF.curved(V2(0.35682, 0.54314), Angle.from_input(i, 0.5, 20), True), V2(2, 5.69573)),
        TF(lambda v, i: TF.curved(V2(0.32765, 0.39556), Angle.from_input(i, 0.5, 20), True), V2(2, 5.81503)),
        TF(lambda v, i: TF.curved(V2(0.29966, 0.26735), Angle.from_input(i, 0.5, 20), True), V2(2, 5.93166)),
        TF(lambda v, i: TF.curved(V2(0.27288, 0.15855), Angle.from_input(i, 0.5, 20), True), V2(2, 6.03653)),
        TF(lambda v, i: TF.curved(V2(0.24729, 0.06912), Angle.from_input(i, 0.5, 20), True), V2(2.01507, 6.13357)),
        TF(lambda v, i: TF.curved(V2(0.2229, -0.00093), Angle.from_input(i, 0.5, 20), True), V2(2.17595, 6.23814)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.14967, 6.3618)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2, 6.7316)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2, 7.18624)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.26172, 7.67057)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.12479, 7.94352)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.14861, 8.10809)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.15951, 7.89794)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.0051, 7.6036)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.16192, 7.14771)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.18233, 7.16368)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.02592, 7.07705)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2, 6.94927)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2, 6.83761)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.06701, 5.88492)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.0629, 4.81172)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.08376, 3.90223)),
        TF.drift_manual(Character.MARTH, 0.06, 2.5, 0.36, V2(2.08591, 3.3174)),
        TF.drift_manual(Character.MARTH, 0.085, 2.5, 0.36)
    ])

    ANGLES_TO_TEST = (ControlStick.from_angle(Angle(0)).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(90)).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(135)).to_edge_coordinate())

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY

    def __init__(self, target, recovery_target):
        RecoveryChain.__init__(self, target, recovery_target)
        self.best_angle = ControlStick.from_angle(Angle(0)).to_edge_coordinate()
        self.best_distance = None

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, Vector2(0, 1))

        inward_x = smashbot_state.get_inward_x()
        self._increment_current_frame(smashbot_state)

        # Calculating and applying angle
        if 0 < self.current_frame <= 3:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)
                self.trajectory = self.create_trajectory(smashbot_state.character)

            next_point = self.ANGLES_TO_TEST[min(self.current_frame - 1, len(self.ANGLES_TO_TEST) - 1)]
            current_angle = ControlStick.from_edge_coordinate(next_point).correct_for_cardinal_strict().to_edge_coordinate()

            # Test current angle in trial
            self.trajectory = self.create_trajectory(smashbot_state.character)

            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(propagate, target=self.target, frame_range=range(self.current_frame, 600), input_frames=self.__generate_angled_input_frames(current_angle))
            else:
                recovery_distance = self.trajectory.get_distance(propagate, target=self.target, ledge=self.recovery_target.ledge, frame_range=range(self.current_frame, 600), input_frames=self.__generate_angled_input_frames(current_angle))

            # Record angle
            extra_distance = recovery_distance - (abs(smashbot_state.position.x) - self.target.x)
            LogUtils.simple_log(extra_distance)

            if recovery_distance != Trajectory.TOO_LOW_RESULT:
                # Converge towards minimum distance required
                if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
                    if (self.best_distance is None or extra_distance < self.best_distance) and extra_distance > 0:
                        self.__update_best_angle(current_angle, extra_distance)

                # Converge towards maximum distance
                else:
                    if self.best_distance is None or extra_distance > self.best_distance:
                        self.__update_best_angle(current_angle, extra_distance)

        # Tilt stick in best angle on last frame
        elif self.current_frame == 4:
            self.trajectory = self.create_trajectory(smashbot_state.character)

            if self.best_distance is None:
                self.best_angle = ControlStick.from_edge_coordinate(90).correct_for_cardinal_strict().to_edge_coordinate()

            x_input = ControlStick.from_edge_coordinate(self.best_angle).to_vector().x
            LogUtils.simple_log(x_input)
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x * x_input, 0)

        # Tilt stick towards stage to make sure we always face forward
        elif self.current_frame == 5:
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x, 0)

        # Deciding if we should fade-back
        elif self.current_frame >= 6:
            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.SHINE_RELEASE_AIR, Action.DEAD_FALL}

    def __generate_angled_input_frames(self, angle):
        input_frames = self._generate_input_frames()
        vector = ControlStick.from_edge_coordinate(angle).to_vector()
        for i in range(5, 22):
            input_frames[i] = FrameInput.direct(vector)
        return input_frames

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle