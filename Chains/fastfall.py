from melee import FrameData
from melee.enums import Button

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils.enums import FAST_FALL_MODE
from Utils.trajectory import Trajectory


class FastFall(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        # If we do not want to fast-fall, then do not
        if DifficultySettings.FAST_FALL == FAST_FALL_MODE.NEVER:
            return False

        # Cannot fast-fall if not in air
        if smashbot_state.on_ground:
            return False

        # Cannot fast-fall if not in the state to do so
        if smashbot_state.hitstun_frames_left > 0 or smashbot_state.is_wall_teching():
            return False

        # Cannot fast-fall while moving upward
        if smashbot_state.speed_y_self > 0:
            return False

        # Cannot fast-fall again if already doing so
        fast_fall_speed = FrameData.INSTANCE.get_fast_fall_speed(smashbot_state.character)
        if smashbot_state.speed_y_self <= -fast_fall_speed:
            return False

        # Should only fast-fall if going to grab ledge or land
        trajectory = Trajectory.create_drift_trajectory(smashbot_state.character, -fast_fall_speed)
        stage_edge = game_state.get_stage_edge()

        if trajectory.get_extra_distance(smashbot_state, opponent_state, (stage_edge, 0), False) > 0 or \
            smashbot_state.is_facing_inwards() and trajectory.get_extra_distance(smashbot_state, opponent_state, (stage_edge, 0), True) > 0:
            if smashbot_state.position.y < -30:
                print(trajectory.get_extra_distance(smashbot_state, opponent_state, (stage_edge, 0), False))
            return True

    def __init__(self):
        Chain.__init__(self)
        self.fell = False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)

        if self.fell and game_state.frame % 2 == 0:
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0.5)
        else:
            controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 0)

        self.fell = True
        return True
