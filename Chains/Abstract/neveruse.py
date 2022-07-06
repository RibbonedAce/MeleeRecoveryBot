from abc import ABCMeta

from Chains.chain import Chain


class NeverUse(Chain, metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
        return False