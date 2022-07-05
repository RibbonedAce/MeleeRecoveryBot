import random

from Utils.mathutils import MathUtils


class HillClimb:
    def __init__(self, lower_bound, upper_bound, target_iterations):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.target_iterations = target_iterations

        self.iterations = 0
        self.best_result = None
        self.best_point = (lower_bound + upper_bound) / 2
        self.current_point = self.best_point

    def get_next_point(self):
        step_size = 0.5 * (self.upper_bound - self.lower_bound) * ((1 - self.iterations / self.target_iterations) ** 2)
        step = MathUtils.lerp(-step_size, step_size, random.random())
        self.current_point = min(max(self.lower_bound, self.best_point + step), self.upper_bound)
        self.iterations += 1
        return self.current_point

    def record_result(self, result):
        self.record_custom_result(result, self.current_point)

    def record_custom_result(self, result, custom_point):
        if self.best_result is None or result > self.best_result:
            self.override_best_result(result, custom_point)

    def override_best_result(self, result, custom_point):
        self.best_result = result
        self.best_point = custom_point