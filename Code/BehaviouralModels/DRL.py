import random
import numpy as np
import math
from collections import deque
import time

from tensorflow.keras import models
from tensorflow.keras import layers 
from tensorflow.keras import optimizers
from tensorflow.keras import callbacks
import tensorflow

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface

MODEL_NAME = "IndiDQR_1024x2"
MIN_REPLAY_MEMORY_SIZE = 128
MAX_REPLAY_MEMORY_SIZE = 50_000
MINIBATCH_SIZE = 128                 #Affect how many states it will use to fit

DISCOUNT = 0.99

UPDATE_TARGET_EVERY = 5



class CustomCallback(callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print("Loss: {:7.2f}".format(logs["loss"]))
        print("Accuracy: {:7.2f}".format(logs["accuracy"]))




class IndiDRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)
        self._mode = None
        self._previous_state = None
        self._previous_prediction = None
        self._previous_score = 0
        self._epsilon = 1
        self._epsilon_decay = 0.9975    #0.99975 before

        #Main model - Get trained every step
        self._main_model = self._build_model_conv(initial_game_state, feasible_actions)

        #Target model - This is what we predict against every step
        self._current_model = self._build_model_conv(initial_game_state, feasible_actions)
        self._current_model.set_weights(self._main_model.get_weights())

        self._target_update_counter = 0

        #Ensures that multiple steps can be fitted at once, so it does not overfit to a single one 
        self._replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)


    def _build_model(self, game_state, feasible_actions):  
        first_layer_size = (len(game_state)) + len(game_state[-1])*3*3      #3 colors in our layers at X pixels + extra info
                                                                                #Should probably use cnn...
        model = models.Sequential()
        model.add(tensorflow.keras.Input(shape=(first_layer_size,), name="digits")) #Input  layer
        model.add(layers.Dense(1024, activation='relu'))                            #Hidden layer
        model.add(layers.Dense(1024, activation='relu'))                            #Hidden layer
        model.add(layers.Dense(len(feasible_actions), activation='linear'))         #Output layer

        opt = optimizers.Adam(learning_rate=0.0001, decay=1e-6)

        model.compile(loss="mse",
              optimizer=opt,
              metrics=['accuracy'])
              
        return model


    def _build_model_conv(self, game_state, feasible_actions):
        inputA = tensorflow.keras.Input(shape=((len(game_state)-1),)) #User info
        inputB_1 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - first layer
        inputB_2 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - second layer
        inputB_3 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - third layer

        #-------- InputB_1 --------
        branchB_1 = layers.Conv2D(16, (3, 3), activation = 'relu')(inputB_1)           #Convolutional Hidden Layer
        branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Conv2D(32, (3, 3), activation = 'relu')(branchB_1)          #Convolutional Hidden Layer
        branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Flatten()(branchB_1)
        modelB_1 = models.Model(inputs=inputB_1, outputs=branchB_1)

        #-------- InputB_2 --------
        branchB_2 = layers.Conv2D(16, (3, 3), activation = 'relu')(inputB_2)           #Convolutional Hidden Layer
        branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Conv2D(32, (3, 3), activation = 'relu')(branchB_2)          #Convolutional Hidden Layer
        branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Flatten()(branchB_2)
        modelB_2 = models.Model(inputs=inputB_2, outputs=branchB_2)

        #-------- InputB_3 --------
        branchB_3 = layers.Conv2D(16, (3, 3), activation = 'relu')(inputB_3)           #Convolutional Hidden Layer
        branchB_3 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_3)
        branchB_3 = layers.Dropout(0.2)(branchB_3)

        branchB_3 = layers.Conv2D(32, (3, 3), activation = 'relu')(branchB_3)          #Convolutional Hidden Layer
        branchB_3 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_3)
        branchB_3 = layers.Dropout(0.2)(branchB_3)

        branchB_3 = layers.Flatten()(branchB_3)
        modelB_3 = models.Model(inputs=inputB_3, outputs=branchB_3)


        #------- Combine -------
        branchC = layers.concatenate([inputA, modelB_1.output, modelB_2.output, modelB_3.output])      

        branchC = layers.Dense(256, activation='relu')(branchC)
        branchC = layers.Dense(256, activation='relu')(branchC)
        output = layers.Dense(len(feasible_actions), activation='linear')(branchC)  #Output layer

        model = models.Model(inputs=[inputA, modelB_1.input, modelB_2.input, modelB_3.input], outputs = output)

        opt = optimizers.Adam(learning_rate=0.0001, decay=1e-6)

        model.compile(loss="mse",
              optimizer=opt,
              metrics=['accuracy'])

        #tensorflow.keras.utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True)

        return model


    def _custom_loss_function(self, score_true, score_expected):
        custom_loss = []
        for index, _ in enumerate(score_true):
            custom_loss += [math.sqrt((score_true[index]-score_expected[index])**2)]
        return np.asarray([custom_loss])

    def _update_replay_memory(self, transition):
        self._replay_memory.append(transition)

    def _get_queues(self, state, step): #Probably not gonna be used
        current_state = self._game_to_model_state(state)
        prediction = self._main_model.predict(current_state)[0]
        return prediction

    def _train(self, terminal_state, step):
        if len(self._replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return
    
        minibatch = random.sample(self._replay_memory, MINIBATCH_SIZE)

        current_state = self._get_current_state(minibatch)
        current_queues_list = self._main_model.predict(current_state)

        future_state = self._get_future_state(minibatch)
        future_queues_list = self._current_model.predict(future_state)

        X_info = []
        X_l1 = []
        X_l2 = []
        X_l3 = []
        y = []

        for index, (current_state, action, reward, new_current_state, done, life_changer) in enumerate(minibatch):
            if done:
                new_queue = -1  #reward
            elif life_changer:
                new_queue = reward
            else:
                max_future_queue = np.max(future_queues_list[index])
                new_queue = reward + DISCOUNT * max_future_queue       #The discount is to represent that moves more in the past will have less of an effect on the current result?

            current_queues = current_queues_list[index]
            current_queues = [ -1 if q < -1 else (q if q < 1 else 1) for q in current_queues]
            current_queues[action] = new_queue

            X_info.append(current_state[0])     #Previous state
            X_l1.append(current_state[1])
            X_l2.append(current_state[2])
            X_l3.append(current_state[3])
            y.append(current_queues)    #The score it should have let to

        X_info_np = np.array(X_info)
        X_info_np = X_info_np.reshape(X_info_np.shape[0], X_info_np.shape[2])
        X_l1_np = np.array(X_l1)
        X_l1_np = X_l1_np.reshape(X_l1_np.shape[0], X_l1_np.shape[2], X_l1_np.shape[3], X_l1_np.shape[4])
        X_l2_np = np.array(X_l2)
        X_l2_np = X_l2_np.reshape(X_l2_np.shape[0], X_l2_np.shape[2], X_l2_np.shape[3], X_l2_np.shape[4])
        X_l3_np = np.array(X_l3)
        X_l3_np = X_l3_np.reshape(X_l3_np.shape[0], X_l3_np.shape[2], X_l3_np.shape[3], X_l3_np.shape[4])

        history = self._main_model.fit([X_info_np, X_l1_np, X_l2_np, X_l3_np], np.array(y), batch_size = MINIBATCH_SIZE, verbose = 0, shuffle=False, callbacks=[CustomCallback()] if terminal_state or step%10 == 1 else None)   #Only call callback if terminal staste

        #Updating to determine if we want to update target_model yet
        if terminal_state:
            self._current_model.set_weights(self._main_model.get_weights())
            self._epsilon *= self._epsilon_decay
            print(f"Epsilon: {self._epsilon}")
            print(f"History: {history.history}")


    def _get_current_state(self, minibatch):
        current_states_0 = np.array([transition[0][0] for transition in minibatch])
        current_states_0 = current_states_0.reshape(current_states_0.shape[0], current_states_0.shape[2])
        current_states_1 = np.array([transition[0][1] for transition in minibatch])
        current_states_1 = current_states_1.reshape(current_states_1.shape[0], current_states_1.shape[2], current_states_1.shape[3], current_states_1.shape[4])
        current_states_2 = np.array([transition[0][2] for transition in minibatch])
        current_states_2 = current_states_2.reshape(current_states_2.shape[0], current_states_2.shape[2], current_states_2.shape[3], current_states_2.shape[4])
        current_states_3 = np.array([transition[0][3] for transition in minibatch])
        current_states_3 = current_states_3.reshape(current_states_3.shape[0], current_states_3.shape[2], current_states_3.shape[3], current_states_3.shape[4])
        return [current_states_0, current_states_1, current_states_2, current_states_3]

    def _get_future_state(self, minibatch):
        new_current_state_0 = np.array([transition[3][0] for transition in minibatch])
        new_current_state_0 = new_current_state_0.reshape(new_current_state_0.shape[0], new_current_state_0.shape[2])
        new_current_state_1 = np.array([transition[3][1] for transition in minibatch])
        new_current_state_1 = new_current_state_1.reshape(new_current_state_1.shape[0], new_current_state_1.shape[2], new_current_state_1.shape[3], new_current_state_1.shape[4])
        new_current_state_2 = np.array([transition[3][2] for transition in minibatch])
        new_current_state_2 = new_current_state_2.reshape(new_current_state_2.shape[0], new_current_state_2.shape[2], new_current_state_2.shape[3], new_current_state_2.shape[4])
        new_current_state_3 = np.array([transition[3][3] for transition in minibatch])
        new_current_state_3 = new_current_state_3.reshape(new_current_state_3.shape[0], new_current_state_3.shape[2], new_current_state_3.shape[3], new_current_state_3.shape[4])
        return [new_current_state_0, new_current_state_1, new_current_state_2, new_current_state_3]

    def action(self, game_state):
        score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
        self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])
        model_state = self._game_to_model_state(game_state)
        if isinstance(self._previous_state, list):
            terminal_state = game_state[0] == 0 or model_state[0][0][0] != self._previous_state[0][0][0] or model_state[0][0][1] != self._previous_state[0][0][1] #If dead, different health, or different points
            self._update_replay_memory((self._previous_state, self._choose_action_from_prediction(self._previous_prediction), score, model_state, game_state[0] == 0, terminal_state))    #Previous state, action taken, score it got, new state it let to, and if it is done (never)
            self._train(terminal_state , game_state[0])
        action = self._calculate_action(model_state)
        return action

    def _modify_model(self, true_score):    #Train model - A new version of this hasve been written to accomidate for RL training. This is more of the traditional way of NN
        true_prediction = []
        action_index = self._choose_action_from_prediction(self._previous_prediction)
        for index, value in enumerate(self._previous_prediction[0]):
            if index == action_index:
                true_prediction += [true_score]
            else:
                true_prediction += [value]
        self._main_model.fit(x = np.asarray([self._previous_state]), y = np.asarray([true_prediction]), verbose = 1, shuffle=False)

    def _calculate_action(self, current_state):
        prediction = self._main_model.predict(current_state)
        action_index = self._choose_action_from_prediction(prediction)
        self._previous_state = current_state
        self._previous_prediction = prediction
        return self._feasible_actions[action_index]

    def _game_to_model_state(self, game_state):
        steps = game_state[0]       #Should this be normalized?
        life = game_state[1] / 100  #Normalize
        points = game_state[2]      #Should this be normalized?
        player_coor = (game_state[3][0]/len(game_state[-1]), game_state[3][1]/len(game_state[-1][0])) #Normalize
        model_state_attr = [life, points, player_coor[0], player_coor[1]]
        
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        
        np_model_state_attr = np.array(model_state_attr).reshape(-1, len(model_state_attr))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [np_model_state_attr, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _choose_action_from_prediction(self, prediction):
        prediction = prediction[0]
        #Choose the highest score
        index_score = [0, prediction[0]]
        for index, score in enumerate(prediction):
            if score > index_score[1]:
                index_score = [index, score]
        index = index_score[0]
        if np.random.random() <= self._epsilon:
            index = np.random.randint(0, len(prediction))
        return index






class GroupDRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions):
        super().__init__(goals, initial_game_state, feasible_actions)