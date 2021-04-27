import random
import numpy as np
import math
from collections import deque
import time
import os

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface



class IndiQLRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._model_addr = model_addr
        self._create_directory(self._model_addr)

        if self._get_file_size(self._model_addr + ".txt"):
            #Load
            self._qTable, self._epsilon = self._load_model()
        else:
            #Create
            self._qTable = {}
            self._epsilon = 1

        self._previous_state = None
        self._previous_action = None
        self._previous_score = 0

        self._learning_rate = 0.1
        self._discount = 0.95

        self._epsilon_decay = 0.9995    #0.99975 before
        self._episodes = 6000
        self._episode_epsilon = self._epsilon_decay**self._episodes

        if self._epsilon < self._episode_epsilon:
            self._epsilon = 0

        self._turn_count = 0

    def get_epsilon(self):
        return self._epsilon

    def _load_model(self):
        print("#####LOAD MODEL#####")
        epsilon = None
        qTable = {}
        with open(self._model_addr + ".txt") as model_file:
            for line in model_file:
                line_split = line.split(";")
                if len(line_split) == 2:
                    key, actions_str = line_split
                    actions = [float(action_str) for action_str in actions_str.split(":")]
                    qTable[key] = actions
                elif len(line_split) == 1:
                    epsilon = 0.62025#float(line_split[0])
                else:
                    print("WUT!?!?!?!?!")
        return qTable, epsilon

    def save_model(self):
        with open(self._model_addr + ".txt", "w") as file:
            for key in self._qTable:
                actions_str = ''.join(str(action) + ":" for action in self._qTable[key])[:-1]
                file.write(key + ";" + actions_str + "\n")
            file.write(str(self._epsilon))
            
        

    def action(self, game_state):
        self._turn_count += 1
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)
        if self._epsilon > self._episode_epsilon and self._epsilon != 0:
            if self._turn_count % 100 == 0:
                print(f"steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
                if self._turn_count % 500 == 0:
                    self._epsilon *= self._epsilon_decay
                    print(f"Epsilon: {self._epsilon}")
            if isinstance(self._previous_state, list):
                if game_state[0] == 0:
                    self._set_score_in_q_table(self._previous_state, -1, self._previous_action, model_state)
                else:
                    self._set_score_in_q_table(self._previous_state, score, self._previous_action, model_state)
        else:
            if self._turn_count % 100 == 0:
                print(f"steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
        action = self._calculate_action(model_state)
        self._previous_action = action
        return action

    def _game_to_model_state(self, game_state):
        player_coor = (game_state[3][0]/len(game_state[-1][0]), game_state[3][1]/len(game_state[-1]))
        player_life = math.ceil(game_state[1]/20)/int(100/20)
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [player_life, player_coor, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _calculate_action(self, current_state):
        prediction = self._get_actions_from_q_table(current_state)
        action_index = self._choose_action_from_prediction(prediction, self._epsilon)
        self._previous_state = current_state
        return self._feasible_actions[action_index]

    def _choose_action_from_prediction(self, prediction, epsilon):
        index = np.argmax(prediction)
        if np.random.random() < epsilon:
            index = np.random.randint(0, len(prediction))
        return index

    def _model_in_q_table(self, model_state):
        return self._get_model_state_str(model_state) in self._qTable

    def _get_model_state_str(self, model_state):
        first_layer = [value for value in model_state[2].flatten()]
        second_layer = [value for value in model_state[3].flatten()]
        third_layer = [value for value in model_state[4].flatten()]
        return str(model_state[0])+","+str(model_state[1])+","+str(first_layer)+","+str(second_layer)+","+str(third_layer)
    
    def _add_state_to_q_table(self, model_state):
        self._qTable[self._get_model_state_str(model_state)] = np.random.uniform(low=-1, high=1, size=len(self._feasible_actions))

    def _get_actions_from_q_table(self, model_state):
        if not self._model_in_q_table(model_state):
            self._add_state_to_q_table(model_state)
        return self._qTable[self._get_model_state_str(model_state)]
    
    def _set_score_in_q_table(self, current_state, score, action, future_state):
        current_prediction = self._get_actions_from_q_table(current_state)
        current_index = action
        
        future_prediction = self._get_actions_from_q_table(future_state)
        future_index = self._choose_action_from_prediction(future_prediction, 0)

        current_q = current_prediction[current_index] 
        max_future_q = future_prediction[future_index] 

        new_q = (1-self._learning_rate) * current_q + self._learning_rate * (score + self._discount * max_future_q)

        current_prediction[current_index] = new_q

    def _same_layers(self, current_state, future_state):
        return (current_state[2] == future_state[2]).all() and (current_state[3] == future_state[3]).all() and (current_state[4] == future_state[4]).all()





class GroupQLRL(BehaviouralModelInterface):
    _qTable = {}

    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._create_directory(self._model_addr)
        self._previous_state = None
        self._previous_score = 0

        self._learning_rate = 0.1
        self._discount = 0.95

        self._epsilon = 1
        self._epsilon_decay = 0.9995  
        self._turn_count = 0

    def action(self, game_state):
        self._turn_count += 1
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)
        if self._turn_count % 100 == 0:
            print(f"steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
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
        return str(model_state) in GroupQLRL._qTable
    
    def _add_state_to_q_table(self, model_state):
        GroupQLRL._qTable[str(model_state)] = np.random.uniform(low=-1, high=1, size=len(self._feasible_actions))

    def _get_actions_from_q_table(self, model_state):
        if not self._model_in_q_table(model_state):
            self._add_state_to_q_table(model_state)
        return GroupQLRL._qTable[str(model_state)]
    
    def _set_score_in_q_table(self, current_state, score, future_state):
        current_prediction = self._get_actions_from_q_table(current_state)
        current_index = self._choose_action_from_prediction(current_prediction)
        
        future_prediction = self._get_actions_from_q_table(future_state)
        future_index = self._choose_action_from_prediction(future_prediction)

        current_q = current_prediction[current_index] 
        max_future_q = future_prediction[future_index] 

        new_q = (1-self._learning_rate) * current_q + self._learning_rate * (score + self._discount * max_future_q)

        current_prediction[current_index] = new_q