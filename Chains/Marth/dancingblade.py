from melee import FrameData
from melee.enums import Action, Button, Character

from Chains.Abstract import StallChain
from Chains.Marth.dolphinslash import DolphinSlash
from Utils import MathUtils, Trajectory


class DancingBlade(StallChain):
    TRAJECTORY = Trajectory.from_csv_file(Character.MARTH, 0, 1, -999, 999, "Data/Trajectories/dancing_blade.csv", include_fall_frames=False)

    @classmethod
    def create_trajectory(cls, game_state, smashbot_state, x_velocity, force_charge=None):
        trajectory = cls.TRAJECTORY.copy()
        x_velocity = MathUtils.sign(x_velocity) * max(0.8 * abs(x_velocity) - 0.0025, 0)

        y_velocity = trajectory.frames[0].vertical_velocity
        if force_charge != True and (force_charge == False or not smashbot_state.stall_is_charged(game_state)):
            y_velocity -= 1

        for i in range(29):
            trajectory.frames[i].min_horizontal_velocity = x_velocity
            trajectory.frames[i].max_horizontal_velocity = x_velocity
            trajectory.frames[i].vertical_velocity = y_velocity

            if i == 0:
                trajectory.frames[i].forward_acceleration = x_velocity
                trajectory.frames[i].backward_acceleration = x_velocity
            else:
                trajectory.frames[i].forward_acceleration = x_velocity - trajectory.frames[i - 1].max_horizontal_velocity
                trajectory.frames[i].backward_acceleration = x_velocity - trajectory.frames[i - 1].min_horizontal_velocity

            x_velocity = MathUtils.sign(x_velocity) * max(abs(x_velocity) - 0.0025, 0)
            y_velocity = max(y_velocity - 0.06, -1.5)

        trajectory.max_ledge_grab = trajectory.get_displacement_after_frames(0, 29)[1]
        return trajectory

    @classmethod
    def _get_primary_recovery(cls, game_state, smashbot_state):
        return DolphinSlash.create_trajectory(game_state, smashbot_state, smashbot_state.get_inward_x_velocity())

    @classmethod
    def _double_jumps_gained(cls):
        return 0

    @classmethod
    def _min_stall_speed(cls, character):
        return FrameData.INSTANCE.get_air_speed(character) - FrameData.INSTANCE.get_air_mobility(character)

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        x = smashbot_state.get_inward_x()

        # If we are not finished with the stall
        if not self.used_move:
            # If double jumping, wait until you reach max height
            if smashbot_state.speed_y_self >= 0 and smashbot_state.action == Action.JUMPING_ARIAL_FORWARD:
                self.interruptable = True
                controller.tilt_analog(Button.BUTTON_MAIN, x, smashbot_state.get_inward_x())
                return True

            # Do the stall if the max height has been achieved
            if smashbot_state.speed_y_self < 0:
                self.interruptable = False
                controller.tilt_analog(Button.BUTTON_MAIN, smashbot_state.get_inward_x(), 0.5)
                controller.press_button(Button.BUTTON_B)
                self.used_move = True
                return True

        # If in the middle of stall, we are not interruptable
        if smashbot_state.action == Action.SWORD_DANCE_1_AIR:
            self.interruptable = False
            controller.tilt_analog(Button.BUTTON_MAIN, x, smashbot_state.get_inward_x())
            return True

        return False