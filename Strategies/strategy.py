from abc import ABCMeta


class Strategy(metaclass=ABCMeta):
    def __init__(self):
        self.controller = None
        self.difficulty = None
        self.tactic = None
        self._propagate = None

    def pick_tactic(self, tactic):
        if type(self.tactic) != tactic:
            self.tactic = tactic(self.controller, self.difficulty)
        self.tactic.step(self._propagate)

    def step(self, propagate): ...
