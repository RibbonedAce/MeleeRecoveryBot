from melee.enums import Character

from Tactics.Abstract import AbstractRecover
from Tactics.CaptainFalcon import FalconRecover
from Tactics.Falco import FalcoRecover
from Tactics.Fox import FoxRecover
from Tactics.Ganondorf import GanondorfRecover
from Tactics.Marth import MarthRecover
from Tactics.tactic import Tactic


class Recover(Tactic):
    CLASS_DICTIONARY = {Character.CPTFALCON: FalconRecover,
                        Character.FOX: FoxRecover,
                        Character.FALCO: FalcoRecover,
                        Character.GANONDORF: GanondorfRecover,
                        Character.MARTH: MarthRecover}

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        clazz = cls.CLASS_DICTIONARY.get(smashbot_state.character)
        if clazz is None:
            return AbstractRecover.should_use(propagate)

        return clazz.should_use(propagate)

    def __init__(self, controller, difficulty):
        Tactic.__init__(self, controller, difficulty)
        self.initialized = False
        self.instance = None

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        if not self.initialized:
            self.initialized = True
            clazz = self.CLASS_DICTIONARY.get(smashbot_state.character)
            if clazz is not None:
                self.instance = clazz(self.controller, self.difficulty)

        if self.instance is None:
            return

        self.instance.step(propagate)
        self.chain = self.instance.chain
