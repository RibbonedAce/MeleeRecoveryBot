from abc import ABCMeta

from melee import Action

from Chains.chain import Chain
from Utils import RecoveryTarget, Trajectory


class RecoveryChain(Chain, metaclass=ABCMeta):
    @classmethod
    def create_trajectory(cls, smashbot_state, x_velocity, angle=0) -> Trajectory: ...

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        return smashbot_state.action != Action.DEAD_FALL

    def __init__(self, target_coords=(0, 0), recovery_target=RecoveryTarget.max()):
        Chain.__init__(self)
        self.target_coords = target_coords
        self.recovery_target = recovery_target
        self.current_frame = -1
        self.trajectory = None