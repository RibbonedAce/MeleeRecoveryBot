from abc import ABCMeta
from typing import Type

from melee.enums import Action

from Chains import AmsahTech, DriftIn, JumpInward, LedgeTech, Nothing, SDI, Struggle, TDI, Tech, Wiggle
from Chains.Abstract import RecoveryChain
from difficultysettings import DifficultySettings
from Tactics.tactic import Tactic


class AbstractMitigate(Tactic, metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
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

    @classmethod
    def _get_meteor_cancel_class(cls) -> Type[RecoveryChain]: ...

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
        meteor_cancel_class = self._get_meteor_cancel_class()
        if meteor_cancel_class.should_use(self._propagate) and \
                smashbot_state.speed_y_attack < 0 and smashbot_state.action_frame >= DifficultySettings.METEOR_CANCEL_FRAME and \
                smashbot_state.can_special_meteor_cancel(game_state):
            self.pick_chain(meteor_cancel_class)
            return

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
