from Chains.chain import Chain


class Nothing(Chain):
    def step_internal(self, propagate):
        return False
