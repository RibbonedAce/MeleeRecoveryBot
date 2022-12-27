from abc import ABCMeta


class Tactic(metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
        return False

    def __init__(self, controller, difficulty):
        self.controller = controller
        self.difficulty = difficulty
        self.chain = None
        self._propagate = None

    def pick_chain(self, chain, args=None):
        if args is None:
            args = []

        if type(self.chain) != chain:
            self.chain = chain(*args)
            self.chain.controller = self.controller
            self.chain.difficulty = self.difficulty

        # Do empty input to remove any potential inputs that other chains failed to clear
        self.chain.controller.empty_input()
        self.chain.step(self._propagate)

    def step_internal(self, propagate): ...

    def step(self, propagate):
        self._propagate = propagate

        # If we can't interrupt the chain, just continue it
        if self.chain is not None and not self.chain.interruptable:
            self.chain.step(self._propagate)
            return

        self.step_internal(self._propagate)

    def is_interruptable(self):
        if self.chain:
            return self.chain.interruptable
        else:
            return False
