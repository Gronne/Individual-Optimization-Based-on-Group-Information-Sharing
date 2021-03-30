import cv2
import numpy as np
import math
import time

from Simulations.GameFeatures import *
from Simulations.Visualizers import *


class EnvironmentSuit:
    def __init__(self, nr_of_env, behaviour_model, step_size = 1,variation = 0, distribution = 0, features = None, verbose = 1 ):      #createEnvironments
        self.environments = self._create_environments(nr_of_env, behaviour_model, step_size, variation, distribution, features, verbose)
        self._print_flag = True
        self._quite_input = 113  # 'q'
        self._speed_up = 43      # '+'
        self._speed_down = 45    # '-'
        self._start_input = 115  # 's'
        self._pause_input = 112  # 'p'
        self._print_toggle = 118 # 'v'

    def _create_environments(self, nr_of_env, behaviour_model, step_size, variation, distribution, env_features_list, verbose):
        if env_features_list == None:
            env_features_list = self._generate_env_features(nr_of_env, variation, distribution)
        window_size = self._calc_window_size(nr_of_env)
        environments = []
        for env_nr in range(0, nr_of_env):
            environments += [Environment("Env_" + str(env_nr+1), behaviour_model, step_size, env_features_list[env_nr], verbose, window_size)]
        return environments

    def _calc_window_size(self, nr_of_env):
        #Max 800 i højden og 1600 i bredden
        size_div = 1
        if nr_of_env <= 2: size_div = 1
        elif nr_of_env <= 8: size_div = 2
        elif nr_of_env <= 16: size_div = 4
        else: size_div = 8
        side_length = int(800 / size_div)
        return (side_length, side_length)

    def _generate_env_features(self, nr_of_env, variation, distribution):       #OBS! Not implemented
        return [GameFeatures()]*nr_of_env

    def run(self, simulation_delay = 1000):
        running_sim = True
        while True:
            if running_sim == True:
                self._update_environments()
                self._simulation_delay(simulation_delay)
            k_input = self._get_keyboard_input()
            if self._quite_input == k_input:
                break
            elif self._speed_up == k_input:
                simulation_delay /= 2
            elif self._speed_down == k_input:
                simulation_delay *= 2
            elif self._start_input == k_input:
                running_sim = True
            elif self._pause_input == k_input:
                running_sim = False
            elif self._print_toggle == k_input:
                self._print_flag = not self._print_flag
        self._shutdown_environments()

    def _update_environments(self):
        for environment in self.environments:
            environment.step()
            if self._print_flag == True:
                environment.print()

    def _simulation_delay(self, simulation_delay):
        time.sleep(simulation_delay/1000)

    def _get_keyboard_input(self):
        keyPress = cv2.waitKey(1)
        return keyPress

    def _shutdown_environments(self):
        cv2.destroyAllWindows()




