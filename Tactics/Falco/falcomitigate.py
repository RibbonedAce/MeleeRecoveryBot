from Chains.Falco import FireBird
from Tactics.Abstract import AbstractMitigate


class FalcoMitigate(AbstractMitigate):
    @classmethod
    def _get_meteor_cancel_class(cls):
        return FireBird