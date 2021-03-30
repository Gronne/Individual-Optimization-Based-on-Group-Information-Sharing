import random
import numpy as NP
from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface



class GenericReinforcementLearning(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions): 
        super().__init__(goals, initial_game_state, feasible_actions)





class SwarmReinforcementLearning(BehaviouralModelInterface):    #Or myabe "Distributed deep reinforcement learning"?
    def __init__(self, goals, initial_game_state, feasible_actions): 
        super().__init__(goals, initial_game_state, feasible_actions)
