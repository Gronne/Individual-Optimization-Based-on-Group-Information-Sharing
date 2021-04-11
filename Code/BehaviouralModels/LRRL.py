import random
import numpy as np
import math
from collections import deque
import time

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface



class IndiLRRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions): 
        super().__init__(goals, initial_game_state, feasible_actions)





class GroupLRRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)