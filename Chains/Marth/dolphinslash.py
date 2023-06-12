from collections import defaultdict

from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import Angle, ControlStick, FrameInput, LogUtils, MathUtils, RecoveryTarget, Trajectory, Vector2
from Utils.enums import FADE_BACK_MODE


class DolphinSlash(RecoveryChain):
    @classmethod
    def __curve_angle(cls, s_input):
        return Angle(MathUtils.i_lerp(0.5, 1, abs(s_input.x)) * MathUtils.sign(s_input.x) * -20)

    TRAJECTORY = Trajectory(Character.MARTH, "DolphinSlash")

    ANGLES_TO_TEST = (ControlStick.from_angle(Angle(0)).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(90)).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(135)).to_edge_coordinate())

    @classmethod
    def create_trajectory(cls, character):
        return cls.TRAJECTORY

    @classmethod
    def create_default_inputs(cls, smashbot_state, game_state):
        inputs = defaultdict(FrameInput.forward)
        for i in range(5, 22):
            inputs[i] = FrameInput.direct(Vector2(1, 0))
        return inputs

    def __init__(self, target=Vector2.zero(), recovery_target=RecoveryTarget.max()):
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
            input_frames = self.__generate_angled_input_frames(current_angle)

            # Test current angle in trial
            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(propagate, target=self.target, frame_range=range(self.current_frame, 600), input_frames=input_frames)
            else:
                recovery_distance = self.trajectory.get_distance(propagate, target=self.target, ledge=self.recovery_target.ledge, frame_range=range(self.current_frame, 600), input_frames=input_frames)

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
                self.best_angle = ControlStick.from_angle(Angle(90)).correct_for_cardinal_strict().to_edge_coordinate()

            s_input = ControlStick.from_edge_coordinate(self.best_angle).to_vector()
            LogUtils.simple_log(s_input)
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x * s_input.x, s_input.y)

        # Tilt stick towards stage to make sure we always face forward
        elif self.current_frame == 5:
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x, 0)

        # Holding the angle
        elif 5 < self.current_frame <= 21:
            s_input = ControlStick.from_edge_coordinate(self.best_angle).to_vector()
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, inward_x * s_input.x, s_input.y)

        # Deciding if we should fade-back
        elif self.current_frame > 21:
            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.SHINE_RELEASE_AIR, Action.DEAD_FALL}

    def __generate_angled_input_frames(self, angle):
        input_frames = defaultdict(FrameInput.forward)
        vector = Vector2.from_angle(ControlStick.from_edge_coordinate(angle).to_angle())
        for i in range(5, 22):
            input_frames[i] = FrameInput.direct(vector)
        return input_frames

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle