import math
import random
from enum import Enum

from melee.enums import Button

from Chains.chain import Chain
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils


class TECH_DIRECTION(Enum):
    TECH_IN_PLACE = 0
    TECH_BACK = 1
    TECH_FORWARD = 2
    TECH_RANDOM = 3


# Grab and throw opponent
class Tech(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        tech_lockout = GameStateUtils.get_smashbot_custom(game_state, "tech_lockout")
        character_data = FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]

        # Tech if we need to
        #   Calculate when we will land
        if smashbot_state.position.y > -4 and PlayerStateUtils.is_flying_in_hit_stun(smashbot_state):
            frames_until_landing = 0
            speed = smashbot_state.speed_y_self
            knockback_angle = math.radians(PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state))
            knockback_magnitude = PlayerStateUtils.get_knockback_magnitude(smashbot_state, opponent_state)
            height = smashbot_state.position.y

            while height > 0 or speed + knockback_magnitude * math.sin(knockback_angle) > 0:
                height += speed + knockback_magnitude * math.sin(knockback_angle)
                speed -= character_data["Gravity"]
                speed = max(speed, -character_data["TerminalVelocity"])
                knockback_magnitude = max(knockback_magnitude - 0.051, 0)
                frames_until_landing += 1
                # Break if it will be false anyway
                if frames_until_landing >= 3 or frames_until_landing >= tech_lockout:
                    return False

            return True

        return False

    def __init__(self, direction=TECH_DIRECTION.TECH_RANDOM):
        if direction == TECH_DIRECTION.TECH_RANDOM:
            self.direction = TECH_DIRECTION(random.randint(0, 2))
        else:
            self.direction = direction

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # If we're on the ground, we're done here
        if smashbot_state.on_ground:
            self.interruptable = True
            controller.empty_input()
            return True

        if GameStateUtils.get_smashbot_custom(game_state, "tech_lockout") > 0:
            controller.empty_input()
            return True

        if self.direction == TECH_DIRECTION.TECH_IN_PLACE:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, .5, .5)
            return True
        elif self.direction == TECH_DIRECTION.TECH_FORWARD:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, int(smashbot_state.facing), .5)
            return True
        elif self.direction == TECH_DIRECTION.TECH_BACK:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, int(not smashbot_state.facing), .5)
            return True

        return False
