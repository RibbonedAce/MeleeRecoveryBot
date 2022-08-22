from Chains.Abstract import NeverUse
from Chains.Marth import DancingBlade, DolphinSlash
from Tactics.Abstract import SpacieRecover


class MarthRecover(SpacieRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return DolphinSlash

    @classmethod
    def _get_secondary_recovery_class(cls):
        return NeverUse

    @classmethod
    def _get_stall_class(cls):
        return DancingBlade