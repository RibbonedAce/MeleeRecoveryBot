import math
from abc import ABCMeta

from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import AngleUtils
from Utils.enums import FADE_BACK_MODE


class SpacieApparition(RecoveryChain, metaclass=ABCMeta):
    @classmethod
    def create_shorten_trajectory(cls, amount):
        result = cls.create_trajectory(None, None, 0)
        shorten_frame = cls._get_shorten_frame()

        for i in range(amount):
            result.frames[shorten_frame + 4 - i].forward_acceleration = result.frames[shorten_frame + 4 - i].max_horizontal_velocity - result.frames[shorten_frame + 2 - i].max_horizontal_velocity
            result.frames[shorten_frame + 4 - i].backward_acceleration = result.frames[shorten_frame + 4 - i].min_horizontal_velocity - result.frames[shorten_frame + 2 - i].min_horizontal_velocity
            result.frames.pop(shorten_frame + 3 - i)

        return result

    @classmethod
    def _get_shorten_frame(cls) -> int: ...

    @classmethod
    def _adjust_trajectory(cls, trajectory, x_velocity):
        x_velocity = max(2 / 3 * abs(x_velocity) - 0.05, 0)
        for i in range(cls._get_shorten_frame()):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = max(x_velocity - 0.05, 0)

        return trajectory

    def step_internal(self, game_state, smashbot_state, opponent_state):
        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        inward_x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_B, (inward_x, 0.5))

        self._increment_current_frame(smashbot_state)
        knockback_angle = smashbot_state.get_knockback_angle(opponent_state)
        if math.cos(math.radians(knockback_angle)) > 0:
            knockback_angle = AngleUtils.get_x_reflection(knockback_angle)
        knockback_magnitude = smashbot_state.get_knockback_magnitude(opponent_state)
        inward_x_velocity = smashbot_state.get_inward_x_velocity()

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_B)

                self.trajectory = self.create_trajectory(game_state, smashbot_state, inward_x_velocity)

            # Decide if we should shorten
            shorten_frame = self._get_shorten_frame()
            if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY and shorten_frame <= self.current_frame <= shorten_frame + 3:
                self.trajectory = self.create_shorten_trajectory(shorten_frame + 4 - self.current_frame)
                recovery_distance = self.trajectory.get_distance(inward_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y), self.recovery_target.ledge, knockback_angle, knockback_magnitude, start_frame=self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    self.controller.press_button(Button.BUTTON_B)

            self._perform_fade_back(game_state, smashbot_state, knockback_angle, knockback_magnitude, inward_x_velocity, inward_x)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.FOX_ILLUSION, Action.FOX_ILLUSION_START, Action.FOX_ILLUSION_SHORTENED, Action.DEAD_FALL}