import random
import numpy as np
import math
from collections import deque
import time
import os

from tensorflow.keras import models
from tensorflow.keras import layers 
from tensorflow.keras import optimizers
from tensorflow.keras import callbacks
import tensorflow

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface

MODEL_NAME = "IndiDQR_1024x2"
MIN_REPLAY_MEMORY_SIZE = 2048
MAX_REPLAY_MEMORY_SIZE = 50_000
MINIBATCH_SIZE = 2048                 #Affect how many states it will use to fit

DISCOUNT = 0.99

UPDATE_TARGET_EVERY = 16

MAP_HEIGHT = 14
MAP_WIDTH = 14



class CustomCallback(callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        return
        print("Loss: {:7.2f}".format(logs["loss"]))
        print("Accuracy: {:7.2f}".format(logs["accuracy"]))




class IndiDRL(BehaviouralModelInterface):
    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._model_addr = model_addr
        self._create_directory(self._model_addr)
        self._create_model_directory(self._model_addr)

        self._mode = None
        self._previous_state = None
        self._previous_prediction = None
        self._previous_score = 0
        self._previous_action = None
        self._turn_count = 0
        
        if self._get_file_size(self._model_addr + ".txt"):
            #Load
            self._main_model, self._current_model, self._epsilon = self._load_model()
        else:
            #Create
            #Main model - Get trained every step
            self._main_model = self._build_model_conv(initial_game_state, feasible_actions)

            #Target model - This is what we predict against every step
            self._current_model = self._build_model_conv(initial_game_state, feasible_actions)
            self._current_model.set_weights(self._main_model.get_weights())
            #Set epsilon
            self._epsilon = 1

        self._epsilon_decay = 0.99925    #0.99975 before
        self._episodes = 6000
        self._episode_epsilon = self._epsilon_decay**self._episodes

        if self._epsilon < self._episode_epsilon:
            self._epsilon = 0

        self._target_update_counter = 0

        #Ensures that multiple steps can be fitted at once, so it does not overfit to a single one 
        self._replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)


    def _create_model_directory(self, addr):
        try:
            main_dir = addr + "_main_model/"
            current_dir = addr + "_current_model/"
            os.makedirs(main_dir)
            os.makedirs(current_dir)
        except FileExistsError:
            pass


    def get_epsilon(self):
        return self._epsilon

    def _load_model(self):
        print("#####LOAD MODEL#####")
        main_model = models.load_model(self._model_addr + "_main_model")
        current_model = models.load_model(self._model_addr + "_current_model")
        epsilon = None
        with open(self._model_addr + ".txt") as model_file:
            for line in model_file:
                epsilon = float(line)
        return main_model, current_model, epsilon

    def save_model(self):
        self._main_model.save(self._model_addr + "_main_model")
        self._current_model.save(self._model_addr + "_current_model")
        with open(self._model_addr + ".txt", "w") as file:
            file.write(str(self._epsilon))

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
        inputA = tensorflow.keras.Input(shape=((len(game_state)-2),)) #User info
        inputB_1 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - first layer
        inputB_2 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - second layer
        inputB_3 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - third layer

        #-------- InputB_1 --------
        #branchB_1 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_1)           #Convolutional Hidden Layer
        #branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        #branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_1)          #Convolutional Hidden Layer
        branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Flatten()(branchB_1)
        modelB_1 = models.Model(inputs=inputB_1, outputs=branchB_1)

        #-------- InputB_2 --------
        #branchB_2 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_2)           #Convolutional Hidden Layer
        #branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        #branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_2)          #Convolutional Hidden Layer
        branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Flatten()(branchB_2)
        modelB_2 = models.Model(inputs=inputB_2, outputs=branchB_2)

        #-------- InputB_3 --------
        #branchB_3 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_3)           #Convolutional Hidden Layer
        #branchB_3 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_3)
        #branchB_3 = layers.Dropout(0.2)(branchB_3)

        branchB_3 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_3)          #Convolutional Hidden Layer
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

        opt = optimizers.Adam(learning_rate=1e-3)

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

    def _get_qs(self, state, step): #Probably not gonna be used
        current_state = self._game_to_model_state(state)
        prediction = self._main_model.predict(current_state)[0]
        return prediction

    def _train(self, terminal_state, step):
        if len(self._replay_memory) < MIN_REPLAY_MEMORY_SIZE or self._turn_count % 1000 != 0:
            return
    
        minibatch = random.sample(self._replay_memory, MINIBATCH_SIZE)

        current_state = self._get_current_state(minibatch)
        current_qs_list = self._main_model.predict(current_state)

        future_state = self._get_future_state(minibatch)
        future_qs_list = self._current_model.predict(future_state)

        X_info = []
        X_l1 = []
        X_l2 = []
        X_l3 = []
        y = []

        for index, (current_state, action, reward, new_current_state, done, life_changer) in enumerate(minibatch):
            if done:
                new_q = -10  #reward
            elif life_changer:
                new_q = reward
            else:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q       #The discount is to represent that moves more in the past will have less of an effect on the current result?

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            self._append_to_input_output_matrices(X_info, X_l1, X_l2, X_l3, y, current_state, current_qs)

        X_info_np = self._transform_info_to_np_structure(X_info)
        X_l1_np = self._transform_X_to_np_structure(X_l1)
        X_l2_np = self._transform_X_to_np_structure(X_l2)
        X_l3_np = self._transform_X_to_np_structure(X_l3)

        history = self._main_model.fit([X_info_np, X_l1_np, X_l2_np, X_l3_np], np.array(y), batch_size = MINIBATCH_SIZE, verbose = 0, shuffle=False, callbacks=[CustomCallback()] if terminal_state or step%10 == 1 else None)   #Only call callback if terminal staste

        #Updating to determine if we want to update target_model yet
        if terminal_state:
            self._target_update_counter += 1

        if self._target_update_counter > UPDATE_TARGET_EVERY:
            self._target_update_counter = 0
            self._current_model.set_weights(self._main_model.get_weights())


    def _append_to_input_output_matrices(self, X0, X1, X2, X3, y, state, qs):
        X0 += [state[0]]    #Previous state
        X1 += [state[1]]
        X2 += [state[2]]
        X3 += [state[3]]
        y  += [qs]    #The score it should have let to

    def _transform_info_to_np_structure(self, X_info):
        X_info_np = np.array(X_info)
        X_info_np = X_info_np.reshape(X_info_np.shape[0], X_info_np.shape[2])
        return X_info_np

    def _transform_X_to_np_structure(self, X):
        X_np = np.array(X)
        X_np = X_np.reshape(X_np.shape[0], X_np.shape[2], X_np.shape[3], X_np.shape[4])
        return X_np

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





    def action(self, game_state, train_flag = True):
        self._turn_count += 1
        model_state = self._game_to_model_state(game_state)

        if train_flag:
            score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
            self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])

            if self._epsilon > self._episode_epsilon and self._epsilon != 0:
                if self._turn_count % 100 == 0:
                    print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")
                    if self._turn_count % 500 == 0:
                        self._epsilon *= self._epsilon_decay
                        print(f"Epsilon: {self._epsilon}, Name: {self._model_addr}")

                if isinstance(self._previous_state, list):
                    terminal_state = game_state[0] == 0 or model_state[0][0][0] != self._previous_state[0][0][0] or model_state[0][0][1] != self._previous_state[0][0][1] #If dead, different health, or different points
                    self._update_replay_memory((self._previous_state, self._previous_action, score, model_state, game_state[0] == 0, terminal_state))    #Previous state, action taken, score it got, new state it let to, and if it is done (never)
                    self._train(terminal_state , game_state[0])

            else:
                if self._turn_count % 100 == 0:
                    print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")
        elif not self._turn_count % 100:
            print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")

        action = self._calculate_action(model_state, 0 if not train_flag or self._epsilon < self._episode_epsilon else self._epsilon)
        return action


    def _calculate_action(self, current_state, epsilon):
        prediction = self._main_model.predict(current_state)
        action_index = self._choose_action_from_prediction(prediction, epsilon)
        self._previous_state = current_state
        self._previous_prediction = prediction
        self._previous_action = action_index
        return self._feasible_actions[action_index]

    def _game_to_model_state(self, game_state):
        steps = game_state[0]       #Should this be normalized?
        life = game_state[1]/100  #Normalize
        points = game_state[2]      #Should this be normalized?
        player_coor = (game_state[3][0]/len(game_state[-1][0]), game_state[3][1]/len(game_state[-1])) #Normalize
        model_state_attr = [life, player_coor[0], player_coor[1]]
        
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        
        np_model_state_attr = np.array(model_state_attr).reshape(-1, len(model_state_attr))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [np_model_state_attr, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _choose_action_from_prediction(self, prediction, epsilon):
        prediction = prediction[0]
        #Choose the highest score
        index = np.argmax(prediction)
        if np.random.random() < epsilon:
            index = np.random.randint(0, len(prediction))
        return index










class GroupDRL(BehaviouralModelInterface):
    _replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)
    _main_model = None
    _current_model = None

    _global_instances = 0
    _global_target_update_count = 0
    _global_training_count = 0
    _epsilon = 1


    def __init__(self, goals, initial_game_state, feasible_actions, model_addr, results_addr): 
        super().__init__(goals, initial_game_state, feasible_actions, results_addr)
        self._model_addr = model_addr

        self._main_model_flag = None
        if GroupDRL._main_model == None:
            self._create_directory(self._model_addr)
            self._create_model_directory(self._model_addr)
            self._main_model_flag = True           
        else:
            self._main_model_flag = False

        self._mode = None
        self._previous_state = None
        self._previous_prediction = None
        self._previous_score = 0
        self._previous_action = None
        self._turn_count = 0
        
        if self._get_file_size(self._model_addr + ".txt"):
            #Load
            if GroupDRL._main_model == None:
                GroupDRL._main_model, GroupDRL._current_model, GroupDRL._epsilon = self._load_model()
        else:
            #Create
            if GroupDRL._main_model == None:
                #Main model - Get trained every step
                GroupDRL._main_model = self._build_model_conv(initial_game_state, feasible_actions)
                #Target model - This is what we predict against every step
                GroupDRL._current_model = self._build_model_conv(initial_game_state, feasible_actions)
                GroupDRL._current_model.set_weights(GroupDRL._main_model.get_weights())
                #Set epsilon
                GroupDRL._epsilon = 1

        self._epsilon_decay = 0.99925    #0.99975 before
        self._episodes = 6000
        self._episode_epsilon = self._epsilon_decay**self._episodes

        if GroupDRL._epsilon < self._episode_epsilon:
            GroupDRL._epsilon = 0

        GroupDRL._global_target_update_count = 0
        GroupDRL._global_instances += 1
        #Ensures that multiple steps can be fitted at once, so it does not overfit to a single one 
        GroupDRL._replay_memory = deque(maxlen=MAX_REPLAY_MEMORY_SIZE)

    def _create_model_directory(self, addr):
        try:
            main_dir = addr + "_main_model/"
            current_dir = addr + "_current_model/"
            os.makedirs(main_dir)
            os.makedirs(current_dir)
        except FileExistsError:
            pass

    def get_epsilon(self):
        return GroupDRL._epsilon

    def _load_model(self):
        print("#####LOAD MODEL#####")
        main_model = models.load_model(self._model_addr + "_main_model")
        current_model = models.load_model(self._model_addr + "_current_model")
        epsilon = None
        with open(self._model_addr + ".txt") as model_file:
            for line in model_file:
                epsilon = float(line)
        return main_model, current_model, epsilon

    def save_model(self):
        if self._main_model_flag == True:
            GroupDRL._main_model.save(self._model_addr + "_main_model")
            GroupDRL._current_model.save(self._model_addr + "_current_model")
            with open(self._model_addr + ".txt", "w") as file:
                file.write(str(GroupDRL._epsilon))

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
        inputA = tensorflow.keras.Input(shape=((len(game_state)-2),)) #User info
        inputB_1 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - first layer
        inputB_2 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - second layer
        inputB_3 = tensorflow.keras.Input(shape=(len(game_state[-1]), len(game_state[-1][0]), 3)) #Map data - third layer

        #-------- InputB_1 --------
        #branchB_1 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_1)           #Convolutional Hidden Layer
        #branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        #branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_1)          #Convolutional Hidden Layer
        branchB_1 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_1)
        branchB_1 = layers.Dropout(0.2)(branchB_1)

        branchB_1 = layers.Flatten()(branchB_1)
        modelB_1 = models.Model(inputs=inputB_1, outputs=branchB_1)

        #-------- InputB_2 --------
        #branchB_2 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_2)           #Convolutional Hidden Layer
        #branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        #branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_2)          #Convolutional Hidden Layer
        branchB_2 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_2)
        branchB_2 = layers.Dropout(0.2)(branchB_2)

        branchB_2 = layers.Flatten()(branchB_2)
        modelB_2 = models.Model(inputs=inputB_2, outputs=branchB_2)

        #-------- InputB_3 --------
        #branchB_3 = layers.Conv2D(64, (3, 3), activation = 'relu')(inputB_3)           #Convolutional Hidden Layer
        #branchB_3 = layers.MaxPooling2D(pool_size=(2, 2))(branchB_3)
        #branchB_3 = layers.Dropout(0.2)(branchB_3)

        branchB_3 = layers.Conv2D(128, (3, 3), activation = 'relu')(inputB_3)          #Convolutional Hidden Layer
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

        opt = optimizers.Adam(learning_rate=1e-3)

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
        GroupDRL._replay_memory.append(transition)

    def _get_qs(self, state, step): #Probably not gonna be used
        current_state = self._game_to_model_state(state)
        prediction = GroupDRL._main_model.predict(current_state)[0]
        return prediction

    def _train(self, terminal_state, step):
        if len(GroupDRL._replay_memory) < (MIN_REPLAY_MEMORY_SIZE*GroupDRL._global_instances) or GroupDRL._global_training_count % (GroupDRL._global_instances*1000) % 1000 != 0:
            return
    
        minibatch = random.sample(GroupDRL._replay_memory, MINIBATCH_SIZE*GroupDRL._global_instances)

        current_state = self._get_current_state(minibatch)
        current_qs_list = GroupDRL._main_model.predict(current_state)

        future_state = self._get_future_state(minibatch)
        future_qs_list = GroupDRL._current_model.predict(future_state)

        X_info = []
        X_l1 = []
        X_l2 = []
        X_l3 = []
        y = []

        for index, (current_state, action, reward, new_current_state, done, life_changer) in enumerate(minibatch):
            if done:
                new_q = -10  #reward
            elif life_changer:
                new_q = reward
            else:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q       #The discount is to represent that moves more in the past will have less of an effect on the current result?

            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            self._append_to_input_output_matrices(X_info, X_l1, X_l2, X_l3, y, current_state, current_qs)

        X_info_np = self._transform_info_to_np_structure(X_info)
        X_l1_np = self._transform_X_to_np_structure(X_l1)
        X_l2_np = self._transform_X_to_np_structure(X_l2)
        X_l3_np = self._transform_X_to_np_structure(X_l3)

        history = GroupDRL._main_model.fit([X_info_np, X_l1_np, X_l2_np, X_l3_np], np.array(y), batch_size = MINIBATCH_SIZE, verbose = 0, shuffle=False, callbacks=[CustomCallback()] if terminal_state or step%10 == 1 else None)   #Only call callback if terminal staste

        #Updating to determine if we want to update target_model yet
        if terminal_state:
             GroupDRL._global_target_update_count += 1

        if GroupDRL._global_target_update_count > UPDATE_TARGET_EVERY:
            GroupDRL._global_target_update_count = 0
            GroupDRL._current_model.set_weights(GroupDRL._main_model.get_weights())


    def _append_to_input_output_matrices(self, X0, X1, X2, X3, y, state, qs):
        X0 += [state[0]]    #Previous state
        X1 += [state[1]]
        X2 += [state[2]]
        X3 += [state[3]]
        y  += [qs]    #The score it should have let to

    def _transform_info_to_np_structure(self, X_info):
        X_info_np = np.array(X_info)
        X_info_np = X_info_np.reshape(X_info_np.shape[0], X_info_np.shape[2])
        return X_info_np

    def _transform_X_to_np_structure(self, X):
        X_np = np.array(X)
        X_np = X_np.reshape(X_np.shape[0], X_np.shape[2], X_np.shape[3], X_np.shape[4])
        return X_np

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





    def action(self, game_state, train_flag = True):
        self._turn_count += 1
        GroupDRL._global_training_count += 1
        model_state = self._game_to_model_state(game_state)

        if train_flag:
            score = self._calculate_score(game_state[0], game_state[2], game_state[3]) - self._previous_score  #Reward - Use reqard difference instead
            self._previous_score = self._calculate_score(game_state[0], game_state[2], game_state[3])

            if GroupDRL._epsilon > self._episode_epsilon and GroupDRL._epsilon != 0:
                if self._turn_count % 100 == 0:
                    print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")
                    if self._turn_count % 500 == 0:
                        GroupDRL._epsilon *= self._epsilon_decay
                        print(f"Epsilon: {GroupDRL._epsilon}, Name: {self._model_addr}")

                if isinstance(self._previous_state, list):
                    terminal_state = game_state[0] == 0 or model_state[0][0][0] != self._previous_state[0][0][0] or model_state[0][0][1] != self._previous_state[0][0][1] #If dead, different health, or different points
                    self._update_replay_memory((self._previous_state, self._previous_action, score, model_state, game_state[0] == 0, terminal_state))    #Previous state, action taken, score it got, new state it let to, and if it is done (never)
                    self._train(terminal_state , game_state[0])

            else:
                if self._turn_count % 100 == 0:
                    print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")
        elif not self._turn_count % 100:
            print(f"Train: {train_flag}, steps: {self._turn_count}, life: {game_state[1]}, points: {game_state[2]}, score: {self._previous_score}, Name: {self._model_addr}")

        action = self._calculate_action(model_state, 0 if not train_flag or GroupDRL._epsilon < self._episode_epsilon else GroupDRL._epsilon)
        return action


    def _calculate_action(self, current_state, epsilon):
        prediction = GroupDRL._main_model.predict(current_state)
        action_index = self._choose_action_from_prediction(prediction, epsilon)
        self._previous_state = current_state
        self._previous_prediction = prediction
        self._previous_action = action_index
        return self._feasible_actions[action_index]

    def _game_to_model_state(self, game_state):
        steps = game_state[0]       #Should this be normalized?
        life = game_state[1]/100  #Normalize
        points = game_state[2]      #Should this be normalized?
        player_coor = (game_state[3][0]/len(game_state[-1][0]), game_state[3][1]/len(game_state[-1])) #Normalize
        model_state_attr = [life, player_coor[0], player_coor[1]]
        
        image_shape = (len(game_state[-1]), len(game_state[-1][0]), len(game_state[-1][0][0][0]))
        
        np_model_state_attr = np.array(model_state_attr).reshape(-1, len(model_state_attr))
        np_map = np.array(game_state[-1])
        np_model_state_map = np.array([  np_map[:,:,0].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,1].reshape(-1, *image_shape)/255, 
                                         np_map[:,:,2].reshape(-1, *image_shape)/255 ])
        return [np_model_state_attr, np_model_state_map[0], np_model_state_map[1], np_model_state_map[2]]

    def _choose_action_from_prediction(self, prediction, epsilon):
        prediction = prediction[0]
        #Choose the highest score
        index = np.argmax(prediction)
        if np.random.random() < epsilon:
            index = np.random.randint(0, len(prediction))
        return index