import random
import numpy as np
import math
from collections import deque
import time

from sklearn.linear_model import LinearRegression

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface


MIN_REPLAY_MEMORY_SIZE = 16_384
MAX_REPLAY_MEMORY_SIZE = 16_384
MINIBATCH_SIZE = 16_384                 #Affect how many states it will use to fit

DISCOUNT = 0.99


class IndiLRRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._create_directory(self._model_addr)
        self._previous_action = None
        self._previous_state = None
        self._previous_game = None
        self._previous_score = 0
        self._turn_count = 0

        if self._get_file_size(self._model_addr + ".txt"):
            #Load
            self._regressions, self._epsilon = self._load_model()
        else:
            #Create
            #Setup regression - One for each action's score
            model_state = self._game_to_model_state(initial_game_state)
            rand_vals = np.random.uniform(low=-1, high=1, size=(len(feasible_actions)))
            self._regressions = LinearRegression().fit([model_state], [rand_vals])
            #Set epsilon
            self._epsilon = 1

        self._epsilon_decay = 0.9995    #0.99975 before
        self._terminal_count = 0
        #Setup memory for last N states
        self._replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)


    def get_epsilon(self):
        return self._epsilon

    def _load_model(self):
        print("#####LOAD MODEL#####")

    def save_model(self):
        coefficients = self._regressions.get_params()
        print(coefficients)

    def action(self, game_state):
        self._turn_count += 1
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)

        if self._turn_count % 100 == 0:
            if self._turn_count > MINIBATCH_SIZE and self._turn_count % 500 == 0:
                self._epsilon *= self._epsilon_decay
                print(f"Epsilon: {self._epsilon}")
            print(f"steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")

        if isinstance(self._previous_state, np.ndarray):
            terminal_state = game_state[0] == 0 or model_state[0] != self._previous_state[0] or game_state[2] != self._previous_game[2] #If dead, different health, or different points
            self._terminal_count += 1 if terminal_state else 0
            self._update_replay_memory((self._previous_state, model_state, self._previous_action, score, game_state[0] == 0, terminal_state))    
            self._train(terminal_state , game_state[0])
            
        action = self._calculate_action([model_state])
        self._previous_action = action
        self._previous_state = model_state
        self._previous_game = game_state
        return action

    def _game_to_model_state(self, game_state):
        player_coor = (game_state[3][0]/len(game_state[-1]), game_state[3][1]/len(game_state[-1][0]))
        player_life = game_state[1]/100
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([ np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return np.concatenate((np.array([player_life, player_coor[0], player_coor[1]]).flatten(), np_model_state_map.flatten()))

    def _update_replay_memory(self, transition):
        self._replay_memory.append(transition)

    def _calculate_action(self, model_state):
        prediction = self._predict(model_state)[0]
        action_index = self._choose_action_from_prediction(prediction)
        return self._feasible_actions[action_index]

    def _predict(self, model_state):
        predictions = self._regressions.predict(model_state)
        return predictions

    def _choose_action_from_prediction(self, prediction):
        index = np.argmax(prediction)
        if np.random.random() <= self._epsilon:
            index = np.random.randint(0, len(prediction))
        return index

    def _train(self, terminal_state, step):
        if len(self._replay_memory) < MIN_REPLAY_MEMORY_SIZE or self._terminal_count % 50 != 0 or not terminal_state:
            return
        print(f"Training at step: {self._turn_count}")
        minibatch = self._replay_memory

        current_states = self._get_state_in_prediction_structure(minibatch, 0)
        current_q_list = np.array(self._predict(current_states))

        new_current_states = self._get_state_in_prediction_structure(minibatch, 1)
        future_q_list = np.array(self._predict(new_current_states))
        
        X = []
        y = []

        for index, (current_state, new_current_state, action, reward, done, life_changer) in enumerate(minibatch):
            if done:
                new_q = -10  #reward
            elif life_changer:
                new_q = reward
            else:
                max_future_q = np.max(future_q_list[index])
                new_q = reward + DISCOUNT * max_future_q

            result = current_q_list[index]
            result[action] = new_q

            X += [current_state]
            y += [result]
        
        self._regressions.fit(X, y)


    def _get_state_in_prediction_structure(self, minibatch, data_index):
        current_states = np.array([transition[data_index] for transition in minibatch])
        return current_states
        








class GroupLRRL(BehaviouralModelInterface):
    _replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)
    _global_training_count = 0
    _global_instances = 0
    _regressions = None
    _epsilon = 1
    _epsilon_decay = 0.9995    #0.99975 before

    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._create_directory(self._model_addr)
        self._previous_action = None
        self._previous_state = None
        self._previous_game = None
        self._previous_score = 0
        self._turn_count = 0

        self._terminal_count = 0

        GroupLRRL._global_instances += 1

        #One for prediction each action's score
        if _regression == None:
            model_state = self._game_to_model_state(initial_game_state)
            rand_vals = np.random.uniform(low=-1, high=1, size=(len(feasible_actions)))
            GroupLRRL._regressions = LinearRegression().fit([model_state], [rand_vals])


    def action(self, game_state):
        self._turn_count += 1
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)

        if self._turn_count % 100 == 0:
            print(f"steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}")
            print(f"Epsilon: {GroupLRRL._epsilon}")

        if isinstance(self._previous_state, np.ndarray):
            terminal_state = game_state[0] == 0 or model_state[0] != self._previous_state[0] or game_state[2] != self._previous_game[2] #If dead, different health, or different points
            self._terminal_count += 1 if terminal_state else 0
            self._update_replay_memory((self._previous_state, model_state, self._previous_action, score, game_state[0] == 0, terminal_state))    
            self._train(terminal_state , game_state[0])
            
        action = self._calculate_action([model_state])
        self._previous_action = action
        self._previous_state = model_state
        self._previous_game = game_state
        return action

    def _game_to_model_state(self, game_state):
        player_coor = (game_state[3][0]/len(game_state[-1]), game_state[3][1]/len(game_state[-1][0]))
        player_life = game_state[1]/100
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([ np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                        np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return np.concatenate((np.array([player_life, player_coor[0], player_coor[1]]).flatten(), np_model_state_map.flatten()))

    def _update_replay_memory(self, transition):
        GroupLRRL._replay_memory.append(transition)

    def _calculate_action(self, model_state):
        prediction = self._predict(model_state)[0]
        action_index = self._choose_action_from_prediction(prediction)
        return self._feasible_actions[action_index]

    def _predict(self, model_state):
        predictions = GroupLRRL._regressions.predict(model_state)
        return predictions

    def _choose_action_from_prediction(self, prediction):
        index = np.argmax(prediction)
        if np.random.random() <= GroupLRRL._epsilon:
            index = np.random.randint(0, len(prediction))
        return index

    def _train(self, terminal_state, step): 
        if len(GroupLRRL._replay_memory) < MIN_REPLAY_MEMORY_SIZE or self._terminal_count % 50 != 0 or not terminal_state:
            return

        GroupLRRL._global_training_count += 1
        if GroupLRRL._global_training_count % GroupLRRL._global_instances != 0:
            return

        GroupLRRL._epsilon *= GroupLRRL._epsilon_decay
        print(f"Training at step: {self._turn_count}")
        minibatch = GroupLRRL._replay_memory

        current_states = self._get_state_in_prediction_structure(minibatch, 0)
        current_q_list = np.array(self._predict(current_states))

        new_current_states = self._get_state_in_prediction_structure(minibatch, 1)
        future_q_list = np.array(self._predict(new_current_states))
        
        X = []
        y = []

        for index, (current_state, new_current_state, action, reward, done, life_changer) in enumerate(minibatch):
            if done:
                new_q = -10  #reward
            elif life_changer:
                new_q = reward
            else:
                max_future_q = np.max(future_q_list[index])
                new_q = reward + DISCOUNT * max_future_q

            result = current_q_list[index]
            result[action] = new_q

            X += [current_state]
            y += [result]
        
        GroupLRRL._regressions.fit(X, y)


    def _get_state_in_prediction_structure(self, minibatch, data_index):
        current_states = np.array([transition[data_index] for transition in minibatch])
        return current_states