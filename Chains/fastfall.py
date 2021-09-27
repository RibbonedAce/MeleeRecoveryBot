import math

from melee.enums import Button

from Chains.chain import Chain
from Utils.difficultysettings import DifficultySettings
from Utils.enums import FAST_FALL_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.utils import Utils


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
        if smashbot_state.hitstun_frames_left > 0 or PlayerStateUtils.is_wall_teching(smashbot_state):
            return False

        # Cannot fast-fall while moving upward
        if smashbot_state.speed_y_self > 0:
            return False

        # Cannot fast-fall again if already doing so
        term_velocity = FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]["FastFallSpeed"]
        if smashbot_state.speed_y_self <= -term_velocity:
            return False

        # Should only fast-fall if going to grab ledge or land
        trajectory = FrameDataUtils.create_trajectory_frames(smashbot_state.character, -term_velocity)
        angle = PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)
        magnitude = PlayerStateUtils.get_knockback_magnitude(smashbot_state, opponent_state)
        facing_inward = PlayerStateUtils.is_facing_inwards(smashbot_state)

        x_vel = abs(smashbot_state.speed_air_x_self)
        x = abs(smashbot_state.position.x)
        y = smashbot_state.position.y
        stage_edge = GameStateUtils.get_stage_edge(game_state)

        for i in range(0, 300):
            drag = FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]["AirFriction"]

            frame = trajectory[min(i, len(trajectory) - 1)]

            x_vel += min(frame.forward_acceleration, max(frame.max_horizontal_velocity - x_vel, -drag))
            magnitude = max(magnitude - 0.051, 0)

            true_x_vel = abs(math.cos(math.radians(angle)) * magnitude) - x_vel
            x += true_x_vel
            y_vel = frame.vertical_velocity + math.sin(math.radians(angle)) * magnitude
            y += y_vel

            if y_vel < 0 and y < -Utils.LEDGE_GRAB_AREA[1]:
                return False

            if y_vel < 0 and (x < stage_edge and y >= 0 and true_x_vel < 0 or
                              facing_inward and x < stage_edge + Utils.LEDGE_GRAB_AREA[0] and -Utils.LEDGE_GRAB_AREA[1] <= y <= -Utils.LEDGE_GRAB_AREA_HIGH[1]):
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
