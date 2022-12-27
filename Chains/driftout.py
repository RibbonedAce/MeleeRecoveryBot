from melee import Button, FrameData

from Chains.chain import Chain
from Utils import TrajectoryFrame, Vector2


class DriftOut(Chain):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]

        # Cannot drift out if on ground
        if smashbot_state.on_ground:
            return False

        # Should not drift out if at ledge grab height
        if smashbot_state.position.y > -FrameData.INSTANCE.get_ledge_box(smashbot_state.character).top:
            return False

        # Should not try to drift if wall jumping
        if smashbot_state.is_wall_teching():
            return False

        # Should not drift out unless on track to go underneath ledge
        position = abs(smashbot_state.position.x)
        velocity = Vector2(smashbot_state.get_inward_x_velocity(), 0)
        if velocity.x < 0:
            return False

        frame = TrajectoryFrame.drift(smashbot_state.character)
        while velocity.x >= 0:
            velocity = frame.velocity(velocity, Vector2(-1, 0))
            position += velocity.x

        return position < game_state.get_stage_edge()

    def step_internal(self, propagate):
        smashbot_state = propagate[1]
        controller = self.controller
        self.interruptable = True

        controller.release_button(Button.BUTTON_L)
        controller.release_button(Button.BUTTON_Y)
        controller.tilt_analog_unit(Button.BUTTON_MAIN, smashbot_state.get_outward_x(), 0)
        controller.tilt_analog_unit(Button.BUTTON_C, 0, 0)
        return True
