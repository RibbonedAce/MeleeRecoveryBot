from melee.enums import Action, Button, Character

from Chains import Chain
from Utils.enums import FADE_BACK_MODE
from Utils.playerstateutils import PlayerStateUtils
from Utils.trajectory import Trajectory
from Utils.utils import Utils


class RaptorBoost(Chain):
    TRAJECTORY = Trajectory.from_csv_file(Character.CPTFALCON, 30, -999, -64, "Data/raptor_boost.csv")

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), fade_back=FADE_BACK_MODE.NONE, ledge=False):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.fade_back = fade_back
        self.ledge = ledge
        self.current_frame = -1

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action != Action.FOX_ILLUSION:
            self.interruptable = True
            controller.empty_input()
            return True

        x = PlayerStateUtils.get_inward_x(smashbot_state)

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action != Action.FOX_ILLUSION:
            self.interruptable = False
            controller.press_button(Button.BUTTON_B)
            controller.tilt_analog(Button.BUTTON_MAIN, x, 0.5)
            self.current_frame = 0
            return True

        # Deciding if we should fade-back
        if self.current_frame >= 0:
            self.current_frame += 1
            controller.release_button(Button.BUTTON_B)

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

                recovery_distance = RaptorBoost.TRAJECTORY.get_remaining_distance(useful_x_velocity, self.target_coords[1] - smashbot_state.position.y, self.ledge, fade_back_frames, self.current_frame)
                if abs(smashbot_state.position.x) - recovery_distance <= self.target_coords[0]:
                    should_fade_back = True

            frame = RaptorBoost.TRAJECTORY.frames[min(self.current_frame, len(RaptorBoost.TRAJECTORY.frames) - 1)]

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