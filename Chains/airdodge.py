import math

from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import Trajectory


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
        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        inward_x = smashbot_state.get_inward_x()

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_L, (0.5, 1))

        self._increment_current_frame(smashbot_state)
        knockback = smashbot_state.get_relative_knockback(opponent_state)
        inward_x_velocity = smashbot_state.get_inward_x_velocity()

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_L)

                self.trajectory = self.create_trajectory(game_state, smashbot_state, smashbot_state.character, 90)

            self._perform_fade_back(game_state, smashbot_state, knockback, inward_x_velocity, inward_x)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.AIRDODGE, Action.DEAD_FALL}