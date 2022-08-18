import math
from abc import ABCMeta
from typing import Type

from melee import FrameData
from melee.enums import Action

from Chains import AirDodge, Chain, DriftIn, DriftOut, EdgeDash, FastFall, JumpInward, JumpOutward
from Chains.Abstract import RecoveryChain
from difficultysettings import DifficultySettings
from Tactics.tactic import Tactic
from Utils import Trajectory
from Utils.enums import RECOVERY_HEIGHT, RECOVERY_MODE


class AbstractRecover(Tactic, metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
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

    @classmethod
    def _get_primary_recovery_class(cls) -> Type[RecoveryChain]: ...

    @classmethod
    def _get_secondary_recovery_class(cls) -> Type[RecoveryChain]: ...

    @classmethod
    def _get_stall_class(cls) -> Type[Chain]: ...

    @classmethod
    def _get_primary_recovery_trajectory(cls, smashbot_state, stage_edge):
        return cls._get_primary_recovery_class().create_trajectory(smashbot_state, smashbot_state.get_inward_x_velocity())

    @classmethod
    def _get_secondary_recovery_trajectory(cls, smashbot_state):
        return cls._get_secondary_recovery_class().create_trajectory(smashbot_state, smashbot_state.get_inward_x_velocity())

    @classmethod
    def _can_hold_drift(cls, game_state, smashbot_state, opponent_state, target):
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
        if self.recovery_target.ledge and DriftIn.should_use(self._propagate) and self._can_hold_drift(game_state, smashbot_state, opponent_state, target):
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # Air dodge
        air_dodge_distance = AirDodge.create_trajectory(smashbot_state, smashbot_state.character, 90).get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.ledge, 0)
        if AirDodge.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.AIR_DODGE and \
                (smashbot_state.is_facing_inwards() or not self.recovery_target.ledge) and air_dodge_distance > 0:
            self.chain = None
            self.pick_chain(AirDodge, [target, self.recovery_target])
            return

        # Secondary recovery
        secondary_recovery_class = self._get_secondary_recovery_class()
        secondary_recovery_distance = self._get_secondary_recovery_trajectory(smashbot_state).get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.ledge, 0)
        if secondary_recovery_class.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.SECONDARY and secondary_recovery_distance > 0:
            self.chain = None
            self.pick_chain(secondary_recovery_class, [target, self.recovery_target])
            return

        # If we cannot air dodge or secondary recovery when we want to, primary recovery ASAP
        if smashbot_state.speed_y_self < 0 and smashbot_state.jumps_left == 0 and \
                (self.recovery_mode == RECOVERY_MODE.SECONDARY and secondary_recovery_distance == Trajectory.TOO_LOW_RESULT or
                 self.recovery_mode == RECOVERY_MODE.AIR_DODGE and air_dodge_distance == Trajectory.TOO_LOW_RESULT):
            self.time_to_recover = True

        # If we are wall teching, primary recovery ASAP
        wall_teching = smashbot_state.is_wall_teching()
        if wall_teching:
            self.time_to_recover = True

        # Decide how we can primary recovery
        if not self.time_to_recover and smashbot_state.jumps_left == 0 and smashbot_state.speed_y_self < 0:
            # Recover ASAP
            primary_recovery_trajectory = self._get_primary_recovery_trajectory(smashbot_state, stage_edge)
            if self.recovery_target.height == RECOVERY_HEIGHT.MAX and self.recovery_mode == RECOVERY_MODE.PRIMARY:
                distance_left = max(primary_recovery_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, False, 0),
                                    primary_recovery_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, True, 0))
                if distance_left <= self.last_distance or distance_left > 0:
                    self.time_to_recover = True
            # Recover at the ledge or stage
            else:
                distance_left = primary_recovery_trajectory.get_extra_distance(game_state, smashbot_state, opponent_state, target, self.recovery_target.height == RECOVERY_HEIGHT.LEDGE, 1)
                if distance_left <= self.last_distance and distance_left <= 0:
                    self.time_to_recover = True

            self.last_distance = distance_left

        double_jump_height = -(FrameData.INSTANCE.dj_height(smashbot_state)) + FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character)
        if self.recovery_target.height == RECOVERY_HEIGHT.LEDGE:
            double_jump_height -= FrameData.INSTANCE.get_ledge_box_top(smashbot_state.character)

        # If we are near a horizontal blast-zone, jump to prevent dying
        # Or if we are low enough
        # Or if we are trying to recover ASAP
        if (self.recovery_target.height == RECOVERY_HEIGHT.MAX or
                 smashbot_state.position.y < double_jump_height or
                 smashbot_state.position.x - game_state.get_left_blast_zone() < 20 or
                 game_state.get_right_blast_zone() - smashbot_state.position.x < 20):

            # Jump outward if past ledge
            if JumpOutward.should_use(self._propagate):
                self.pick_chain(JumpOutward)
                return

            if JumpInward.should_use(self._propagate):
                self.pick_chain(JumpInward)
                return

        # Recover when we're ready
        primary_recovery_class = self._get_primary_recovery_class()
        if primary_recovery_class.should_use(self._propagate) and \
                (smashbot_state.speed_y_self <= 0 or wall_teching) and self.time_to_recover:
            self.chain = None
            self.pick_chain(primary_recovery_class, [target, self.recovery_target])
            return

        # If we can do a Falcon Kick to get back easier, then do so
        stall_class = self._get_stall_class()
        if stall_class.should_use(self._propagate):
            self.pick_chain(stall_class)
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
