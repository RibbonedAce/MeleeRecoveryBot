from melee.enums import Action

from Chains.amsahtech import AmsahTech
from Chains.driftin import DriftIn
from Chains.jumpinward import JumpInward
from Chains.ledgetech import LedgeTech
from Chains.nothing import Nothing
from Chains.sdi import SDI
from Chains.struggle import Struggle
from Chains.tdi import TDI
from Chains.tech import Tech
from Chains.wiggle import Wiggle
from difficultysettings import DifficultySettings
from Tactics.tactic import Tactic


class Mitigate(Tactic):
    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        # Grabbed
        if smashbot_state.is_grabbed():
            return True

        # Thrown action
        if smashbot_state.is_being_thrown():
            return True

        # Damaged action
        if smashbot_state.is_suffering_damage():
            return True

        # Need to wiggle out
        if smashbot_state.is_flying_in_hit_stun() or smashbot_state.action == Action.TUMBLING:
            return True

        return False

    def __init__(self, controller, difficulty):
        Tactic.__init__(self, controller, difficulty)
        self.ledge_tech = DifficultySettings.should_ledge_tech()

    def step(self, game_state, smashbot_state, opponent_state):
        self._propagate = (game_state, smashbot_state, opponent_state)

        # If we can't interrupt the chain, just continue it
        if self.chain is not None and not self.chain.interruptable:
            self.chain.step(game_state, smashbot_state, opponent_state)
            return

        # Grab escape
        if Struggle.should_use(self._propagate):
            self.pick_chain(Struggle)
            return

        # Amsah tech
        if AmsahTech.should_use(self._propagate):
            self.pick_chain(AmsahTech)
            return

        # Ledge tech
        if LedgeTech.should_use(self._propagate) and self.ledge_tech:
            self.pick_chain(LedgeTech)
            return

        # Smash DI
        if SDI.should_use(self._propagate):
            self.pick_chain(SDI)
            return

        # Trajectory DI
        if TDI.should_use(self._propagate):
            self.pick_chain(TDI)
            return

        # Tech
        if Tech.should_use(self._propagate):
            self.pick_chain(Tech)
            return

        # Meteor cancel 8 frames after hit-lag ended
        if JumpInward.should_use(self._propagate) and \
                smashbot_state.speed_y_attack < 0 and smashbot_state.action_frame >= DifficultySettings.METEOR_CANCEL_FRAME and \
                smashbot_state.jumps_left > 0 and smashbot_state.can_jump_meteor_cancel(game_state):
            self.pick_chain(JumpInward)
            return

        # Meteor cancel 8 frames after hit-lag ended
        # if FalconDive.should_use(self._propagate) and \
        #         smashbot_state.speed_y_attack < 0 and smashbot_state.action_frame >= DifficultySettings.METEOR_CANCEL_FRAME and \
        #         smashbot_state.can_special_meteor_cancel(game_state):
        #     self.pick_chain(FalconDive)
        #     return

        if Wiggle.should_use(self._propagate):
            self.chain = None
            self.pick_chain(Wiggle)
            return

        # DI inward as aerial fallback
        if DriftIn.should_use(self._propagate):
            self.pick_chain(DriftIn)
            return

        # DI inward as grounded fallback
        self.pick_chain(Nothing)
