from abc import ABCMeta


class Chain(metaclass=ABCMeta):
    @staticmethod
    def should_use(propagate):
        return True

    def __init__(self):
        self.interruptable = True
        self.controller = None
        self.difficulty = None

    def step_internal(self, game_state, smashbot_state, opponent_state) -> bool: ...

    def step(self, game_state, smashbot_state, opponent_state):
        decided = self.step_internal(game_state, smashbot_state, opponent_state)

        # Fallback
        if not decided:
            self.interruptable = True
            self.controller.empty_input()
