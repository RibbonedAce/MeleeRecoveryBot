import math

from melee import Action, FrameData, PlayerState

from Utils.angleutils import AngleUtils
from Utils.mathutils import MathUtils
from Utils.trajectory import Trajectory


class PlayerStateExtensions:
    @staticmethod
    def init_extensions():
        PlayerState.get_position_after_drift = PlayerStateExtensions.__get_position_after_drift
        PlayerState.get_remaining_knockback = PlayerStateExtensions.__get_remaining_knockback
        PlayerState.get_position_after_hit_stun = PlayerStateExtensions.__get_position_after_hit_stun
        PlayerState.get_knockback_danger = PlayerStateExtensions.__get_knockback_danger
        PlayerState.get_knockback_angle = PlayerStateExtensions.__get_knockback_angle
        PlayerState.get_knockback_magnitude = PlayerStateExtensions.__get_knockback_magnitude
        PlayerState.get_hit_stun_frames = PlayerStateExtensions.__get_hit_stun_frames
        PlayerState.get_duration_stuck = PlayerStateExtensions.__get_duration_stuck
        PlayerState.get_attack = PlayerStateExtensions.__get_attack
        PlayerState.get_attack_angle = PlayerStateExtensions.__get_attack_angle
        PlayerState.get_attack_magnitude = PlayerStateExtensions.__get_attack_magnitude
        PlayerState.is_bouncing = PlayerStateExtensions.__is_bouncing
        PlayerState.is_being_thrown = PlayerStateExtensions.__is_being_thrown
        PlayerState.is_flying_in_hit_stun = PlayerStateExtensions.__is_flying_in_hit_stun
        PlayerState.get_inward_x = PlayerStateExtensions.__get_inward_x
        PlayerState.get_outward_x = PlayerStateExtensions.__get_outward_x
        PlayerState.is_facing_inwards = PlayerStateExtensions.__is_facing_inwards
        PlayerState.is_grabbed = PlayerStateExtensions.__is_grabbed
        PlayerState.is_wall_teching = PlayerStateExtensions.__is_wall_teching
        PlayerState.is_teching = PlayerStateExtensions.__is_teching
    
    @staticmethod
    def __get_position_after_drift(player_state, other_state, frames=1):
        trajectory = Trajectory.create_drift_trajectory(player_state.character, player_state.speed_y_self)
        angle = player_state.get_knockback_angle(other_state)
        magnitude = player_state.get_knockback_magnitude(other_state)

        x_vel = abs(player_state.speed_air_x_self)
        x = player_state.position.x
        y = player_state.position.y

        for i in range(frames):
            drag = FrameData.INSTANCE.get_air_friction(player_state.character)

            frame = trajectory[min(i, len(trajectory) - 1)]

            x_vel += min(frame.forward_acceleration, max(frame.max_horizontal_velocity - x_vel, -drag))
            magnitude = max(magnitude - 0.051, 0)

            x += -MathUtils.sign(x) * x_vel + math.cos(math.radians(angle)) * magnitude
            y += frame.vertical_velocity + math.sin(math.radians(angle)) * magnitude

        return x, y

    @staticmethod
    def __get_remaining_knockback(player_state, other_state, angle=None, magnitude=None):
        if angle is None:
            angle = player_state.get_knockback_angle(other_state)
        if magnitude is None:
            magnitude = player_state.get_knockback_magnitude(other_state)

        x = 0
        y = 0

        while magnitude > 0:
            magnitude = max(magnitude - 0.051, 0)
            x += math.cos(math.radians(angle)) * magnitude
            y += math.sin(math.radians(angle)) * magnitude

        return x, y

    @staticmethod
    def __get_position_after_hit_stun(player_state, other_state, stage_edge, angle=None, magnitude=None):
        if angle is None:
            angle = player_state.get_knockback_angle(other_state)
        if magnitude is None:
            magnitude = player_state.get_knockback_magnitude(other_state)

        frames = player_state.get_hit_stun_frames(other_state)
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

            y_vel = max(y_vel - FrameData.INSTANCE.get_gravity(player_state.character), -FrameData.INSTANCE.get_terminal_velocity(player_state.character))
            magnitude = max(magnitude - 0.051, 0)

        return x, y

    @staticmethod
    def __get_knockback_danger(player_state, other_state, stage_edge, knockback_angle):
        position = player_state.get_position_after_hit_stun(other_state, stage_edge, knockback_angle)
        x = abs(position[0]) - stage_edge
        y = position[1]
        angle = math.atan2(y, x)
        magnitude = math.sqrt(x ** 2 + y ** 2)
        return magnitude * math.cos(angle + math.radians(45))

    @staticmethod
    def __get_knockback_angle(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to retrieve data stored externally
        if player_state.is_being_thrown():
            return other_state.get_attack_angle()
        return AngleUtils.refit_angle(math.degrees(math.atan2(player_state.speed_y_attack, player_state.speed_x_attack)))

    @staticmethod
    def __get_knockback_magnitude(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to retrieve data stored externally
        if player_state.is_being_thrown():
            return player_state.get_attack_magnitude(other_state)
        return math.sqrt(player_state.speed_x_attack ** 2 + player_state.speed_y_attack ** 2)

    @staticmethod
    def __get_hit_stun_frames(player_state, other_state):
        # We don't have time to calculate throw knockback as throws have no hit-lag,
        # so need to calculate manually
        if player_state.is_being_thrown():
            return round(player_state.get_knockback_magnitude(other_state) * 40 / 3)
        return player_state.hitstun_frames_left

    @staticmethod
    def __is_bouncing(player_state, other_state):
        return player_state.hitstun_frames_left >= 32 and player_state.hitlag_left > 0 and \
               player_state.hitstun_frames_left / player_state.get_knockback_magnitude(other_state) > 14

    @staticmethod
    def __is_being_thrown(player_state):
        return Action.THROWN_FORWARD.value <= player_state.action.value <= Action.THROWN_DOWN_2.value

    @staticmethod
    def __is_flying_in_hit_stun(player_state):
        return Action.DAMAGE_HIGH_1.value <= player_state.action.value <= Action.DAMAGE_FLY_ROLL.value

    @staticmethod
    def __get_inward_x(player_state):
        return int(player_state.position.x < 0)

    @staticmethod
    def __get_outward_x(player_state):
        return 1 - player_state.get_inward_x()

    @staticmethod
    def __is_facing_inwards(player_state):
        facing_inwards = player_state.facing == (player_state.position.x < 0)
        if player_state.action == Action.TURNING and player_state.action_frame == 1:
            facing_inwards = not facing_inwards

        return facing_inwards

    @staticmethod
    def __is_grabbed(player_state):
        return player_state.action in [Action.GRABBED, Action.GRAB_PUMMELED, Action.GRAB_PULL, Action.GRAB_PUMMELED,
                                       Action.GRAB_PULLING_HIGH, Action.GRABBED_WAIT_HIGH, Action.PUMMELED_HIGH]

    @staticmethod
    def __is_wall_teching(player_state):
        return Action.WALL_TECH.value <= player_state.action.value <= Action.WALL_TECH_JUMP.value

    @staticmethod
    def __is_teching(player_state):
        return Action.NEUTRAL_TECH.value <= player_state.action.value <= Action.BACKWARD_TECH.value

    @staticmethod
    def __get_hit_lag_duration(player_state, damage):
        d = math.floor(damage)
        e = 1

        attack = player_state.get_attack()
        # Electric attack hit-stun multiplier
        if attack is not None and attack["Effect"] == "Electric":
            e = 1.5

        return (d / 3 + 3) * e

    @staticmethod
    def __get_duration_stuck(player_state):
        attack = player_state.get_attack()
        # Don't assume anything if we can't figure out the attack
        if attack is None:
            return 0

        # If opponent is falling when using an aerial attack, assume that they will land the next frame
        landing_lag = attack["Landing Lag"]
        if landing_lag > 0 and player_state.speed_y_self < 0:
            return landing_lag

        # If it's a grounded move or a rising aerial, assume they will go through all of it
        return attack["IASA"] - player_state.action_frame

    @staticmethod
    def __get_attack(player_state):
        for attack in FrameData.ATTACK_DATA[player_state.character][player_state.action]:
            if player_state.action_frame >= attack[0]:
                return attack[1]
        return None

    @staticmethod
    def __get_attack_magnitude(player_state, other_state):
        attack = other_state.get_attack()
        # If attack not configured, then return a "moderately powerful" attack
        if attack is None:
            return 3

        p = player_state.percent
        d = attack["Damage"]
        w = FrameData.INSTANCE.get_weight(player_state.character)
        s = attack["KB Growth"]
        b = attack["Base KB"]

        # Set knockback moves
        if attack["Set KB"] != 0:
            p = 10
            d = attack["Set KB"]

        # Weight-independent moves (e.g. throws)
        if not attack["Weight Dependent"]:
            w = 100

        return (((((p / 10 + p * d / 20) * 200 / (w + 100) * 1.4) + 18) * s / 100) + b) * 0.03

    @staticmethod
    def __get_attack_angle(player_state):
        attack = player_state.get_attack()
        # If attack not configured, then return 45 degrees
        angle = 45
        if attack is not None:
            angle = attack["Angle"]
        if not player_state.facing:
            angle = AngleUtils.get_x_reflection(angle)

        return angle
