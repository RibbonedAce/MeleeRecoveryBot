from Strategies.strategy import Strategy
from Tactics.mitigate import Mitigate
from Tactics.recover import Recover
from Tactics.wait import Wait


class OnlyRecover(Strategy):
    def __init__(self, controller, difficulty):
        super().__init__()
        self.approach = False
        self.approach_frame = -123
        self.controller = controller
        self.set_difficulty = difficulty
        self.difficulty = 4

    def __str__(self):
        string = "Bait"

        if not self.tactic:
            return string
        string += str(type(self.tactic))

        if not self.tactic.chain:
            return string
        string += str(type(self.tactic.chain))
        return string

    def step(self, game_state, smashbot_state, opponent_state):
        self._propagate = (game_state, smashbot_state, opponent_state)

        if Mitigate.should_use(self._propagate):
            self.pick_tactic(Mitigate)
            return

        if self.tactic and not self.tactic.is_interruptable():
            self.tactic.step(game_state, smashbot_state, opponent_state)
            return

        # If we're stuck in a lag state, just do nothing. Trying an action might just
        #   buffer an input we don't want
        if Wait.should_use(self._propagate):
            self.pick_tactic(Wait)
            return

        if Recover.should_use(self._propagate):
            self.pick_tactic(Recover)
            return

        self.pick_tactic(Wait)
