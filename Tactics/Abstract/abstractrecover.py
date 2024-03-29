from abc import ABCMeta
from collections import defaultdict
from typing import Type

import ctrajectory
from melee import FrameData
from melee.enums import Action

from Chains import AirDodge, DriftIn, DriftOut, EdgeDash, FastFall, JumpInward, JumpOutward
from Chains.Abstract import NeverUse, RecoveryChain, StallChain
from difficultysettings import DifficultySettings
from Tactics.tactic import Tactic
from Utils import FrameInput, LogUtils, Trajectory, Vector2
from Utils.enums import RECOVERY_HEIGHT, RECOVERY_MODE


class AbstractRecover(Tactic, metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        on_edge = smashbot_state.action in {Action.EDGE_HANGING, Action.EDGE_CATCHING}
        opponent_on_edge = opponent_state.action in {Action.EDGE_HANGING, Action.EDGE_CATCHING, Action.EDGE_GETUP_SLOW,
                                                     Action.EDGE_GETUP_QUICK, Action.EDGE_ATTACK_SLOW,
                                                     Action.EDGE_ATTACK_QUICK, Action.EDGE_ROLL_SLOW,
                                                     Action.EDGE_ROLL_QUICK}

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
        if opponent_state.action in {Action.DEAD_DOWN, Action.DEAD_RIGHT, Action.DEAD_LEFT,
                                     Action.DEAD_FLY, Action.DEAD_FLY_STAR, Action.DEAD_FLY_SPLATTER}:
            return True

        # If opponent is on stage
        if not opponent_state.off_stage:
            return True

        # If opponent is in hit-stun, then recover, unless we're on the edge.
        if opponent_state.off_stage and opponent_state.hitstun_frames_left > 0 and not on_edge:
            return True

        if opponent_state.action == Action.DEAD_FALL and opponent_state.position.y < -30:
            return True

        stage_edge = Vector2(game_state.get_stage_edge(), 0)
        # If opponent is closer to the edge, recover
        opponent_dist = (opponent_state.get_relative_position() - stage_edge).get_magnitude()
        smashbot_dist = (smashbot_state.get_relative_position() - stage_edge).get_magnitude()

        if opponent_dist < smashbot_dist and not on_edge:
            return True

        if smashbot_dist >= 20:
            return True

        # If we're both fully off-stage, recover
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
    def _get_stall_class(cls) -> Type[StallChain]: ...

    @classmethod
    def _get_primary_recovery_trajectory(cls, smashbot_state):
        return cls._get_primary_recovery_class().create_trajectory(smashbot_state.character)

    @classmethod
    def _get_secondary_recovery_trajectory(cls, smashbot_state):
        return cls._get_secondary_recovery_class().create_trajectory(smashbot_state.character)

    @classmethod
    def _get_primary_recovery_inputs(cls, smashbot_state, game_state):
        return cls._get_primary_recovery_class().create_default_inputs(smashbot_state, game_state)

    @classmethod
    def _can_hold_drift(cls, propagate, target, ledge):
        smashbot_state = propagate[1]
        trajectory = Trajectory.create_drift_trajectory(smashbot_state.character)
        return trajectory.get_extra_distance(propagate, target=target, ledge=ledge) > 0

    def __init__(self, controller, difficulty):
        Tactic.__init__(self, controller, difficulty)
        self.time_to_recover = False
        self.recovery_mode = DifficultySettings.get_recovery_mode()
        self.recovery_target = DifficultySettings.get_recovery_target()
        self.should_hold_drift = DifficultySettings.should_hold_drift()
        self.last_early_distance = Trajectory.TOO_LOW_RESULT

    def step_internal(self, propagate):
        self._propagate = propagate
        game_state = propagate[0]
        smashbot_state = propagate[1]

        if EdgeDash.should_use(self._propagate):
            self.pick_chain(EdgeDash)
            return

        # If we're in dead max fall, just drift towards the stage
        if DriftIn.should_use(self._propagate) and smashbot_state.action == Action.DEAD_FALL:
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # If we can make it with a fast-fall, do so
        if FastFall.should_use(self._propagate):
            self.pick_chain(FastFall)
            return

        target = Vector2(game_state.get_stage_edge(), 0)

        # If we can recover without using any more moves, then just hold in
        if self.should_hold_drift and DriftIn.should_use(self._propagate) and \
                self._can_hold_drift(propagate, target, self.recovery_target.ledge):
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # Air dodge
        air_dodge_inputs = defaultdict(FrameInput.forward)
        air_dodge_inputs[0] = FrameInput.direct(Vector2(0, 1))
        air_dodge_distance = AirDodge.create_trajectory(smashbot_state.character).get_extra_distance(propagate, target=target, ledge=self.recovery_target.ledge, input_frames=air_dodge_inputs)
        if AirDodge.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.AIR_DODGE and \
                (smashbot_state.is_facing_inwards() or not self.recovery_target.ledge) and air_dodge_distance > 0:
            self.chain = None
            self.pick_chain(AirDodge, (target, self.recovery_target))
            return

        # Perform secondary recovery
        secondary_recovery_class = self._get_secondary_recovery_class()
        secondary_recovery_distance = self._get_secondary_recovery_trajectory(smashbot_state).get_extra_distance(propagate, target=target, ledge=self.recovery_target.ledge)
        if secondary_recovery_class.should_use(self._propagate) and self.recovery_mode == RECOVERY_MODE.SECONDARY and secondary_recovery_distance > 0:
            self.chain = None
            self.pick_chain(secondary_recovery_class, (target, self.recovery_target))
            return

        # If we cannot air dodge or perform secondary recovery when we want to, perform primary recovery instead
        if smashbot_state.speed_y_self < 0 and smashbot_state.jumps_left == 0 and \
                (self.recovery_mode == RECOVERY_MODE.SECONDARY and secondary_recovery_distance == Trajectory.TOO_LOW_RESULT or
                 self.recovery_mode == RECOVERY_MODE.AIR_DODGE and air_dodge_distance == Trajectory.TOO_LOW_RESULT):
            self.recovery_mode = RECOVERY_MODE.PRIMARY

        # If we are wall teching, perform primary recovery ASAP
        wall_teching = smashbot_state.is_wall_teching()
        if wall_teching:
            self.time_to_recover = True

        # Decide how we can perform primary recovery
        if not self.time_to_recover and smashbot_state.jumps_left == 0 and smashbot_state.speed_y_self < 0:
            primary_recovery_trajectory = self._get_primary_recovery_trajectory(smashbot_state)
            drift_trajectory = Trajectory.create_drift_trajectory(smashbot_state.character)

            max_descent_stage = target.y - primary_recovery_trajectory.stall_height
            max_descent_ledge = max_descent_stage - FrameData.INSTANCE.get_ledge_box(smashbot_state.character).top
            if primary_recovery_trajectory.requires_extra_height:
                max_descent_ledge += 2

            stall_class = self._get_stall_class()
            if stall_class is NeverUse:
                trajectory = None
                weak_trajectory = None
                double_jumps_gained = 0
                min_stall_speed = 999
            else:
                trajectory = stall_class.create_trajectory(True).nickname
                weak_trajectory = stall_class.create_trajectory(False).nickname
                double_jumps_gained = stall_class.double_jumps_gained()
                min_stall_speed = stall_class.min_stall_speed(smashbot_state.character)

            descent_data = ctrajectory.get_descent_data(trajectory, weak_trajectory, drift_trajectory.nickname, max_descent_stage, max_descent_ledge, smashbot_state.get_relative_position(), smashbot_state.get_relative_velocity(), smashbot_state.stall_is_charged(game_state), double_jumps_gained, FrameData.INSTANCE.get_dj_speed(smashbot_state.character), min_stall_speed)
            stage_new_position, stage_new_velocity, stage_frames = descent_data[max_descent_stage]
            ledge_new_position, ledge_new_velocity, ledge_frames = descent_data[max_descent_ledge]
            if self.recovery_target.ledge:
                new_position, new_velocity, num_frames = ledge_new_position, ledge_new_velocity, ledge_frames
            else:
                new_position, new_velocity, num_frames = stage_new_position, stage_new_velocity, stage_frames

            inputs = self._get_primary_recovery_inputs(smashbot_state, game_state)
            early_distance = primary_recovery_trajectory.get_extra_distance(self._propagate, target=target, ledge=self.recovery_target.ledge, input_frames=inputs, ignore_stage_vertex=True)
            late_distance = primary_recovery_trajectory.get_extra_distance(self._propagate, target=target, ledge=self.recovery_target.ledge, position=Vector2(new_position[0], new_position[1]), velocity=Vector2(new_velocity[0], new_velocity[1]), input_frames=inputs, ignore_stage_vertex=True)
            ledge_distance = primary_recovery_trajectory.get_extra_distance(self._propagate, target=target, ledge=True, position=Vector2(ledge_new_position[0], ledge_new_position[1]), velocity=Vector2(ledge_new_velocity[0], ledge_new_velocity[1]), input_frames=inputs, ignore_stage_vertex=True)
            max_distance = max(early_distance, late_distance, ledge_distance)

            LogUtils.simple_log("Descent frames:", descent_data, early_distance, late_distance)
            # Recover ASAP
            if self.recovery_target.height == RECOVERY_HEIGHT.MAX and self.recovery_mode == RECOVERY_MODE.PRIMARY:
                if self.last_early_distance >= early_distance >= late_distance or early_distance > 0:
                    self.time_to_recover = True
                self.last_early_distance = early_distance
            # Recover at the ledge or stage
            elif num_frames <= 0 or (ledge_frames <= 0 and max_distance < 0):
                self.time_to_recover = True

        double_jump_height = FrameData.INSTANCE.get_terminal_velocity(smashbot_state.character) - FrameData.INSTANCE.fast_dj_height(smashbot_state.character)
        if self.recovery_target.height == RECOVERY_HEIGHT.LEDGE:
            double_jump_height -= FrameData.INSTANCE.get_ledge_box(smashbot_state.character).top

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
            self.pick_chain(primary_recovery_class, (target, self.recovery_target))
            return

        # If we can stall to get back easier, then do so
        stall_class = self._get_stall_class()
        if stall_class.should_use(self._propagate):
            self.chain = None
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
