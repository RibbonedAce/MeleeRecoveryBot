from abc import ABCMeta
from collections import defaultdict

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import Angle, ControlStick, FrameInput, HillClimb, LogUtils, RecoveryTarget, Trajectory, Vector2
from Utils.enums import FADE_BACK_MODE


class FireAnimal(RecoveryChain, metaclass=ABCMeta):
    ANGLES_TO_TEST = (ControlStick.from_angle(Angle(90)).to_edge_coordinate(),
                      ControlStick(ControlStick.DEAD_ZONE_ESCAPE, ControlStick(ControlStick.DEAD_ZONE_ESCAPE, 0).get_most_up_y()).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(45)).to_edge_coordinate(),
                      ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(90)).to_edge_coordinate(),
                      ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), -ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(-45)).to_edge_coordinate(),
                      ControlStick(ControlStick.DEAD_ZONE_ESCAPE, ControlStick(ControlStick.DEAD_ZONE_ESCAPE, 0).get_most_down_y()).to_edge_coordinate(),
                      ControlStick.from_angle(Angle(-90)).to_edge_coordinate())

    @classmethod
    def create_default_inputs(cls, smashbot_state, game_state):
        input_frames = defaultdict(lambda: FrameInput.forward())
        position = smashbot_state.get_relative_position()
        vector = Vector2.from_angle(Vector2(position.x - game_state.get_stage_edge(), -position.y).to_angle().correct_for_cardinal_strict())
        for i in range(42, cls._get_launch_end_frame()):
            input_frames[i] = FrameInput.direct(vector)
        return input_frames

    @classmethod
    def _get_launch_end_frame(cls) -> int: ...

    def __init__(self, target=(0, 0), recovery_target=RecoveryTarget.max()):
        RecoveryChain.__init__(self, target, recovery_target)
        self.min_angle = self.__determine_initial_min_angle()
        self.max_angle = ControlStick.from_angle(Angle(90)).to_edge_coordinate()
        self.best_angle = ControlStick.from_angle(Angle(0)).to_edge_coordinate()
        self.best_distance = None
        self.hill_climb = None

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, Vector2(0, 1))

        self._increment_current_frame(smashbot_state)

        # Calculating and applying angle
        if 0 < self.current_frame <= 40:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                self.trajectory = self.create_trajectory(smashbot_state.character)

                # If going for ledge and facing backwards, do not go straight up or down
                if self.recovery_target.ledge and not smashbot_state.is_facing_inwards():
                    self.max_angle = min(self.max_angle, ControlStick.from_angle(Angle(90)).to_edge_coordinate() - 1)
                    self.min_angle = max(self.min_angle, ControlStick.from_angle(Angle(-90)).to_edge_coordinate() + 1)

                self.hill_climb = HillClimb(self.min_angle, self.max_angle, 40)

            next_point = round(self.hill_climb.get_next_point())
            if self.current_frame <= 9 and self.min_angle <= self.ANGLES_TO_TEST[self.current_frame - 1] <= self.max_angle:
                next_point = self.ANGLES_TO_TEST[self.current_frame - 1]
            current_angle = ControlStick.from_edge_coordinate(next_point).correct_for_cardinal_strict().to_edge_coordinate()
            LogUtils.simple_log(current_angle, self.best_angle)

            # Test current angle in trial
            self.trajectory = self.create_trajectory(smashbot_state.character)

            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(propagate, target=self.target, frame_range=range(self.current_frame, 600), input_frames=self.__generate_angled_input_frames(current_angle))
            else:
                recovery_distance = self.trajectory.get_distance(propagate, target=self.target, ledge=self.recovery_target.ledge, frame_range=range(self.current_frame, 600), input_frames=self.__generate_angled_input_frames(current_angle))

            # Record angle for hill-climbing
            extra_distance = recovery_distance - (abs(smashbot_state.position.x) - self.target.x)
            LogUtils.simple_log(extra_distance)

            if recovery_distance != Trajectory.TOO_LOW_RESULT:
                # Converge towards minimum distance required, favoring negative angles
                if self.recovery_target.is_sweet_spot():
                    if current_angle <= 0:
                        self.hill_climb.record_custom_result(-abs(extra_distance), current_angle)
                        if (self.best_distance is None or extra_distance < self.best_distance) and extra_distance > 0:
                            self.__update_best_angle(current_angle, extra_distance)
                            if self.hill_climb.best_point > 0:
                                self.hill_climb.override_best_result(-abs(extra_distance), current_angle)
                    elif self.best_angle >= 0:
                        self.hill_climb.record_custom_result(extra_distance, current_angle)
                        if self.best_distance is None or current_angle < self.best_angle:
                            self.__update_best_angle(current_angle, extra_distance)

                # Converge towards minimum distance required
                elif self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
                    self.hill_climb.record_custom_result(-abs(extra_distance), current_angle)
                    if (self.best_distance is None or extra_distance < self.best_distance) and extra_distance > 0:
                        self.__update_best_angle(current_angle, extra_distance)

                # Converge towards maximum distance
                else:
                    self.hill_climb.record_custom_result(extra_distance, current_angle)
                    if self.best_distance is None or extra_distance > self.best_distance:
                        self.__update_best_angle(current_angle, extra_distance)

        # Tilt stick in best angle on last frame
        elif self.current_frame == 41:
            if self.best_distance is None:
                self.best_angle = ControlStick.from_edge_coordinate(round(self.hill_climb.get_next_point())).correct_for_cardinal_strict().to_edge_coordinate()

            s_input = ControlStick.from_edge_coordinate(self.best_angle).to_vector()
            LogUtils.simple_log(s_input)
            self.controller.tilt_analog_unit(Button.BUTTON_MAIN, smashbot_state.get_inward_x() * s_input.x, s_input.y)

        elif self.current_frame >= 42:
            self._perform_fade_back(propagate)

        LogUtils.simple_log("frame number:", self.current_frame, smashbot_state.action_frame)
        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FIREFOX_AIR, Action.FIREFOX_WAIT_AIR, Action.SWORD_DANCE_1_AIR, Action.DEAD_FALL}

    def __generate_angled_input_frames(self, angle):
        input_frames = self._generate_input_frames()
        vector = ControlStick.from_edge_coordinate(angle).to_vector()
        for i in range(42, self._get_launch_end_frame()):
            input_frames[i] = FrameInput.direct(vector)
        return input_frames

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle

    def __determine_initial_min_angle(self):
        if self.recovery_target.is_sweet_spot():
            return ControlStick.from_angle(Angle(-90)).to_edge_coordinate()
        return ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate()