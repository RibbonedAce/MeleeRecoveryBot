from melee.enums import Character

from Tactics.Abstract import AbstractMitigate
from Tactics.CaptainFalcon import FalconMitigate
from Tactics.Falco import FalcoMitigate
from Tactics.Fox import FoxMitigate
from Tactics.Ganondorf import GanondorfMitigate
from Tactics.Marth import MarthMitigate
from Tactics.tactic import Tactic


class Mitigate(Tactic):
    CLASS_DICTIONARY = {Character.CPTFALCON: FalconMitigate,
                        Character.FOX: FoxMitigate,
                        Character.FALCO: FalcoMitigate,
                        Character.GANONDORF: GanondorfMitigate,
                        Character.MARTH: MarthMitigate}

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        clazz = cls.CLASS_DICTIONARY.get(smashbot_state.character)
        if clazz is None:
            return AbstractMitigate.should_use(propagate)

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