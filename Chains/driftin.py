from melee import Button

from Chains.chain import Chain


class DriftIn(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

        # Cannot drift in if on ground
        if smashbot_state.on_ground:
            return False

        # Should not try to drift if wall jumping
        if smashbot_state.is_wall_teching():
            return False

        # Should not drift past ledge
        if smashbot_state.position.y < 0 and abs(smashbot_state.position.x) <= game_state.get_stage_edge():
            return False

        return True

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_MAIN, smashbot_state.get_inward_x(), 0.5)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
        return True
