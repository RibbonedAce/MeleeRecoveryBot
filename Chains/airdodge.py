import math

from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import AngleUtils, LogUtils, Trajectory
from Utils.enums import FADE_BACK_MODE


class AirDodge(RecoveryChain):
    TRAJECTORY_DICTIONARY = {Character.CPTFALCON: Trajectory.from_csv_file(Character.CPTFALCON, 0, 30, -999, 999, "Data/Trajectories/falcon_air_dodge.csv", include_fall_frames=False),
                             Character.FOX: Trajectory.from_csv_file(Character.FOX, 0, 30, -999, 999, "Data/Trajectories/falcon_air_dodge.csv", include_fall_frames=False),
                             Character.FALCO: Trajectory.from_csv_file(Character.FALCO, 0, 30, -999, 999, "Data/Trajectories/falco_air_dodge.csv", include_fall_frames=False),
                             Character.GANONDORF: Trajectory.from_csv_file(Character.GANONDORF, 0, 30, -999, 999, "Data/Trajectories/ganondorf_air_dodge.csv", include_fall_frames=False),
                             Character.MARTH: Trajectory.from_csv_file(Character.MARTH, 0, 30, -999, 999, "Data/Trajectories/marth_air_dodge.csv", include_fall_frames=False)}

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, angle=0.0):
        trajectory = AirDodge.TRAJECTORY_DICTIONARY[smashbot_state.character].copy()
        velocity = [2.79 * math.cos(math.radians(angle)), 2.79 * math.sin(math.radians(angle))]

        for i in range(29):
            trajectory.frames[i].vertical_velocity = velocity[1]
            trajectory.frames[i].min_horizontal_velocity = velocity[0]
            trajectory.frames[i].max_horizontal_velocity = velocity[0]

            if i == 0:
                trajectory.frames[i].forward_acceleration = velocity[0]
                trajectory.frames[i].backward_acceleration = velocity[0]
            else:
                trajectory.frames[i].forward_acceleration = velocity[0] - trajectory.frames[i-1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = velocity[0] - trajectory.frames[i-1].min_horizontal_velocity

            velocity[0] *= 0.9
            velocity[1] *= 0.9

        frames = Trajectory.create_trajectory_frames(smashbot_state.character, velocity[1] / 0.9)
        for i in range(29, 49):
            index = min(i - 29, len(frames) - 1)
            trajectory.frames[i].vertical_velocity = frames[index].vertical_velocity
            trajectory.frames[i].forward_acceleration = frames[index].forward_acceleration
            trajectory.frames[i].backward_acceleration = frames[index].backward_acceleration
            trajectory.frames[i].min_horizontal_velocity = frames[index].min_horizontal_velocity
            trajectory.frames[i].max_horizontal_velocity = frames[index].max_horizontal_velocity

        trajectory.frames += frames[min(20, len(frames) - 1):]
        trajectory.max_ledge_grab = trajectory.get_displacement_after_frames(0, 50)[1]
        return trajectory

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.trajectory is None:
            self.trajectory = AirDodge.create_trajectory(game_state, smashbot_state, smashbot_state.character, 90)

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.AIRDODGE, Action.DEAD_FALL]:
            return False

        x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in [Action.AIRDODGE, Action.DEAD_FALL]:
            self.interruptable = False
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0

            LogUtils.simple_log("smashbot_state.position.x", "smashbot_state.position.y", "smashbot_state.speed_air_x_self", "smashbot_state.speed_y_self", "smashbot_state.speed_x_attack", "smashbot_state.speed_y_attack", "ecb.bottom", "smashbot_state.ecb.left", "smashbot_state.ecb.right",
                                "FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character)", "FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)", "self.ledge", "self.fade_back", "x_input", "should_fade_back", "recovery_distance",
                                "frame.vertical_velocity", "frame.forward_acceleration", "frame.backward_acceleration", "frame.max_horizontal_velocity", "frame.mid_horizontal_velocity", "frame.min_horizontal_velocity", "frame.ecb_bottom", "frame.ecb_inward")
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_L)

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

            LogUtils.simple_log(smashbot_state.position.x, smashbot_state.position.y, smashbot_state.speed_air_x_self, smashbot_state.speed_y_self, smashbot_state.speed_x_attack, smashbot_state.speed_y_attack, smashbot_state.ecb.bottom.y, smashbot_state.ecb.left.x, smashbot_state.ecb.right.x,
                                FrameData.INSTANCE.get_ledge_box_horizontal(smashbot_state.character), FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character), self.recovery_target.ledge, self.recovery_target.fade_back_mode, x_input, should_fade_back, recovery_distance,
                                frame.vertical_velocity, frame.forward_acceleration, frame.backward_acceleration, frame.max_horizontal_velocity, frame.mid_horizontal_velocity, frame.min_horizontal_velocity, frame.ecb_bottom, frame.ecb_inward)
            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True