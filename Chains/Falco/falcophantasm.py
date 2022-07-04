import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.chain import Chain
from Utils.angleutils import AngleUtils
from Utils.enums import FADE_BACK_MODE
from Utils.logutils import LogUtils
from Utils.mathutils import MathUtils
from Utils.recoverytarget import RecoveryTarget
from Utils.trajectory import Trajectory


class FalcoPhantasm(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.FALCO, 0, 24, -999, 999, "Data/falco_phantasm.csv")

    @staticmethod
    def create_trajectory(x_velocity):
        trajectory = FalcoPhantasm.TRAJECTORY.copy()
        x_velocity = max(2 / 3 * abs(x_velocity) - 0.05, 0)

        for i in range(15):
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

    @staticmethod
    def create_shorten_trajectory(amount):
        result = FalcoPhantasm.TRAJECTORY.copy()

        for i in range(amount):
            result.frames[19-i].forward_acceleration = result.frames[19-i].max_horizontal_velocity - result.frames[17-i].max_horizontal_velocity
            result.frames[19-i].backward_acceleration = result.frames[19-i].min_horizontal_velocity - result.frames[17-i].min_horizontal_velocity
            result.frames.pop(18-i)

        return result

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), recovery_target=RecoveryTarget.max()):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.recovery_target = recovery_target
        self.current_frame = -1
        self.trajectory = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.FOX_ILLUSION, Action.FOX_ILLUSION_START, Action.FOX_ILLUSION_SHORTENED]:
            return False

        x = smashbot_state.get_inward_x()

        useful_x_velocity = smashbot_state.speed_air_x_self * -MathUtils.sign(smashbot_state.position.x)
        if self.trajectory is None:
            self.trajectory = FalcoPhantasm.create_trajectory(useful_x_velocity)

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
            if self.recovery_target.fade_back_mode == FADE_BACK_MODE.EARLY and 15 <= self.current_frame <= 18:
                self.trajectory = FalcoPhantasm.create_shorten_trajectory(19 - self.current_frame)
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