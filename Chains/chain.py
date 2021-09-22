from abc import ABCMeta


class Chain(metaclass=ABCMeta):
    interruptable = True
    logger = None
    controller = None
    difficulty = None

    @staticmethod
    def should_use(propagate):
        return True

    def step_internal(self, game_state, smashbot_state, opponent_state) -> bool: ...

    def step(self, game_state, smashbot_state, opponent_state):
        decided = self.step_internal(game_state, smashbot_state, opponent_state)

        # Fallback
        if not decided:
            self.interruptable = True
            self.controller.empty_input()
