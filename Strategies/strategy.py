from abc import ABCMeta


class Strategy:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.controller = None
        self.difficulty = None
        self.tactic = None
        self._propagate = None

    def pick_tactic(self, tactic):
        if type(self.tactic) != tactic:
            self.tactic = tactic(self.controller, self.difficulty)
        self.tactic.step(self._propagate[0], self._propagate[1], self._propagate[2])

    def step(self, game_state, smashbot_state, opponent_state): ...
