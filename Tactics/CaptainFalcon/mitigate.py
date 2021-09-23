from melee.enums import Action

import Chains
from Chains.CaptainFalcon import FalconDive
from Tactics.tactic import Tactic
from Utils.difficultysettings import DifficultySettings
from Utils.gamestateutils import GameStateUtils
from Utils.playerstateutils import PlayerStateUtils


class Mitigate(Tactic):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        # Grabbed, thrown, in hit-stun, or tumbling
        if PlayerStateUtils.is_grabbed(smashbot_state):
            return True

        # Thrown action
        if PlayerStateUtils.is_being_thrown(smashbot_state):
            return True

        # Damaged action
        if PlayerStateUtils.is_flying_in_hit_stun(smashbot_state):
            return True

        if smashbot_state.action == Action.TUMBLING:
            return True

        return False

    def __init__(self, logger, controller, difficulty):
        Tactic.__init__(self, logger, controller, difficulty)
        self.ledge_tech = DifficultySettings.should_ledge_tech()

    def step(self, game_state, smashbot_state, opponent_state):
        self._propagate = (game_state, smashbot_state, opponent_state)

        # If we can't interrupt the chain, just continue it
        if self.chain is not None and not self.chain.interruptable:
            self.chain.step(game_state, smashbot_state, opponent_state)
            return

        # Grab escape
        if Chains.Struggle.should_use(self._propagate):
            self.pick_chain(Chains.Struggle)
            return

        # Amsah tech
        if Chains.AmsahTech.should_use(self._propagate):
            self.pick_chain(Chains.AmsahTech)
            return

        # Ledge tech
        if Chains.LedgeTech.should_use(self._propagate) and self.ledge_tech:
            self.pick_chain(Chains.LedgeTech)
            return

        # Smash DI
        if Chains.SDI.should_use(self._propagate):
            self.pick_chain(Chains.SDI)
            return

        # Trajectory DI
        if Chains.TDI.should_use(self._propagate):
            self.pick_chain(Chains.TDI)
            return

        # Tech
        if Chains.Tech.should_use(self._propagate):
            self.pick_chain(Chains.Tech)
            return

        # Meteor cancel 8 frames after hit-lag ended
        if Chains.JumpInward.should_use(self._propagate) and \
                smashbot_state.speed_y_attack < 0 and smashbot_state.action_frame >= DifficultySettings.METEOR_CANCEL_FRAME and \
                smashbot_state.jumps_left > 0 and GameStateUtils.get_smashbot_custom(game_state, "meteor_jump_lockout") == 0:
            self.pick_chain(Chains.JumpInward)
            return

        # Meteor cancel 8 frames after hit-lag ended
        if Chains.CaptainFalcon.FalconDive.should_use(self._propagate) and \
                smashbot_state.speed_y_attack < 0 and smashbot_state.action_frame >= DifficultySettings.METEOR_CANCEL_FRAME and \
                GameStateUtils.get_smashbot_custom(game_state, "meteor_ff_lockout") == 0:
            self.pick_chain(Chains.CaptainFalcon.FalconDive)
            return

        if Chains.Wiggle.should_use(self._propagate):
            self.chain = None
            self.pick_chain(Chains.Wiggle)
            return

        # DI inward as a fallback
        if Chains.DriftIn.should_use(self._propagate):
            self.pick_chain(Chains.DriftIn)
            return
