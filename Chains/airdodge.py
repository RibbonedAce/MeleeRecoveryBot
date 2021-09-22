import math

from melee.enums import Button, Action

from Chains.chain import Chain
from Utils.enums import FADE_BACK_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.trajectory import Trajectory
from Utils.trajectoryframe import TrajectoryFrame
from Utils.utils import Utils


class AirDodge(Chain):

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    @staticmethod
    def create_trajectory(character, angle):
        frames = []
        velocity = [2.79 * math.cos(math.radians(angle)), 2.79 * math.sin(math.radians(angle))]

        for i in range(29):
            frames.append(TrajectoryFrame(velocity[1], 0, 0, velocity[0], None, velocity[0], 0))
            velocity[0] *= 0.9
            velocity[1] *= 0.9

        frames += FrameDataUtils.create_trajectory_frames(character, velocity[1])

        air_dodge_offset = 0
        for i in range(50):
            air_dodge_offset += frames[min(i, len(frames) - 1)].vertical_velocity

        return Trajectory(character, 30, -999, air_dodge_offset, frames)

    def __init__(self, target_coords=(0, 0), fade_back=FADE_BACK_MODE.NONE, ledge=False):
        self.target_coords = target_coords
        self.fade_back = fade_back
        self.ledge = ledge
        self.current_frame = -1
        self.trajectory = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        if self.trajectory is None:
            self.trajectory = self.__decide_trajectory(smashbot_state.character)

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in [Action.AIRDODGE, Action.DEAD_FALL]:
            self.interruptable = True
            controller.empty_input()
            return True

        x = PlayerStateUtils.get_inward_x(smashbot_state)

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in [Action.AIRDODGE, Action.DEAD_FALL]:
            self.interruptable = False
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            self.current_frame = 0
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_L)

            # Check if we should still fade-back
            should_fade_back = False
            recovery_distance = None
            useful_x_velocity = smashbot_state.speed_air_x_self * -Utils.sign(smashbot_state.position.x)

            # See if we can fade back on this frame
            if self.fade_back != FADE_BACK_MODE.NONE:
                fade_back_frames = set()
                # If we can make it by fading back this frame, do it
                if self.fade_back == FADE_BACK_MODE.EARLY:
                    fade_back_frames.add(self.current_frame)
                # If we can make it by holding a fade back starting this frame, do it
                elif self.fade_back == FADE_BACK_MODE.LATE:
                    for i in range(self.current_frame, 600):
                        fade_back_frames.add(i)

                recovery_distance = self.trajectory.get_remaining_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.ledge, fade_back_frames, self.current_frame)
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

            controller.tilt_analog(Button.BUTTON_MAIN, x_input, 0.5)
        self.interruptable = False
        return True

    def __decide_trajectory(self, character):
        return AirDodge.create_trajectory(character, 90)