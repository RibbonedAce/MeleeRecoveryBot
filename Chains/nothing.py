from Chains.chain import Chain


class Nothing(Chain):
    def step_internal(self, game_state, smashbot_state, opponent_state):
        return False
