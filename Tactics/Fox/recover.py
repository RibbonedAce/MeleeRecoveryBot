import math

from melee import FrameData
from melee.enums import Action

from Chains.airdodge import AirDodge
from Chains.driftin import DriftIn
from Chains.driftout import DriftOut
from Chains.edgedash import EdgeDash
from Chains.fastfall import FastFall
from Chains.Fox.firefox import FireFox
from Chains.Fox.foxillusion import FoxIllusion
from Chains.jumpinward import JumpInward
from difficultysettings import DifficultySettings
from Tactics.tactic import Tactic
from Utils.angleutils import AngleUtils
from Utils.controlstick import ControlStick
from Utils.enums import RECOVERY_HEIGHT, RECOVERY_MODE
from Utils.trajectory import Trajectory


class Recover(Tactic):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        on_edge = smashbot_state.action in [Action.EDGE_HANGING, Action.EDGE_CATCHING]
        opponent_on_edge = opponent_state.action in [Action.EDGE_HANGING, Action.EDGE_CATCHING, Action.EDGE_GETUP_SLOW,
                                                     Action.EDGE_GETUP_QUICK, Action.EDGE_ATTACK_SLOW,
                                                     Action.EDGE_ATTACK_QUICK, Action.EDGE_ROLL_SLOW,
                                                     Action.EDGE_ROLL_QUICK]

        # If the opponent is on-stage, and we're on-edge, we need to ledge-dash
        if not opponent_state.off_stage and on_edge:
            return True

        # If we're on stage, then we don't need to recover
        if not smashbot_state.off_stage:
            return False

        if smashbot_state.on_ground:
            return False

        # We can now assume that we're off the stage...

        # If opponent is dead
        if opponent_state.action in [Action.DEAD_DOWN, Action.DEAD_RIGHT, Action.DEAD_LEFT,
                                     Action.DEAD_FLY, Action.DEAD_FLY_STAR, Action.DEAD_FLY_SPLATTER]:
            return True

        # If opponent is on stage
        if not opponent_state.off_stage:
            return True

        # If opponent is in hit-stun, then recover, unless we're on the edge.
        if opponent_state.off_stage and opponent_state.hitstun_frames_left > 0 and not on_edge:
            return True

        if opponent_state.action == Action.DEAD_FALL and opponent_state.position.y < -30:
            return True

        stage_edge = game_state.get_stage_edge()
        # If opponent is closer to the edge, recover
        diff_x_opponent = abs(stage_edge - abs(opponent_state.position.x))
        diff_x = abs(stage_edge - abs(smashbot_state.position.x))

        # Using (opponent_state.position.y + 15)**2 was causing a keep-distance/dash-dance bug.
        opponent_dist = math.sqrt(opponent_state.position.y ** 2 + diff_x_opponent ** 2)
        smashbot_dist = math.sqrt(smashbot_state.position.y ** 2 + diff_x ** 2)

        if opponent_dist < smashbot_dist and not on_edge:
            return True

        if smashbot_dist >= 20:
            return True

        # If we're both fully off stage, recover
        if opponent_state.off_stage and smashbot_state.off_stage and not on_edge and not opponent_on_edge:
            return True

        # If opponent is ON the edge, recover
        if opponent_on_edge and not on_edge:
            return True

        return False

    @staticmethod
    def __can_hold_drift(game_state, smashbot_state, opponent_state, target):
        trajectory = Trajectory.create_drift_trajectory(smashbot_state.character, smashbot_state.speed_y_self)
        distance = trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, False)
        if distance <= 0 and smashbot_state.is_facing_inwards():
            distance = trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, True)
        return distance > 0

    def __init__(self, controller, difficulty):
        Tactic.__init__(self, controller, difficulty)
        self.time_to_recover = False
        self.recovery_mode = DifficultySettings.get_recovery_mode()
        self.recovery_target = DifficultySettings.get_recovery_target()
        self.grab_ledge = DifficultySettings.should_grab_ledge()
        self.last_distance = Trajectory.TOO_LOW_RESULT

    def step_internal(self, game_state, smashbot_state, opponent_state):
        if EdgeDash.should_use(self._propagate):
            self.pick_chain(EdgeDash)
            return

        stage_edge = game_state.get_stage_edge()

        # If we're in dead max fall, just drift towards the stage
        if DriftIn.should_use(self._propagate) and smashbot_state.action == Action.DEAD_FALL:
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # If we can make it with a fast-fall, do so
        if FastFall.should_use(self._propagate):
            self.pick_chain(FastFall)
            return

        target = (stage_edge, 0)

        # If we are currently moving away from the stage, DI in
        if self.grab_ledge and DriftIn.should_use(self._propagate) and Recover.__can_hold_drift(game_state, smashbot_state, opponent_state, target):
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # Air dodge
        if AirDodge.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.AIR_DODGE and \
                (smashbot_state.is_facing_inwards() or not self.recovery_target.ledge) and \
                AirDodge.create_trajectory(smashbot_state.character, 90).get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.ledge, 0) > 0:
            self.chain = None
            self.pick_chain(AirDodge, [target, self.recovery_target])
            return

        # Fox Illusion
        if FoxIllusion.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.SECONDARY and \
                FoxIllusion.TRAJECTORY.get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.ledge, 0) > 0:
            self.chain = None
            self.pick_chain(FoxIllusion, [target, self.recovery_target])
            return

        # If we are wall teching, Fire Fox ASAP
        wall_teching = smashbot_state.is_wall_teching()
        if wall_teching:
            self.time_to_recover = True

        # Decide how we can Fire Fox
        if not self.time_to_recover and smashbot_state.jumps_left == 0 and smashbot_state.speed_y_self < 0:
            angle_to_ledge = AngleUtils.correct_for_cardinal(math.degrees(math.atan2(-smashbot_state.position.y, abs(smashbot_state.position.x) - stage_edge)))
            min_angle = ControlStick(ControlStick(0, ControlStick.DEAD_ZONE_ESCAPE).get_most_right_x(), ControlStick.DEAD_ZONE_ESCAPE).to_angle()
            test_angle = max(angle_to_ledge, min_angle)
            fire_fox_trajectory = FireFox.create_trajectory(abs(smashbot_state.speed_air_x_self), test_angle)

            # Recover ASAP
            if self.recovery_target.height == RECOVERY_HEIGHT.MAX and self.recovery_mode == RECOVERY_MODE.PRIMARY:
                distance_left = max(fire_fox_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, False, 0),
                                    fire_fox_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, True, 0))
                if distance_left > 0:
                    self.time_to_recover = True
            # Recover at the ledge or stage
            else:
                distance_left = fire_fox_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.ledge, 1)

            if distance_left <= self.last_distance and distance_left <= 0:
                self.time_to_recover = True
            self.last_distance = distance_left

        double_jump_height = -(FrameData.INSTANCE.dj_height(smashbot_state)) + FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character)
        if self.recovery_target.height == RECOVERY_HEIGHT.LEDGE:
            double_jump_height -= FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)

        # If we are near a horizontal blast-zone, jump to prevent dying
        # Or if we are low enough
        # Or if we are trying to recover ASAP
        if JumpInward.should_use(self._propagate) and \
                (self.recovery_target.height == RECOVERY_HEIGHT.MAX or
                 smashbot_state.position.y < double_jump_height or
                 smashbot_state.position.x - game_state.get_left_blast_zone() < 20 or
                 game_state.get_right_blast_zone() - smashbot_state.position.x < 20):
            self.pick_chain(JumpInward)
            return

        # Recover when we're ready
        if FireFox.should_use(self._propagate) and \
                (smashbot_state.speed_y_self <= 0 or wall_teching) and self.time_to_recover:
            self.chain = None
            self.pick_chain(FireFox, [target, self.recovery_target])
            return

        # Drift out from the stage if too far in
        if DriftOut.should_use(self._propagate):
            self.chain = None
            self.pick_chain(DriftOut)
            return

        # Drift into the stage
        if DriftIn.should_use(self._propagate):
            self.chain = None
            self.pick_chain(DriftIn)