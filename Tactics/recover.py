from melee.enums import Character

from Tactics import CaptainFalcon, Falco, Fox
from Tactics.Abstract import AbstractRecover
from Tactics.tactic import Tactic


class Recover(Tactic):
    CLASS_DICTIONARY = {Character.CPTFALCON: CaptainFalcon.CaptainFalconRecover,
                        Character.FOX: Fox.FoxRecover,
                        Character.FALCO: Falco.FalcoRecover}

    @classmethod
    def should_use(cls, propagate):
        smashbot_state = propagate[1]

        clazz = cls.CLASS_DICTIONARY.get(smashbot_state.character)
        if clazz is None:
            return AbstractRecover.should_use(propagate)

        return clazz.should_use(propagate)

    def __init__(self, controller, difficulty):
        Tactic.__init__(self, controller, difficulty)
        self.__initialized = False
        self.__instance = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        if not self.__initialized:
            self.__initialized = True
            clazz = self.CLASS_DICTIONARY.get(smashbot_state.character)
            if clazz is not None:
                self.__instance = clazz(self.controller, self.difficulty)

        if self.__instance is None:
            return

        self.__instance.step(game_state, smashbot_state, opponent_state)
        self.chain = self.__instance.chain
