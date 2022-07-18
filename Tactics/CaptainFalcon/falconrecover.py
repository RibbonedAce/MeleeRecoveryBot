from Chains.CaptainFalcon import FalconDive, FalconKick, RaptorBoost
from Tactics.Abstract import AbstractRecover


class FalconRecover(AbstractRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return FalconDive

    @classmethod
    def _get_secondary_recovery_class(cls):
        return RaptorBoost

    @classmethod
    def _get_stall_class(cls):
        return FalconKick