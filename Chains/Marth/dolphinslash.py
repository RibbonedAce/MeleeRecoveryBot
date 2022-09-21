import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import AngleUtils, LogUtils, MathUtils, Trajectory, TrajectoryFrame
from Utils.enums import FADE_BACK_MODE


class DolphinSlash(RecoveryChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.MARTH, 5, 20, -999, 999, "Data/Trajectories/dolphin_slash.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = MathUtils.sign(x_velocity) * max(0.666 * abs(x_velocity) - 0.05, 0)

        for i in range(5):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = MathUtils.sign(x_velocity) * max(abs(x_velocity) - 0.05, 0)

        for i in range(5, 22):
            frame_magnitude = (trajectory.frames[i].max_horizontal_velocity ** 2 + trajectory.frames[i].vertical_velocity ** 2) ** 0.5
            frame_angle = math.degrees(math.atan2(trajectory.frames[i].vertical_velocity, trajectory.frames[i].max_horizontal_velocity))
            frame_angle -= angle
            if frame_angle > 90:
                frame_angle = 180 - frame_angle
            x_angle = math.cos(math.radians(frame_angle))
            y_angle = math.sin(math.radians(frame_angle))

            trajectory.frames[i].vertical_velocity =y_angle * frame_magnitude
            trajectory.frames[i].min_horizontal_velocity = x_angle * frame_magnitude
            trajectory.frames[i].max_horizontal_velocity = x_angle * frame_magnitude
            trajectory.frames[i].forward_acceleration = x_angle * frame_magnitude - trajectory.frames[i - 1].max_horizontal_velocity
            trajectory.frames[i].backward_acceleration = x_angle * frame_magnitude - trajectory.frames[i - 1].min_horizontal_velocity

        for i in range(22, 39):
            trajectory.frames[i].vertical_velocity = trajectory.frames[i - 1].vertical_velocity - 0.06

        gravity = -FrameData.INSTANCE.get_gravity(smashbot_state.character)
        mobility = FrameData.INSTANCE.get_air_mobility(smashbot_state.character)
        speed = trajectory.frames[38].max_horizontal_velocity
        velocity = trajectory.frames[38].vertical_velocity
        term_velocity = -2.5

        while velocity != term_velocity:
            velocity = max(velocity + gravity, term_velocity)
            trajectory.frames.append(TrajectoryFrame(
                vertical_velocity=velocity,
                forward_acceleration=mobility,
                backward_acceleration=-mobility,
                max_horizontal_velocity=speed,
                min_horizontal_velocity=-speed))

        return trajectory

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.trajectory is None:
            self.trajectory = self.create_trajectory(game_state, smashbot_state, 0)

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.SHINE_RELEASE_AIR, Action.DEAD_FALL]:
            return False

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in [Action.SHINE_RELEASE_AIR]:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "smashbot_state.ecb.left", "smashbot_state.ecb.right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

            # Check if we should still fade-back
            should_fade_back = False
            useful_x_velocity = smashbot_state.get_inward_x_velocity()
            angle = smashbot_state.get_knockback_angle(opponent_state)
            if math.cos(math.radians(angle)) > 0:
                angle = AngleUtils.get_x_reflection(angle)
            magnitude = smashbot_state.get_knockback_magnitude(opponent_state)

            recovery_distance = None

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

            x_input = x
            if smashbot_state.action == Action.SHINE_RELEASE_AIR and smashbot_state.action_frame == 5:
                x_input = smashbot_state.get_inward_x()
            elif should_fade_back:
                x_input = 1 - x

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True