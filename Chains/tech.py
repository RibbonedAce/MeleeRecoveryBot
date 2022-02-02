import math
import random
from enum import Enum

from melee import FrameData, GameState
from melee.enums import Action, Button

from Chains.chain import Chain


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

        # Tech if we need to
        #   Calculate when we will land
        if smashbot_state.position.y > -4 and smashbot_state.is_flying_in_hit_stun():
            frames_until_landing = 0
            speed = smashbot_state.speed_y_self
            knockback_angle = math.radians(smashbot_state.get_knockback_angle(opponent_state))
            knockback_magnitude = smashbot_state.get_knockback_magnitude(opponent_state)
            height = smashbot_state.position.y

            while height > 0 or speed + knockback_magnitude * math.sin(knockback_angle) > 0:
                height += speed + knockback_magnitude * math.sin(knockback_angle)
                speed -= FrameData.INSTANCE.get_gravity(smashbot_state.character)
                speed = max(speed, -FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character))
                knockback_magnitude = max(knockback_magnitude - 0.051, 0)
                frames_until_landing += 1
                # Break if it will be false anyway
                if frames_until_landing >= 3:
                    return False

            # Need to get out of tech lockout before landing
            return frames_until_landing > GameState.TECH_LOCKOUT[smashbot_state.get_port(game_state)]

        return False

    def __init__(self, direction=TECH_DIRECTION.TECH_RANDOM):
        Chain.__init__(self)
        self.teched = False
        if direction == TECH_DIRECTION.TECH_RANDOM:
            self.direction = TECH_DIRECTION(random.randint(0, 2))
        else:
            self.direction = direction

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller

        # If we are off the stage, we're done here
        if abs(smashbot_state.position.x) > game_state.get_stage_edge():
            return False

        # If we're not tumbling, or in hit-stun, or hitting the tech, we're done here
        if smashbot_state.action != Action.TUMBLING and not smashbot_state.is_flying_in_hit_stun() and not (smashbot_state.is_teching() and smashbot_state.action_frame < 2):
            return False

        # Wait for tech lockout to end
        if not self.teched and not smashbot_state.can_tech(game_state):
            self.interruptable = False
            controller.empty_input()
            return True

        self.interruptable = False
        self.teched = True
        x = smashbot_state.get_inward_x()

        if self.direction == TECH_DIRECTION.TECH_IN_PLACE:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, .5, .5)
            return True
        elif self.direction == TECH_DIRECTION.TECH_FORWARD:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, x, .5)
            return True
        elif self.direction == TECH_DIRECTION.TECH_BACK:
            controller.press_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, 1 - x, .5)
            return True

        return False
