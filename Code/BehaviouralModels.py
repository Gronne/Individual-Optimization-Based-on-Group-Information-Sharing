import random
import numpy as NP
from GameFeatures import GameFeatures as GF

class BehaviouralModelInterface:
    def __init__(self, goals):
        self._goals = goals
        self._coordinate_history = []

    def action(self, game_state, feasible_actions):     #game_state = [survival_time, health, points, coordinate, map_colors]
        score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        nr_of_actions = len(feasible_actions)
        index = random.randint(0, nr_of_actions-1)
        return feasible_actions[index]

    def _calculate_score(self, survival_time, resources, coordinate):
        score = 0
        if GF.GoalSystem.Time in self._goals:
            score += survival_time * 2
        if GF.GoalSystem.Resources in self._goals:
            score += resources * 10
        if GF.GoalSystem.Safety in self._goals:
            score += self._coordinate_variance(coordinate, 10) * 1
        return score

    def _coordinate_variance(self, new_coor, filter_size):
        self._add_coor_to_history(new_coor, filter_size)
        mean = NP.mean(self._coordinate_history, axis=0)
        dist_to_mean = [NP.linalg.norm(mean-coor) for coor in self._coordinate_history]
        nr_of_coors = len(self._coordinate_history)
        deviations = [dist**2 for dist in dist_to_mean]
        variance = sum(deviations) / nr_of_coors
        return variance

    def _add_coor_to_history(self, new_coor, filter_size):
        if len(self._coordinate_history) < filter_size:
            self._coordinate_history += [[new_coor[0], new_coor[1]]]
        else:
            self._coordinate_history = self._coordinate_history[1:] + [[new_coor[0], new_coor[1]]]