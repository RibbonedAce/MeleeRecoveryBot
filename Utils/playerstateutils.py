import math

from melee import Action

from Utils.angleutils import AngleUtils
from Utils.framedatautils import FrameDataUtils
from Utils.utils import Utils


class PlayerStateUtils:
    @staticmethod
    def get_position_after_drift(player_state, other_state, frames=1):
        trajectory = FrameDataUtils.create_trajectory_frames(player_state.character, player_state.speed_y_self)
        angle = PlayerStateUtils.get_knockback_angle(player_state, other_state)
        magnitude = PlayerStateUtils.get_knockback_magnitude(player_state, other_state)

        x_vel = abs(player_state.speed_air_x_self)
        x = player_state.position.x
        y = player_state.position.y

        for i in range(frames):
            drag = FrameDataUtils.INSTANCE.characterdata[player_state.character]["AirFriction"]

            frame = trajectory[min(i, len(trajectory) - 1)]

            x_vel += min(frame.forward_acceleration, max(frame.max_horizontal_velocity - x_vel, -drag))
            magnitude = max(magnitude - 0.051, 0)

            x += -Utils.sign(x) * x_vel #+ math.cos(math.radians(angle)) * magnitude
            y += frame.vertical_velocity #+ math.sin(math.radians(angle)) * magnitude

        return x, y

    @staticmethod
    def get_remaining_knockback(player_state=None, other_state=None, angle=None, magnitude=None):
        if angle is None:
            angle = PlayerStateUtils.get_knockback_angle(player_state, other_state)
        if magnitude is None:
            magnitude = PlayerStateUtils.get_knockback_magnitude(player_state, other_state)

        x = 0
        y = 0

        while magnitude > 0:
            magnitude = max(magnitude - 0.051, 0)
            x += math.cos(math.radians(angle)) * magnitude
            y += math.sin(math.radians(angle)) * magnitude

        return x, y

    @staticmethod
    def get_position_after_hit_stun(player_state, other_state, stage_edge, angle=None, magnitude=None):
        if angle is None:
            angle = PlayerStateUtils.get_knockback_angle(player_state, other_state)
        if magnitude is None:
            magnitude = PlayerStateUtils.get_knockback_magnitude(player_state, other_state)

        frames = PlayerStateUtils.get_hit_stun_frames(player_state, other_state)
        character_data = FrameDataUtils.INSTANCE.characterdata[player_state.character]
        y_vel = player_state.speed_y_self

        x = player_state.position.x
        y = player_state.position.y
        highest_y = y

        for i in range(frames):
            actual_y_vel = y_vel + magnitude * math.sin(math.radians(angle))
            x += magnitude * math.cos(math.radians(angle))
            y += actual_y_vel
            highest_y = max(y, highest_y)

            # If we are going to hit the stage, just say we landed there
            if highest_y > 0 and abs(x) < stage_edge and y < 0 and actual_y_vel < 0:
                break

            y_vel = max(y_vel - character_data["Gravity"], -character_data["TerminalVelocity"])
            magnitude = max(magnitude - 0.051, 0)

        return x, y

    @staticmethod
    def get_knockback_danger(smashbot_state, opponent_state, stage_edge, knockback_angle):
        position = PlayerStateUtils.get_position_after_hit_stun(smashbot_state, opponent_state, stage_edge, knockback_angle)
        x = abs(position[0]) - stage_edge
        y = position[1]
        angle = math.atan2(y, x)
        magnitude = math.sqrt(x ** 2 + y ** 2)
        return magnitude * math.cos(angle + math.radians(45))

    @staticmethod
    def get_knockback_angle(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to retrieve data stored externally
        if PlayerStateUtils.is_being_thrown(player_state):
            return FrameDataUtils.get_attack_angle(other_state)
        return AngleUtils.refit_angle(math.degrees(math.atan2(player_state.speed_y_attack, player_state.speed_x_attack)))

    @staticmethod
    def get_knockback_magnitude(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to retrieve data stored externally
        if PlayerStateUtils.is_being_thrown(player_state):
            return FrameDataUtils.get_attack_magnitude(player_state, other_state)
        return math.sqrt(player_state.speed_x_attack ** 2 + player_state.speed_y_attack ** 2)

    @staticmethod
    def get_hit_stun_frames(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to calculate manually
        if PlayerStateUtils.is_being_thrown(player_state):
            return round(PlayerStateUtils.get_knockback_magnitude(player_state, other_state) * 40 / 3)
        return player_state.hitstun_frames_left

    @staticmethod
    def is_bouncing(player_state, other_state):
        return player_state.hitstun_frames_left >= 32 and player_state.hitlag_left > 0 and \
               player_state.hitstun_frames_left / PlayerStateUtils.get_knockback_magnitude(player_state, other_state) > 14

    @staticmethod
    def is_being_thrown(player_state):
        return Action.THROWN_FORWARD.value <= player_state.action.value <= Action.THROWN_DOWN_2.value

    @staticmethod
    def is_flying_in_hit_stun(player_state):
        return Action.DAMAGE_HIGH_1.value <= player_state.action.value <= Action.DAMAGE_FLY_ROLL.value

    @staticmethod
    def get_inward_x(player_state):
        return int(player_state.position.x < 0)

    @staticmethod
    def get_outward_x(player_state):
        return 1 - PlayerStateUtils.get_inward_x(player_state)

    @staticmethod
    def is_facing_inwards(player_state):
        facing_inwards = player_state.facing == (player_state.position.x < 0)
        if player_state.action == Action.TURNING and player_state.action_frame == 1:
            facing_inwards = not facing_inwards

        return facing_inwards

    @staticmethod
    def is_grabbed(player_state):
        return player_state.action in [Action.GRABBED, Action.GRAB_PUMMELED, Action.GRAB_PULL,
                                       Action.GRAB_PUMMELED, Action.GRAB_PULLING_HIGH, Action.GRABBED_WAIT_HIGH,
                                       Action.PUMMELED_HIGH]

    @staticmethod
    def is_wall_teching(player_state):
        return Action.WALL_TECH.value <= player_state.action.value <= Action.WALL_TECH_JUMP.value

    @staticmethod
    def is_teching(player_state):
        return Action.NEUTRAL_TECH.value <= player_state.action.value <= Action.BACKWARD_TECH.value