class Environment:
    def __init__(self, name, behaviour_model, step_size, features, verbose = 2, window_size = (600, 600)):
        if verbose == 2:
            self._window = self._create_layout(window_size)
            self._window_size = window_size
        self._original_features = features
        self._name = name
        self._verbose = verbose
        self._player = self._create_player(features)
        self._game_map = self._get_game_map(features)
        self._game_map_size = self._get_game_map_size(features)
        self._game_objects = self._get_game_objects(features)
        self._color_map_copy = self._create_color_block_map()
        self._model = behaviour_model(self._get_game_goals(features), self._get_game_state(), self._get_action_inputs())

    def _create_layout(self, window_size):
        img = np.zeros([window_size[0], window_size[1], 3],dtype=np.uint8)  #Square window
        img.fill(255)
        return img

    def _create_player(self, features):
        start_pos = features.get_start_position()
        return {"Object": Player(features.get_controls(), features.get_survival_properties(), start_pos), "Location": start_pos, "Start Location": start_pos}

    def _get_game_goals(self, features):
        return features.get_goals()

    def _get_game_map(self, features):
        return features.get_map()

    def _get_game_map_size(self, features):
        return features.get_map_size()

    def _get_game_objects(self, features):
        list_of_monsters = features.get_monsters()
        list_of_items = features.get_items()
        list_of_objects = list_of_monsters + list_of_items
        return list_of_objects

    def _get_game_goals(self, features):
        return features.get_goals()

    def step(self):
        print("Step from " + self._name)
        game_state = self._get_game_state()
        action_inputs =  self._get_action_inputs()
        action = self._model.action(game_state)
        self._game_react(action)


    def _get_action_inputs(self):
        return self._player["Object"].get_feasible_controls(self._game_map_size, self._player["Location"])

    def _perform_action(self, action):
        self._player["Location"] = self._player["Object"].move_action(action, self._player["Location"], self._game_map, self._game_map_size)

    def _move_game_objects(self):
        for obj in self._game_objects:
            obj["Location"] = obj["Object"].move_action(obj["Location"], self._game_map, self._game_map_size)

    def _game_react(self, action):
        self._perform_action(action)
        self._move_game_objects()
        self._player_react()
        self._game_object_react()

    def _player_react(self):
        player_coor = self._player["Location"]
        player_block = self._game_map[player_coor]["Object"]
        player_objects = self._find_game_objects(player_coor)
        self._player["Object"].reaction_action(player_block, player_objects)
        self._react_on_player_status()

    def _react_on_player_status(self):
        if self._player["Object"].get_health() == 0:
            self._player["Object"].kill_player()
            self._reset_environment()

    def _reset_environment(self):   #Respawn player, respawn items
        self._player["Location"] = self._player["Start Location"]
        for obj in self._game_objects:
            obj["Object"].reset()
            obj["Location"] = obj["Start Location"]

    def _game_object_react(self):
        for game_object in self._game_objects:
            obj_coor = game_object["Location"]
            if obj_coor == (-1, -1):
                obj_coor = game_object["Start Location"]
            block = self._game_map[obj_coor]["Object"]
            objects = [obj for obj in self._find_game_objects(obj_coor) if obj != game_object]
            player_interaction = obj_coor == self._player["Location"]
            game_object["Object"].reaction_action(block, objects, player_interaction)

    def _find_game_objects(self, location):
        return [game_object["Object"] for game_object in self._game_objects if game_object["Location"] == location]

    def print(self):
        if self._verbose == 2:
            GameVisualizer._visualize_game(self._window, self._name, self._window_size, self._game_map_size, self._player, self._game_map, self._game_objects)
        elif self._verbose == 1:
            print("Game-State for " + self.get_name())
            print(self._get_game_state())

    def get_name(self):
        return self._name

    def _get_game_state(self):
        player_survival_time = self._player["Object"].get_survival_time()
        player_health = self._player["Object"].get_health()
        player_points = self._player["Object"].get_points()
        player_coordinate = self._player["Location"]
        map_view = self._map_view_layered()
        return [player_survival_time, player_health, player_points, player_coordinate, map_view]

    def _map_view_layered(self):
        new_map = self._color_map_copy
        for game_object in self._game_objects:  #First set monsters
            coor = game_object["Location"]
            obj = game_object["Object"]
            if isinstance(obj, GameMonster):
                new_map[coor[0]-1][coor[1]-1][1] = obj.get_color()
                new_map[coor[0]-1][coor[1]-1][2] = obj.get_color()
        for game_object in self._game_objects:  #Then set items - To get the right color combination
            coor = game_object["Location"]
            obj = game_object["Object"]
            if isinstance(obj, GameItem):
                new_map[coor[0]-1][coor[1]-1][2] = obj.get_color()
        return new_map

    def _create_color_block_map(self):      #Remember to make the map 2D!!!!!!!!!!!!!
        coordinate_list = [(coor_h, coor_w) for coor_h in range(1, self._game_map_size[0]+1) for coor_w in range(1, self._game_map_size[1]+1)]
        color_map = []
        color_list = []
        for index, coor in enumerate(coordinate_list):
            if index % self._game_map_size[0] == 0 and index != 0:
                color_map += [color_list]
                color_list = []
            block_color = self._game_map[coor]["Object"].get_color()
            colors = [block_color, block_color, block_color]
            color_list += [colors]
        color_map += [color_list]
        return color_map
