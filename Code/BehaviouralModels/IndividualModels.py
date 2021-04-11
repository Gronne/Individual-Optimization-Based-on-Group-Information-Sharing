from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface
from BehaviouralModels.DRL import IndiDRL
from BehaviouralModels.QLRL import IndiQLRL
from BehaviouralModels.LRRL import IndiLRRL
from BehaviouralModels.GRL import IndiGRL


class DeepReinforcementLearning(IndiDRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)

    
class QLearning(IndiQLRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)


class RegressionLearning(IndiLRRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)


class GenericLearning(IndiGRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)

