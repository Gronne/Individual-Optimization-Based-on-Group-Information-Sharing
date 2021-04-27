import random
import os
import numpy as NP
from Simulations.GameFeatures import GameFeatures as GF

class BehaviouralModelInterface:
    def __init__(self, goals, initial_game_state, feasible_actions, result_addr): 
        self._goals = goals
        self._initial_game_state = initial_game_state
        self._feasible_actions = feasible_actions
        self._coordinate_history = []

        self._result_addr = result_addr
        self._create_directory(self._result_addr)

    def _create_directory(self, addr):
        try:
            directory = ''.join(folder + "/" for folder in addr.split('/')[:-1])
            os.makedirs(directory)
        except FileExistsError:
            pass

    def action(self, game_state):     #game_state = [survival_time, health, points, coordinate, map_colors]
        score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        nr_of_actions = len(self._feasible_actions)
        index = random.randint(0, nr_of_actions-1)
        return self._feasible_actions[index]

    def _calculate_score(self, survival_time, resources, coordinate):
        score = 0
        if GF.GoalSystem.Time in self._goals:
            score += survival_time * 0.1
        if GF.GoalSystem.Resources in self._goals:
            score += resources * 1
        if GF.GoalSystem.Safety in self._goals:
            score += (1 / self._coordinate_variance(coordinate, 10)) * 0.1
        if score == 0: score = 0.00001
        normalized_score = 1 - (1/score)
        if normalized_score < 0:
            normalized_score = 0
        return score

    def _coordinate_variance(self, new_coor, filter_size):
        self._add_coor_to_history(new_coor, filter_size)
        mean = NP.mean(self._coordinate_history, axis=0)
        dist_to_mean = [NP.linalg.norm(mean-coor) for coor in self._coordinate_history]
        nr_of_coors = len(self._coordinate_history)
        deviations = [dist**2 for dist in dist_to_mean]
        variance = sum(deviations) / nr_of_coors
        if variance == 0:
            variance = 0.01
        return variance

    def _add_coor_to_history(self, new_coor, filter_size):
        if len(self._coordinate_history) < filter_size:
            self._coordinate_history += [[new_coor[0], new_coor[1]]]
        else:
            self._coordinate_history = self._coordinate_history[1:] + [[new_coor[0], new_coor[1]]]

    def save_model(self):
        raise Exception("save_model() must be implemented.")

    def save_result(self, survival_time, points, epsilon):
        with open(self._result_addr + ".txt", "a+") as file:
            file.write(f"SurvivalTime:{survival_time},Points:{points},Epsilon:{epsilon}\n")

    def _get_file_size(self, file_addr):
        try:
            size = os.stat(file_addr).st_size
        except:
            size = 0
        return size
















#Nothing
