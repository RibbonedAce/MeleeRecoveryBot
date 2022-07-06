from melee.enums import Character

from Tactics import CaptainFalcon, Falco, Fox
from Tactics.Abstract import AbstractMitigate
from Tactics.tactic import Tactic


class Mitigate(Tactic):
    CLASS_DICTIONARY = {Character.CPTFALCON: CaptainFalcon.CaptainFalconMitigate,
                        Character.FOX: Fox.FoxMitigate,
                        Character.FALCO: Falco.FalcoMitigate}

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

    def step_internal(self, game_state, smashbot_state, opponent_state):
        if not self.initialized:
            self.initialized = True
            clazz = self.CLASS_DICTIONARY.get(smashbot_state.character)
            if clazz is not None:
                self.instance = clazz(self.controller, self.difficulty)

        if self.instance is None:
            return

        self.instance.step(game_state, smashbot_state, opponent_state)
        self.chain = self.instance.chain