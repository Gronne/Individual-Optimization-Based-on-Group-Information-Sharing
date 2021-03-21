import random

class BehaviouralModelInterface:
    def __init__(self, goals):
        self._goals = goals

    def action(self, game_state, feasible_actions): #game_state = [health, points, coordinate, map_colors]
        #print("  Health: " + str(game_state[0]) + " - Points: " + str(game_state[1]))
        nr_of_actions = len(feasible_actions)
        index = random.randint(0, nr_of_actions-1)
        return feasible_actions[index]