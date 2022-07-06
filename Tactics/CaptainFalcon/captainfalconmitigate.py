from Chains.CaptainFalcon import FalconDive
from Tactics.Abstract import AbstractMitigate


class CaptainFalconMitigate(AbstractMitigate):
    @classmethod
    def _get_meteor_cancel_class(cls):
        return FalconDive
