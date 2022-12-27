from Strategies.strategy import Strategy
from Tactics import Mitigate, Recover, Wait


class OnlyRecover(Strategy):
    def __init__(self, controller, difficulty):
        super().__init__()
        self.approach = False
        self.approach_frame = -123
        self.controller = controller
        self.set_difficulty = difficulty
        self.difficulty = 4

    def step(self, propagate):
        self._propagate = propagate

        if Mitigate.should_use(self._propagate):
            self.pick_tactic(Mitigate)
            return

        if self.tactic and not self.tactic.is_interruptable():
            self.tactic.step(propagate)
            return

        # If we're stuck in a lag state, just do nothing. Trying an action might just
        #   buffer an input we don't want
        if Wait.should_use(self._propagate):
            self.pick_tactic(Wait)
            return

        # If we need to recover, do it
        if Recover.should_use(self._propagate):
            self.pick_tactic(Recover)
            return

        self.pick_tactic(Wait)

    def __str__(self):
        string = "OnlyRecover"

        if not self.tactic:
            return string
        string += str(type(self.tactic))

        if not self.tactic.chain:
            return string
        string += str(type(self.tactic.chain))
        return string
