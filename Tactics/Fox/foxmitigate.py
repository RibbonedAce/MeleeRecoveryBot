from Chains.Fox import FireFox
from Tactics.Abstract import AbstractMitigate


class FoxMitigate(AbstractMitigate):
    @classmethod
    def _get_meteor_cancel_class(cls):
        return FireFox