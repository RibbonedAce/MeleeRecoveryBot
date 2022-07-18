from Chains.Ganondorf import DarkDive, GerudoDragon, WizardsFoot
from Tactics.Abstract import AbstractRecover


class GanondorfRecover(AbstractRecover):
    @classmethod
    def _get_primary_recovery_class(cls):
        return DarkDive

    @classmethod
    def _get_secondary_recovery_class(cls):
        return GerudoDragon

    @classmethod
    def _get_stall_class(cls):
        return WizardsFoot