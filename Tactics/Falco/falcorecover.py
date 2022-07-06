from Chains.Abstract import NeverUse
from Chains.Falco import FalcoPhantasm, FireBird
from Tactics.Abstract import SpacieRecover


class FalcoRecover(SpacieRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return FireBird

    @classmethod
    def _get_secondary_recovery_class(cls):
        return FalcoPhantasm

    @classmethod
    def _get_stall_class(cls):
        return NeverUse