import math
from abc import ABCMeta

from melee import FrameData
from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import AngleUtils, ControlStick, HillClimb, LogUtils, MathUtils, RecoveryTarget, Trajectory
from Utils.enums import FADE_BACK_MODE


class FireAnimal(RecoveryChain, metaclass=ABCMeta):
    ANGLES_TO_TEST = (ControlStick.from_angle(90).to_edge_coordinate(True),
                      ControlStick(ControlStick.DEAD_ZONE_ESCAPE, ControlStick(ControlStick.DEAD_ZONE_ESCAPE, 0).get_most_up_y()).to_edge_coordinate(True),
                      ControlStick.from_angle(45).to_edge_coordinate(True),
                      ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(True),
                      ControlStick.from_angle(0).to_edge_coordinate(True),
                      ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), -ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(True),
                      ControlStick.from_angle(-45).to_edge_coordinate(True),
                      ControlStick(ControlStick.DEAD_ZONE_ESCAPE, ControlStick(ControlStick.DEAD_ZONE_ESCAPE, 0).get_most_down_y()).to_edge_coordinate(True),
                      ControlStick.from_angle(-90).to_edge_coordinate(True))

    @classmethod
    def _get_fire_travel_deceleration(cls) -> float: ...

    @classmethod
    def _get_fire_travel_deceleration_start_frame(cls) -> int: ...

    @classmethod
    def _get_fire_travel_start_speed(cls) -> float: ...

    @classmethod
    def _get_fire_travel_end_frame(cls) -> int: ...

    @classmethod
    def _adjust_trajectory(cls, trajectory, smashbot_state, x_velocity, angle):
        x_velocity = MathUtils.sign(x_velocity) * max(0.8 * abs(x_velocity) - 0.02, 0)

        for i in range(42):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = MathUtils.sign(x_velocity) * max(abs(x_velocity) - 0.02, 0)

        x_angle = math.cos(math.radians(angle))
        y_angle = math.sin(math.radians(angle))
        magnitude = cls._get_fire_travel_start_speed()
        travel_end_frame = cls._get_fire_travel_end_frame()

        for i in range(42, travel_end_frame):
            trajectory.frames[i].vertical_velocity = y_angle * magnitude
            trajectory.frames[i].min_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].max_horizontal_velocity = x_angle * magnitude
            trajectory.frames[i].forward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].max_horizontal_velocity
            trajectory.frames[i].backward_acceleration = x_angle * magnitude - trajectory.frames[i - 1].min_horizontal_velocity

            if i > cls._get_fire_travel_deceleration_start_frame():
                magnitude = max(magnitude - cls._get_fire_travel_deceleration(), 0)

        gravity = FrameData.INSTANCE.get_gravity(smashbot_state.character)
        terminal_velocity = FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character)
        for i in range(travel_end_frame, travel_end_frame + 20):
            trajectory.frames[i].vertical_velocity = max(trajectory.frames[i - 1].vertical_velocity - gravity, -terminal_velocity)

        trajectory.frames += Trajectory.create_trajectory_frames(smashbot_state.character, trajectory.frames[travel_end_frame + 19].vertical_velocity)
        return trajectory

    def __init__(self, target_coords=(0, 0), recovery_target=RecoveryTarget.max()):
        RecoveryChain.__init__(self, target_coords, recovery_target)
        self.min_angle = self.__determine_initial_min_angle()
        self.max_angle = ControlStick.from_angle(90).to_edge_coordinate(True)
        self.best_angle = ControlStick.from_angle(0).to_edge_coordinate(True)
        self.best_distance = None
        self.start_x_velocity = 0
        self.hill_climb = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        inward_x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, (0.5, 1))

        self._increment_current_frame(smashbot_state)
        knockback_angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(knockback_angle)) > 0:
            knockback_angle = AngleUtils.get_x_reflection(knockback_angle)
        knockback_magnitude = smashbot_state.get_knockback_magnitude(opponent_state)
        inward_x_velocity = smashbot_state.get_inward_x_velocity()

        # Calculating and applying angle
        if 0 < self.current_frame <= 40:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                self.trajectory = self.create_trajectory(game_state, smashbot_state, inward_x_velocity, ControlStick.coordinate_num_to_angle(self.min_angle))
                self.start_x_velocity = inward_x_velocity

                # If going for ledge and facing backwards, do not go straight up or down
                if self.recovery_target.ledge and not smashbot_state.is_facing_inwards():
                    self.max_angle = min(self.max_angle, ControlStick.from_angle(90).to_edge_coordinate(True) - 1)
                    self.min_angle = max(self.min_angle, ControlStick.from_angle(-90).to_edge_coordinate(True) + 1)

                self.hill_climb = HillClimb(self.min_angle, self.max_angle, 40)

            next_point = round(self.hill_climb.get_next_point())
            if self.current_frame <= 9 and self.min_angle <= self.ANGLES_TO_TEST[self.current_frame - 1] <= self.max_angle:
                next_point = self.ANGLES_TO_TEST[self.current_frame - 1]
            current_angle = ControlStick.from_edge_coordinate(next_point).correct_for_cardinal_strict().to_edge_coordinate(True)
            LogUtils.simple_log(current_angle, self.best_angle)

            # Test current angle in trial
            self.trajectory = self.create_trajectory(game_state, smashbot_state, self.start_x_velocity, ControlStick.coordinate_num_to_angle(current_angle))
            relative_target = (abs(smashbot_state.position.x) - self.target_coords[0], self.target_coords[1] - smashbot_state.position.y)
            stage_vertex = self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y)

            if self.recovery_target.is_max():
                recovery_distance = self.trajectory.get_distance_traveled_above_target(inward_x_velocity, relative_target, stage_vertex, knockback_angle, knockback_magnitude, self.current_frame)
            else:
                recovery_distance = self.trajectory.get_distance(inward_x_velocity, relative_target[1], stage_vertex, self.recovery_target.ledge, knockback_angle, knockback_magnitude, self._generate_fade_back_frames(), self.current_frame)

            # Record angle for hill-climbing
            extra_distance = recovery_distance - (abs(smashbot_state.position.x) - self.target_coords[0])
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
                self.best_angle = ControlStick.from_edge_coordinate(round(self.hill_climb.get_next_point())).correct_for_cardinal_strict().to_edge_coordinate(True)

            xy = ControlStick.from_edge_coordinate(self.best_angle).to_smashbot_xy()
            LogUtils.simple_log(xy)
            self.controller.tilt_analog(Button.BUTTON_MAIN, (1 - inward_x) + (2 * inward_x - 1) * xy[0], xy[1])

        elif self.current_frame >= 42:
            self._perform_fade_back(game_state, smashbot_state, knockback_angle, knockback_magnitude, inward_x_velocity, inward_x)

        LogUtils.simple_log("frame number:", self.current_frame, smashbot_state.action_frame)
        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FIREFOX_AIR, Action.FIREFOX_WAIT_AIR, Action.SWORD_DANCE_1_AIR, Action.DEAD_FALL}

    def __update_best_angle(self, current_angle, extra_distance):
        self.best_distance = extra_distance
        self.best_angle = current_angle

    def __determine_initial_min_angle(self):
        if self.recovery_target.is_sweet_spot():
            return ControlStick.from_angle(-90).to_edge_coordinate(True)
        return ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_edge_coordinate(True)