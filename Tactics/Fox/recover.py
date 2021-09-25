import math

import melee
from melee.enums import Action

from Chains import AirDodge, DriftIn, FastFall, EdgeDash, JumpInward
from Data import OtherStageData
from Tactics.tactic import Tactic
from Utils.difficultysettings import DifficultySettings
from Utils.enums import RECOVER_HEIGHT, RECOVER_MODE
from Utils.framedatautils import FrameDataUtils
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils
from Utils.utils import Utils


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

        # If the opponent is on-stage, and Smashbot is on-edge, Smashbot needs to ledge-dash
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

        stage_edge = GameStateUtils.get_stage_edge(game_state)
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
    def __can_hold_drift(smashbot_state, opponent_state, stage_edge):
        trajectory = FrameDataUtils.create_trajectory_frames(smashbot_state.character, smashbot_state.speed_y_self)
        angle = PlayerStateUtils.get_knockback_angle(smashbot_state, opponent_state)
        magnitude = PlayerStateUtils.get_knockback_magnitude(smashbot_state, opponent_state)

        x_vel = abs(smashbot_state.speed_air_x_self)
        x = abs(smashbot_state.position.x)
        y = smashbot_state.position.y

        for i in range(0, 300):
            drag = FrameDataUtils.INSTANCE.characterdata[smashbot_state.character]["AirFriction"]

            frame = trajectory[min(i, len(trajectory) - 1)]

            x_vel += min(frame.forward_acceleration, max(frame.max_horizontal_velocity - x_vel, -drag))
            magnitude = max(magnitude - 0.051, 0)

            true_x_vel = abs(math.cos(math.radians(angle)) * magnitude) - x_vel
            x += true_x_vel
            y_vel = frame.vertical_velocity + math.sin(math.radians(angle)) * magnitude
            y += y_vel

            if y_vel < 0 and y < -Utils.LEDGE_GRAB_AREA[1]:
                return False

            if y_vel < 0 and (x < stage_edge and y >= 0 and true_x_vel < 0 or
                              x < stage_edge + Utils.LEDGE_GRAB_AREA[0] and -Utils.LEDGE_GRAB_AREA[1] <= y <= -Utils.LEDGE_GRAB_AREA_HIGH[1]):
                return True

    def __init__(self, logger, controller, difficulty):
        Tactic.__init__(self, logger, controller, difficulty)
        self.time_to_recover = False
        self.recover_mode = DifficultySettings.get_recover_mode()
        self.recover_height = DifficultySettings.get_recover_height()
        self.ledge = self.recover_height == RECOVER_HEIGHT.LEDGE
        self.fade_back_mode = DifficultySettings.get_fade_back_mode()
        self.last_distance = -100

    def step_internal(self, game_state, smashbot_state, opponent_state):
        if EdgeDash.should_use(self._propagate):
            self.pick_chain(EdgeDash)
            return

        stage_edge = GameStateUtils.get_stage_edge(game_state)
        diff_x = abs(smashbot_state.position.x) - stage_edge

        # If we're in dead max fall, just drift towards the stage
        if DriftIn.should_use(self._propagate) and \
                smashbot_state.action == Action.DEAD_FALL:
            self.chain = None
            self.pick_chain(DriftIn)
            return

        # If we can make it with a fast-fall, do so
        if FastFall.should_use(self._propagate):
            self.pick_chain(FastFall)
            return

        # If we are currently moving away from the stage, DI in
        if DriftIn.should_use(self._propagate) and Recover.__can_hold_drift(smashbot_state, opponent_state, stage_edge):
            self.chain = None
            self.pick_chain(DriftIn)
            return

        target = (stage_edge, 0)
        if self.ledge:
            target = (stage_edge + Utils.LEDGE_GRAB_AREA[0], -Utils.LEDGE_GRAB_AREA[1])

        # Air dodge
        if AirDodge.should_use(self._propagate) and self.recover_mode == RECOVER_MODE.AIR_DODGE and \
                (PlayerStateUtils.is_facing_inwards(smashbot_state) or not self.ledge) and \
                AirDodge.create_trajectory(smashbot_state.character, 90).get_extra_distance(smashbot_state, opponent_state, target, self.ledge, 0) > 0:
            self.chain = None
            self.pick_chain(AirDodge, [target, self.fade_back_mode, self.ledge])
            return

        # Raptor Boost
        # if RaptorBoost.should_use(self._propagate) and self.recover_mode == RECOVER_MODE.SECONDARY and \
        #         RaptorBoost.TRAJECTORY.get_extra_distance(smashbot_state, opponent_state, target, self.ledge, 0) > 0:
        #     self.chain = None
        #     self.pick_chain(RaptorBoost, [target, self.fade_back_mode, self.ledge])
        #     return

        # If we are wall teching, Falcon Dive ASAP
        wall_teching = PlayerStateUtils.is_wall_teching(smashbot_state)
        if wall_teching:
            self.time_to_recover = True

        # # Decide how we can Falcon Dive
        # if not self.time_to_recover and smashbot_state.jumps_left == 0 and smashbot_state.speed_y_self < 0:
        #     # Recover ASAP
        #     if self.recover_height == RECOVER_HEIGHT.MAX:
        #         distance_left = max(FalconDive.TRAJECTORY.get_extra_distance(smashbot_state, opponent_state, target, False, 0),
        #                             FalconDive.TRAJECTORY.get_extra_distance(smashbot_state, opponent_state, target, True, 0))
        #         if distance_left > 0:
        #             distance_left = self.last_distance - 100
        #     # Recover at the ledge or stage
        #     else:
        #         distance_left = FalconDive.TRAJECTORY.get_extra_distance(smashbot_state, opponent_state, target, self.ledge, 1)
        #
        #     if distance_left <= self.last_distance and distance_left <= 0:
        #         self.time_to_recover = True
        #     self.last_distance = distance_left

        # If we are near a horizontal blast-zone, jump to prevent dying
        # Or if we are low enough
        # Or if we are trying to recover ASAP
        if JumpInward.should_use(self._propagate) and \
                (self.recover_height == RECOVER_HEIGHT.MAX or
                 smashbot_state.position.y < -43 or
                 smashbot_state.position.x - OtherStageData.get_left_blast_zone(game_state.stage) < 20 or
                 OtherStageData.get_right_blast_zone(game_state.stage) - smashbot_state.position.x < 20):
            self.pick_chain(JumpInward)
            return

        # # Recover when we're ready
        # if FalconDive.should_use(self._propagate) and \
        #         (smashbot_state.speed_y_self <= 0 or wall_teching) and self.time_to_recover:
        #     self.chain = None
        #     self.pick_chain(FalconDive, [target, self.fade_back_mode, self.ledge])
        #     return
        #
        # # If we can do a Falcon Kick to get back easier, then do so
        # if FalconKick.should_use(self._propagate):
        #     self.pick_chain(FalconKick)
        #     return

        # DI into the stage
        if DriftIn.should_use(self._propagate) and \
                not (diff_x < 13 and game_state.stage == melee.enums.Stage.BATTLEFIELD and smashbot_state.position.y < 0):
            self.chain = None
            self.pick_chain(DriftIn)