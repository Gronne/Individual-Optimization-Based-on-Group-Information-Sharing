import random
import numpy as np
import math
from collections import deque
import time

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface



class IndiQLRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions): 
        super().__init__(goals, initial_game_state, feasible_actions)
        self._qTable = {}
        self._previous_state = None
        self._previous_score = 0

        self._learning_rate = 0.1
        self._discount = 0.95

        self._epsilon = 1
        self._epsilon_decay = 0.9975    #0.99975 before

        self._turn_count = 0

    def action(self, game_state):
        self._turn_count += 1
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)
        if self._turn_count % 100 == 0:
            print(f"life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
            self._epsilon *= self._epsilon_decay
            print(f"Epsilon: {self._epsilon}")
        if isinstance(self._previous_state, list):
            if game_state[0] != 0:
                self._set_score_in_q_table(self._previous_state, -1, model_state)
            else:
                self._set_score_in_q_table(self._previous_state, score, model_state)
        action = self._calculate_action(model_state)
        return action

    def _game_to_model_state(self, game_state):
        player_coor = (game_state[3][0]/len(game_state[-1]), game_state[3][1]/len(game_state[-1][0]))
        player_life = math.ceil(game_state[1]/20)/int(100/20)
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [player_life, player_coor, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _calculate_action(self, current_state):
        prediction = self._get_actions_from_q_table(current_state)
        action_index = self._choose_action_from_prediction(prediction)
        self._previous_state = current_state
        return self._feasible_actions[action_index]

    def _choose_action_from_prediction(self, prediction):
        index = np.argmax(prediction)
        if np.random.random() <= self._epsilon:
            index = np.random.randint(0, len(prediction))
        return index

    def _model_in_q_table(self, model_state):
        return str(model_state) in self._qTable
    
    def _add_state_to_q_table(self, model_state):
        self._qTable[str(model_state)] = np.random.uniform(low=-1, high=1, size=len(self._feasible_actions))

    def _get_actions_from_q_table(self, model_state):
        if not self._model_in_q_table(model_state):
            self._add_state_to_q_table(model_state)
        return self._qTable[str(model_state)]
    
    def _set_score_in_q_table(self, current_state, score, future_state):
        current_prediction = self._get_actions_from_q_table(current_state)
        current_index = self._choose_action_from_prediction(current_prediction)
        
        future_prediction = self._get_actions_from_q_table(future_state)
        future_index = self._choose_action_from_prediction(future_prediction)

        current_q = current_prediction[current_index] 
        max_future_q = future_prediction[future_index] 

        new_q = (1-self._learning_rate) * current_q + self._learning_rate * (score + self._discount * max_future_q)

        current_prediction[current_index] = new_q





class GroupQLRL(BehaviouralModelInterface):
    _qTable = {}
    _learning_rate = 0.1
    _discount = 0.95

    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)
        self._previous_state = None
        self._previous_score = 0

    def action(self, game_state):
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)
        if game_state[0] % 10 == 0:
            print(f"life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
        if isinstance(self._previous_state, list):
            if game_state[0] != 0:
                self._set_score_in_q_table(self._previous_state, -1, model_state)
            else:
                self._set_score_in_q_table(self._previous_state, score, model_state)
        action = self._calculate_action(model_state)
        return action

    def _game_to_model_state(self, game_state):
        player_coor = (game_state[3][0]/len(game_state[-1]), game_state[3][1]/len(game_state[-1][0]))
        player_life = math.ceil(game_state[1]/20)
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [player_life, player_coor, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _calculate_action(self, current_state):
        prediction = self._get_actions_from_q_table(current_state)
        action_index = self._choose_action_from_prediction(prediction)
        self._previous_state = current_state
        return self._feasible_actions[action_index]

    def _choose_action_from_prediction(self, prediction):
        return np.argmax(prediction)

    def _model_in_q_table(self, model_state):
        return str(model_state) in _qTable
    
    def _add_state_to_q_table(self, model_state):
        _qTable[str(model_state)] = np.random.uniform(low=-1, high=1, size=len(_feasible_actions))

    def _get_actions_from_q_table(self, model_state):
        if not self._model_in_q_table(model_state):
            self._add_state_to_q_table(model_state)
        return _qTable[str(model_state)]
    
    def _set_score_in_q_table(self, current_state, score, future_state):
        current_prediction = self._get_actions_from_q_table(current_state)
        current_index = self._choose_action_from_prediction(current_prediction)
        
        future_prediction = self._get_actions_from_q_table(future_state)
        future_index = self._choose_action_from_prediction(future_prediction)

        current_q = current_prediction[current_index] 
        max_future_q = future_prediction[future_index] 

        new_q = (1-_learning_rate) * current_q + _learning_rate * (score + _discount * max_future_q)

        current_prediction[current_index] = new_q