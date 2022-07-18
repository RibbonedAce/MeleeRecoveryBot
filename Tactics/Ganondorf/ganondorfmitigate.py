from Chains.Ganondorf import DarkDive
from Tactics.Abstract import AbstractMitigate


class GanondorfMitigate(AbstractMitigate):
    @classmethod
    def _get_meteor_cancel_class(cls):
        return DarkDive
