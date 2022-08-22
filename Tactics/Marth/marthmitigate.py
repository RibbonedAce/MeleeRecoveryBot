from Chains.Marth import DolphinSlash
from Tactics.Abstract import AbstractMitigate


class MarthMitigate(AbstractMitigate):
    @classmethod
    def _get_meteor_cancel_class(cls):
        return DolphinSlash