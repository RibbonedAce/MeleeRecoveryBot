from Chains.Abstract import NeverUse
from Chains.Fox import FireFox, FoxIllusion
from Tactics.Abstract import SpacieRecover


class FoxRecover(SpacieRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return FireFox

    @classmethod
    def _get_secondary_recovery_class(cls):
        return FoxIllusion

    @classmethod
    def _get_stall_class(cls):
        return NeverUse