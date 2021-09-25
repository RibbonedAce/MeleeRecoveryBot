import melee
from melee.enums import Action

from Chains import Nothing
from Tactics.tactic import Tactic
from Utils.framedatautils import FrameDataUtils


class Wait(Tactic):
    @staticmethod
    def should_use(propagate):
        game_state = propagate[0]
        smashbot_state = propagate[1]
        opponent_state = propagate[2]

        # Make an exception for shine states, since we're still actionable for them
        if smashbot_state.action in [Action.DOWN_B_GROUND_START, Action.DOWN_B_GROUND, Action.DOWN_B_STUN]:
            return False

        # If we're in the cooldown for an attack, just do nothing.
        if FrameDataUtils.INSTANCE.attack_state(smashbot_state.character, smashbot_state.action,
                                                smashbot_state.action_frame) == melee.enums.AttackState.COOLDOWN:
            return True

        # When teetering on the edge, make sure there isn't an opponent pushing on us.
        # We'll fall if we try to act
        opponent_pushing = (game_state.distance < 8) and abs(smashbot_state.position.x) > abs(opponent_state.position.x)
        if smashbot_state.action == Action.EDGE_TEETERING_START and opponent_pushing:
            return True

        if smashbot_state.action in [Action.THROW_UP, Action.THROW_DOWN, Action.THROW_FORWARD, Action.THROW_BACK]:
            return True

        if smashbot_state.action in [Action.UPTILT, Action.UPSMASH]:
            return True

        if smashbot_state.action in [Action.BACKWARD_TECH, Action.NEUTRAL_TECH, Action.FORWARD_TECH,
                                     Action.TECH_MISS_UP, Action.EDGE_GETUP_QUICK, Action.EDGE_GETUP_SLOW,
                                     Action.EDGE_ROLL_QUICK, Action.EDGE_ROLL_SLOW, Action.SHIELD_STUN,
                                     Action.TECH_MISS_DOWN, Action.LANDING_SPECIAL]:
            return True

        if smashbot_state.action == Action.LANDING and smashbot_state.action_frame <= 3:
            return True

        return False

    def step_internal(self, game_state, smashbot_state, opponent_state):
        self.pick_chain(Nothing)
