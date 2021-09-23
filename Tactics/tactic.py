from abc import ABCMeta


class Tactic(metaclass=ABCMeta):
    chain = None

    @staticmethod
    def should_use(propagate):
        return False

    def __init__(self, logger, controller, difficulty):
        self.logger = logger
        self.controller = controller
        self.difficulty = difficulty
        self._propagate = None

    def pick_chain(self, chain, args=None):
        if args is None:
            args = []

        if type(self.chain) != chain:
            self.chain = chain(*args)
            self.chain.logger = self.logger
            self.chain.controller = self.controller
            self.chain.difficulty = self.difficulty

        # Do empty input to remove any potential inputs that other chains failed to clear
        self.chain.controller.empty_input()
        self.chain.step(self._propagate[0], self._propagate[1], self._propagate[2])

    def step_internal(self, game_state, smashbot_state, opponent_state) -> bool:
        ...

    def step(self, game_state, smashbot_state, opponent_state):
        self._propagate = (game_state, smashbot_state, opponent_state)

        # If we can't interrupt the chain, just continue it
        if self.chain is not None and not self.chain.interruptable:
            self.chain.step(game_state, smashbot_state, opponent_state)
            return

        self.step_internal(game_state, smashbot_state, opponent_state)

    def is_interruptable(self):
        if self.chain:
            return self.chain.interruptable
        else:
            return False
