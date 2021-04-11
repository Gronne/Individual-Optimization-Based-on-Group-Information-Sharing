from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface
from BehaviouralModels.DRL import GroupDRL
from BehaviouralModels.QLRL import GroupQLRL
from BehaviouralModels.LRRL import GroupLRRL
from BehaviouralModels.GRL import GroupGRL


class DeepReinforcementLearning(GroupDRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)

    
class QLearning(GroupQLRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)


class RegressionLearning(GroupLRRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)


class GenericLearning(GroupGRL):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)

