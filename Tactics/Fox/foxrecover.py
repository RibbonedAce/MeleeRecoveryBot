from Chains.Abstract import NeverUse
from Chains.Fox import FireFox, FoxIllusion
from Tactics.Abstract import AbstractRecover


class FoxRecover(AbstractRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return FireFox

    @classmethod
    def _get_secondary_recovery_class(cls):
        return FoxIllusion

    @classmethod
    def _get_stall_class(cls):
        return NeverUse