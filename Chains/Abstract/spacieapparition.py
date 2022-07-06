import math
from abc import ABCMeta

from melee import FrameData
from melee.enums import Action, Button

from Chains.Abstract.recoverychain import RecoveryChain
from Utils import AngleUtils, LogUtils, MathUtils
from Utils.enums import FADE_BACK_MODE


class SpacieApparition(RecoveryChain, metaclass=ABCMeta):
    @classmethod
    def create_shorten_trajectory(cls, amount):
        result = cls.create_trajectory(None, 0)
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
        controller = self.controller

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FOX_ILLUSION, Action.FOX_ILLUSION_START, Action.FOX_ILLUSION_SHORTENED]:
            return False

        x = smashbot_state.get_inward_x()

        useful_x_velocity = smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x)
        if self.trajectory is None:
            self.trajectory = self.create_trajectory(smashbot_state, useful_x_velocity)

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action != Action.FOX_ILLUSION:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "smashbot_state.ecb_bottom", "smashbot_state.ecb_left", "smashbot_state.ecb_right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

            # Check if we should still fade-back
            should_fade_back = False
            angle = smashbot_state.get_knockback_angle(opponent_state)
            if math.cos(math.radians(angle)) > 0:
                angle = AngleUtils.get_x_reflection(angle)
            magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

            recovery_distance = None

            # Decide if we should shorten
            shorten_frame = self._get_shorten_frame()
            if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY and shorten_frame <= self.current_frame <= shorten_frame + 3:
                self.trajectory = self.create_shorten_trajectory(shorten_frame + 4 - self.current_frame)
                recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y), self.recovery_target.ledge, angle, magnitude, start_frame=self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    controller.press_button(Button.BUTTON_B)

            # See if we can fade back on this frame
            if self.recovery_target.fade_back_mode != FADE_BACK_MODE.NONE:
                fade_back_frames = set()
                # If we can make it by fading back this frame, do it
                if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY:
                    fade_back_frames.add(self.current_frame)
                # If we can make it by holding a fade back starting this frame, do it
                elif self.recovery_target.fade_back_mode == FADE_BACK_MODE.LATE:
                    for i in range(self.current_frame, 600):
                        fade_back_frames.add(i)

                recovery_distance = self.trajectory.get_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.trajectory.get_relative_stage_vertex(game_state, abs(smashbot_state.position.x), smashbot_state.position.y), self.recovery_target.ledge, angle, magnitude, fade_back_frames, self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    should_fade_back = True

            frame = self.trajectory.frames[min(self.current_frame, len(self.trajectory.frames) - 1)]

            if should_fade_back:
                x_input = 1 - x
                # If returning to neutral makes us fade-back faster, do it
                if frame.mid_horizontal_velocity is not None and \
                        frame.mid_horizontal_velocity < useful_x_velocity + frame.backward_acceleration:
                    x_input = 0.5

            else:
                x_input = x
                # If returning to neutral makes us fade-forward faster, do it
                if frame.mid_horizontal_velocity is not None and \
                        frame.mid_horizontal_velocity > useful_x_velocity + frame.forward_acceleration:
                    x_input = 0.5

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb_bottom[1], smashbot_state.ecb_left[0], smashbot_state.ecb_right[0],
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True