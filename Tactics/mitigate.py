from melee.enums import Character

from Tactics import CaptainFalcon, Fox
from Tactics.tactic import Tactic


class Mitigate(Tactic):
    CLASS_DICTIONARY = {Character.CPTFALCON: CaptainFalcon.Mitigate,
                        Character.FOX: Fox.Mitigate}

    @staticmethod
    def should_use(propagate):
        smashbot_state = propagate[1]

        clazz = Mitigate.CLASS_DICTIONARY.get(smashbot_state.character)
        if clazz is None:
            return False

        return clazz.should_use(propagate)

    def __init__(self, logger, controller, difficulty):
        Tactic.__init__(self, logger, controller, difficulty)
        self.initialized = False
        self.instance = None

    def step_internal(self, game_state, smashbot_state, opponent_state):
        if not self.initialized:
            self.initialized = True
            clazz = Mitigate.CLASS_DICTIONARY.get(smashbot_state.character)
            if clazz is not None:
                self.instance = clazz(self.logger, self.controller, self.difficulty)

        if self.instance is None:
            return

        self.instance.step(game_state, smashbot_state, opponent_state)
        self.chain = self.instance.chain