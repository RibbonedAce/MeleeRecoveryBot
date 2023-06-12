from collections import defaultdict

from melee import FrameData
from melee.enums import Button

from Chains.chain import Chain
from difficultysettings import DifficultySettings
from Utils import FrameInput, LogUtils, Trajectory, Vector2
from Utils.enums import FAST_FALL_MODE


class FastFall(Chain):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

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
        if smashbot_state.speed_y_self <= -FrameData.INSTANCE.get_fast_fall_speed(smashbot_state.character):
            return False

        # Should only fast-fall if going to grab ledge or land
        trajectory = Trajectory.create_drift_trajectory(smashbot_state.character)
        target = Vector2(game_state.get_stage_edge(), 0)
        fast_fall_inputs = defaultdict(FrameInput.forward)
        fast_fall_inputs[0] = FrameInput.direct(Vector2(0, -1))

        stage_distance = trajectory.get_extra_distance(propagate, target=target, ledge=False, input_frames=fast_fall_inputs)
        if stage_distance > 0 or smashbot_state.is_facing_inwards() and trajectory.get_extra_distance(propagate, target=target, ledge=True, input_frames=fast_fall_inputs) > 0:
            if smashbot_state.position.y < -30:
                LogUtils.simple_log(stage_distance)
            return True

    def __init__(self):
        Chain.__init__(self)
        self.fell = False

    def step_internal(self, propagate):
        game_state = propagate[0]
        controller = self.controller
        self.interruptable = True

        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog_unit(Button.BUTTON_C, 0, 0)

        if self.fell and game_state.frame % 2 == 0:
            controller.tilt_analog_unit(Button.BUTTON_MAIN, 0, 0)
        else:
            controller.tilt_analog_unit(Button.BUTTON_MAIN, 0, -1)

        self.fell = True
        return True
