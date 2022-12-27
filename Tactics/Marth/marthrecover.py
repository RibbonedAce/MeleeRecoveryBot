from Chains.Marth import DancingBlade, DolphinSlash
from Tactics.Abstract import AbstractRecover


class MarthRecover(AbstractRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return DolphinSlash

    @classmethod
    def _get_secondary_recovery_class(cls):
        return DolphinSlash

    @classmethod
    def _get_stall_class(cls):
        return DancingBlade