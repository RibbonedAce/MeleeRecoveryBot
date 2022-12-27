from abc import ABCMeta


class Chain(metaclass=ABCMeta):
    @classmethod
    def should_use(cls, propagate):
        return True

    def __init__(self):
        self.interruptable = True
        self.controller = None
        self.difficulty = None

    def step_internal(self, propagate) -> bool: ...

    def step(self, propagate):
        decided = self.step_internal(propagate)

        # Fallback
        if not decided:
            self.interruptable = True
            self.controller.empty_input()
