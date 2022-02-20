from melee import Button, FrameData

from Chains.chain import Chain


class DriftOut(Chain):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

        # Cannot drift out if on ground
        if smashbot_state.on_ground:
            return False

        # Should not drift out if at ledge grab height
        if smashbot_state.position.y > -FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character):
            return False

        # Should not try to drift if wall jumping
        if smashbot_state.is_wall_teching():
            return False

        # Should not drift out unless on track to go underneath ledge
        position = abs(smashbot_state.position.x)
        velocity = smashbot_state.speed_air_x_self * position / smashbot_state.position.x
        if velocity > 0:
            return False

        mobility = FrameData.INSTANCE.get_air_mobility(smashbot_state.character)
        while True:
            velocity += mobility
            if velocity > 0:
                break
            position += velocity

        return position < game_state.get_stage_edge()

    def step_internal(self, game_state, smashbot_state, opponent_state):
        controller = self.controller
        self.interruptable = True
        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog(Button.BUTTON_MAIN, smashbot_state.get_outward_x(), 0.5)
        controller.tilt_analog(Button.BUTTON_C, 0.5, 0.5)
        return True
