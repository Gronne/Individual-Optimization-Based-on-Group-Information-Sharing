import numpy as np
import math

class GameFeatures:     #feature.add_controls(GameFeatures.Controls.)
    class Controls:
        LeftRight = "LeftRight"
        UpDown ="UpDown"
        AllArrows = "AllArrows"

    class MapLayout:
        DefaultMap1 = "XXXXXXXXXXXXXXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXXXXXXXXXXXXXXn"
        DefaultMap2 = "XXXXXXXXXXXXXXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXXXXXXXXXXXOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOXXXXXXXXXXXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXXXXXXXXXXXXXXn"
        DefaultMap3 = "XXXXXXXXXXXXXXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXXXXXXXXXXXXOXnXXXXXXXXXXXXOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXOOOOOOOOOOOOXnXXXXXXXXXXXXXXn"
        DefaultMap4 = "XOOOOOOOOOOOOXnOXOOOOXXOOOOXOnOOXOOOOOOOOXOOnOOOXOOOOOOXOOOnOOOOXOOOOXOOOOnOOOOOOOOOOOOOOnOXOOOOOOOOOOXOnOXOOOOOOOOOOXOnOOOOOOOOOOOOOOnOOOOXOOOOXOOOOnOOOXOOOOOOXOOOnOOXOOOOOOOOXOOnOXOOOOXXOOOOXOnXOOOOOOOOOOOOXn"
        Empty14x14  = "OOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOnOOOOOOOOOOOOOOn"
        SimpleMap   = "XXXXXXXXXXXXXXnXOOOOOOOOOOOOXnXXXXXXXXXXXXXXn"
        SimpleMap2  = "XXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXOOOOOOOOOOOOXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXnXXXXXXXXXXXXXXn"
        
    class MonsterColor:
        White = "White"
        Black = "Black"
        Blue = "Blue"
        Red = "Red"
        Green = "Green"
        Yellow = "Yellow"

    class MonsterEffect:
        Kill = "Kill"
        TakeLife = "TakeLife"
        TakePoints = "TakePoints"
        Nothing = "Nothing"
        GiveLife = "GiveLife"
        GivePoints = "GivePoints"

    class MonsterType:
        Invincible = "Invincible"
        Small = "small"
        Ledium = "medium"
        Large = "large"

    class MonsterBehaviour:
        UpDown = "UpDown"
        LeftRight = "LeftRight"
        DiagonalLeft = "DiagonalLeft"
        DiagonalRight = "DiagonaliRight"
        FollowUser = "FollowUser"
        Nothing = "Nothing"

    class BlockColor:
        White = "White"
        Black = "Black"
        Blue = "Blue"
        Red = "Red"
        Green = "Green"
        Yellow = "Yellow"

    class BlockEffect:
        Nothing = "Nothing"
        Block = "Block"
        TakeLife = "TakeLife"
        GiveLife = "GiveLife"
        TakePoints = "TakePoints"
        GivePoints = "GivePoints"

    class ItemColor:
        White = "White"
        Black = "Black"
        Blue = "Blue"
        Red = "Red"
        Green = "Green"
        Yellow = "Yellow"

    class ItemEffect:
        GivePoints = "GivePoints"
        TakePoints = "TakePoints"
        GiveLife = "GiveLife"
        TakeLife = "TakeLife"
        Nothing = "Nothing"

    class ItemBehaviour:
        Nothing = "Nothing"
        Respawn = "Respawn"

    class GoalSystem:
        Time = "MaximizeSurvivalTime"  
        Resources = "MaximizeResources"
        Safety = "MaximizeSafetyAndComfort"     #Minimize how much the agent move around
    
    class SurvivalProperty:
        Starve = "Starvation"
        Slowdown = "Slowdown"
        Nothing = "Nothing"

    def __init__(self):
        #Set all to default
        self._features = {  "Start": (2, 2),
                            "Monsters": [], 
                            "Map": {},
                            "Items": [],
                            "Map Size": (0, 0),
                            "Control": GameFeatures.Controls.AllArrows,
                            "Goals": [],
                            "Survival": []}
        self.add_survival_property(GameFeatures.SurvivalProperty.Nothing)

    def add_controls(self, control_type):   #Only one
        self._features["Control"] = control_type

    def add_map_layout(self, map_string, map_setup = { "X": {"Color": "Black", "Effect": "Block"}, "O": {"Color": "White", "Effect": "Nothing"} }): #Only one
        map_split = map_string.split("n")[:-1]
        self._check_map(map_split)
        self._features["Map Size"] = (len(map_split), len(map_split[0]))
        for row_nr, row in enumerate(map_split):
            for col_nr, char in enumerate(row):
                if char in map_setup:
                    self.add_block(map_setup[char]["Color"], map_setup[char]["Effect"], [(row_nr+1, col_nr+1)])
                else:
                    raise Exception(char + " does not exists in the setup file")

    def _check_map(self, map_split):
        array_length = len(map_split[0])
        for array in map_split:
            if len(array) != array_length:
                raise Exception("Invalid Map row Lengths")

    def add_monster(self, m_type, color, effect, behaviour, locations, speed = 1, effect_strength = 1):    #Multiple 
        self._features["Monsters"] += [ {"Object": GameMonster(m_type, color, effect, behaviour, location, speed, effect_strength), "Location": location, "Start Location": location} for location in locations]

    def add_block(self, color, effect, locations, effect_strength = 1): #Multiple 
        for location in locations:
            if (location[0] > 0 and location[0] <= self._features["Map Size"][1]) and (location[1] > 0 and location[1] <= self._features["Map Size"][1]):
                self._features["Map"][location] = {"Object": GameBlock(color, effect, effect_strength), "Location": location, "Start Location": location}
            else:
                raise Exception("Block outsite out scope")


    def add_item(self, color, effect, behaviour, locations, respawn_time = 10, effect_strength=1):  #Multiple 
        self._features["Items"] += [ {"Object": GameItem(color, effect, behaviour, location, respawn_time, effect_strength), "Location": location, "Start Location": location} for location in locations]

    def add_goals(self, goals):
        if isinstance(goals, list):
            self._features["Goals"] += goals
        else:
            self._features["Goals"] += [goals]

    def add_survival_property(self, s_type, interval = 10, strength = 1):
        self._features["Survival"] += [{"Property": s_type, "Interval": interval, "Strength": strength}]

    def add_start_position(self, location):
        self._features["Start"] = location

    def get_all_features(self):
        return self._features

    def get_start_position(self):
        return self._features["Start"]

    def get_monsters(self):
        return self._features["Monsters"]
    
    def get_items(self):
        return self._features["Items"]

    def get_map_size(self):
        return self._features["Map Size"]

    def get_map(self):
        return self._features["Map"]

    def get_controls(self):
        return self._features["Control"]

    def get_goals(self):
        return self._features["Goals"]

    def get_survival_properties(self):
        return self._features["Survival"]



class GameObject:
    def __init__(self):
        pass 

    def _create_color(self, color_str):
        new_color = ()
        if color_str.lower() == "red":
            new_color = (0, 0, 255)
        elif color_str.lower() == "green":
            new_color = (0, 255, 0)
        elif color_str.lower() == "blue":
            new_color = (255, 0, 0)
        elif color_str.lower() == "black":
            new_color = (0, 0, 0)
        elif color_str.lower() == "white":
            new_color = (255, 255, 255)
        elif color_str.lower() == "yellow":
            new_color = (0, 255, 255)
        else:
            raise Exception(color_str + " color does not exist for Blocks")
        return new_color

    def reset(self):
        pass

    def _possible_to_move_left(self, location, game_map, map_size):
        move_out_of_bound = location[1] > 1
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0], location[1]-1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_right(self, location, game_map, map_size):
        move_out_of_bound = location[1] < map_size[1]
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0], location[1]+1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_up(self, location, game_map, map_size):
        move_out_of_bound = location[0] > 1
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]-1, location[1])]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_down(self, location, game_map, map_size):
        move_out_of_bound = location[0] < map_size[0]
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]+1, location[1])]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_diaLeftUp(self, location, game_map, map_size):
        move_out_of_bound = location[1] > 1 and location[0] > 1
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]-1, location[1]-1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_diaLeftDown(self, location, game_map, map_size):
        move_out_of_bound = location[1] < map_size[1] and location[0] < map_size[0]
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]+1, location[1]+1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_diaRightUp(self, location, game_map, map_size):
        move_out_of_bound = location[0] > 1 and location[1] < map_size[1]
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]-1, location[1]+1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)

    def _possible_to_move_diaRightDown(self, location, game_map, map_size):
        move_out_of_bound = location[1] > 1 and location[0] < map_size[0]
        if move_out_of_bound == True:
            move_into_solid_object = game_map[(location[0]+1, location[1]-1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block
        else:
            move_into_solid_object = False
        return not (not move_out_of_bound or not move_into_solid_object)
    
    def _move_left(self, location):
        return (location[0], location[1]-1)

    def _move_right(self, location):
        return (location[0], location[1]+1)

    def _move_up(self, location):
        return (location[0]-1, location[1])

    def _move_down(self, location):
        return (location[0]+1, location[1])

    def _move_diaLeftUp(self, location):
        return (location[0]-1, location[1]-1)

    def _move_diaLeftDown(self, location):
        return (location[0]+1, location[1]+1)

    def _move_diaRightUp(self, location):
        return (location[0]-1, location[1]+1)

    def _move_diaRightDown(self, location):
        return (location[0]+1, location[1]-1)




class GameBlock(GameObject):
    def __init__(self, color, effect, effect_strength=1):
        self._color = super()._create_color(color)
        self._effect = effect
        self._effect_strength = effect_strength

    def get_color(self):
        return self._color

    def get_effect(self):
        return self._effect

    def get_effect_strength(self):
        return self._effect_strength




class GameMonster(GameObject):
    def __init__(self, m_type, color, effect, behavior, start_pos, speed = 1, effect_strength = 1):
        self._type = m_type
        self._color = super()._create_color(color)
        self._effect = effect
        self._behavior = behavior
        self._previous_action = self._determine_first_action(behavior)
        self._start_pos = start_pos
        self._speed = speed
        self._effect_strength = effect_strength
        self._turn = 0

    def reset(self):
        self._turn = 0

    def _determine_first_action(self, behavior):
        return 0

    def get_color(self):
        return self._color

    def get_start_location(self):
        return self._start_pos

    def get_effect(self):
        return self._effect

    def get_effect_strength(self):
        return self._effect_strength

    def get_speed(self):
        return self._speed

    def move_action(self, location, game_map, map_size):
        new_location = location
        self._turn += 1
        if self._time_to_move():
            move_factor = math.ceil(1 / self.get_speed())
            for _ in range(0, move_factor):
                new_location = self._move_action(new_location, game_map, map_size)
        return new_location

    def _time_to_move(self):
        if self.get_speed() == 0:
            return False
        return True if self._turn % math.ceil(self.get_speed()) == 0 else False

    def _move_action(self, location, game_map, map_size):
        new_location = ()
        if self._behavior == GameFeatures.MonsterBehaviour.Nothing:
            new_location = location
        elif self._behavior == GameFeatures.MonsterBehaviour.LeftRight:
            new_location = self._move_leftRight(location, game_map, map_size)
        elif self._behavior == GameFeatures.MonsterBehaviour.UpDown:
            new_location = self._move_upDown(location, game_map, map_size)
        elif self._behavior == GameFeatures.MonsterBehaviour.DiagonalLeft:
            new_location = self._move_diagonalLeft(location, game_map, map_size)
        elif self._behavior == GameFeatures.MonsterBehaviour.DiagonalRight:
            new_location = self._move_diagonalRight(location, game_map, map_size)
        elif self._behavior == GameFeatures.MonsterBehaviour.FollowUser:
            raise Exception("Follow user is not yet implemented")    
        else:
            raise Exception("No such behavior exists for the monster type")
        return new_location

    def _move_leftRight(self, location, game_map, map_size):
        new_location = ()
        if self._previous_action == 0:
            if self._possible_to_move_left(location, game_map, map_size) == True:
                new_location = self._move_left(location)
                self._previous_action = 0
            elif self._possible_to_move_right(location, game_map, map_size) == True:
                new_location = self._move_right(location)
                self._previous_action = 1
            else:
                new_location = location
        elif self._previous_action == 1:
            if self._possible_to_move_right(location, game_map, map_size) == True:
                new_location = self._move_right(location)
                self._previous_action = 1
            elif self._possible_to_move_left(location, game_map, map_size) == True:
                new_location = self._move_left(location)
                self._previous_action = 0
            else:
                new_location = location
        return new_location

    def _move_upDown(self, location, game_map, map_size):
        new_location = ()
        if self._previous_action == 0:
            if self._possible_to_move_up(location, game_map, map_size) == True:
                new_location = self._move_up(location)
                self._previous_action = 0
            elif self._possible_to_move_down(location, game_map, map_size) == True:
                new_location = self._move_down(location)
                self._previous_action = 1
            else:
                new_location = location
        elif self._previous_action == 1:
            if self._possible_to_move_down(location, game_map, map_size) == True:
                new_location = self._move_down(location)
                self._previous_action = 1
            elif self._possible_to_move_up(location, game_map, map_size) == True:
                new_location = self._move_up(location)
                self._previous_action = 0
            else:
                new_location = location
        return new_location

    def _move_diagonalLeft(self, location, game_map, map_size):
        new_location = ()
        if self._previous_action == 0:
            if self._possible_to_move_diaLeftUp(location, game_map, map_size) == True:
                new_location = self._move_diaLeftUp(location)
                self._previous_action = 0
            elif self._possible_to_move_diaLeftDown(location, game_map, map_size) == True:
                new_location = self._move_diaLeftDown(location)
                self._previous_action = 1
            else:
                new_location = location
        elif self._previous_action == 1:
            if self._possible_to_move_diaLeftDown(location, game_map, map_size) == True:
                new_location = self._move_diaLeftDown(location)
                self._previous_action = 1
            elif self._possible_to_move_diaLeftUp(location, game_map, map_size) == True:
                new_location = self._move_diaLeftUp(location)
                self._previous_action = 0
            else:
                new_location = location
        return new_location
    
    def _move_diagonalRight(self, location, game_map, map_size):
        new_location = ()
        if self._previous_action == 0:
            if self._possible_to_move_diaRightUp(location, game_map, map_size) == True:
                new_location = self._move_diaRightUp(location)
                self._previous_action = 0
            elif self._possible_to_move_diaRightDown(location, game_map, map_size) == True:
                new_location = self._move_diaRightDown(location)
                self._previous_action = 1
            else:
                new_location = location
        elif self._previous_action == 1:
            if self._possible_to_move_diaRightDown(location, game_map, map_size) == True:
                new_location = self._move_diaRightDown(location)
                self._previous_action = 1
            elif self._possible_to_move_diaRightUp(location, game_map, map_size) == True:
                new_location = self._move_diaRightUp(location)
                self._previous_action = 0
            else:
                new_location = location
        return new_location

    def reaction_action(self, block, objects, player_interaction):
        pass





class GameItem(GameObject):
    def __init__(self, color, effect, behavior, start_pos, respawn_time = 10, effect_strength = 1):
        self._color = super()._create_color(color)
        self._effect = effect
        self._behavior = behavior
        self._start_pos = start_pos
        self._active_item = True
        self._step_since_inactivity = 0
        self._respawn_time = respawn_time
        self._effect_strength = effect_strength
        self._turn = 0

    def reset(self):
        self._active_item = True
        self._step_since_inactivity = 0
        self._turn = 0

    def is_active(self):
        return self._active_item

    def get_color(self):
        return self._color
    
    def get_start_location(self):
        return self._start_pos

    def was_active_this_round(self):
        return self._active_item or self._step_since_inactivity == 0

    def get_effect(self):
        return self._effect

    def get_effect_strength(self):
        return self._effect_strength

    def get_speed(self):
        return self._respawn_time

    def move_action(self, location, game_map, map_size):
        self._turn += 1
        new_location = ()
        if self._behavior == GameFeatures.ItemBehaviour.Respawn:
            if self._active_item == False:
                self._step_since_inactivity += 1
                new_location = (-1, -1)
            elif self._active_item == True:
                self._step_since_inactivity = 0
                new_location = self._start_pos
        elif self._behavior == GameFeatures.ItemBehaviour.Nothing:
            if self._active_item == False:
                new_location = (-1, -1)
            elif self._active_item == True:
                new_location = self._start_pos
        return new_location

    def reaction_action(self, block, objects, player_interaction):
        if self._behavior == GameFeatures.ItemBehaviour.Nothing:
            if player_interaction == True:
                self._active_item = False
        elif self._behavior == GameFeatures.ItemBehaviour.Respawn:
            if player_interaction == True:
                self._active_item = False
            elif self._step_since_inactivity >= self.get_speed():
                self._active_item = True
        else:
            raise Exception("No such behavior exists for Items")

        






class Player:
    def __init__(self, controls, survival_properties, start_pos):
        self._controls = controls 
        self._survival_properties = survival_properties
        self._start_pos = start_pos
        self._speed = 1
        self._health = 100
        self._points = 0
        self._turn = 0
        self._survival_time = 0

    def get_survival_time(self):
        return self._survival_time

    def get_controls(self):
        return self._controls

    def get_health(self):
        return self._health
    
    def get_points(self):
        return self._points

    def kill_player(self):
        self._health = 100
        self._points = 0
        self._survival_time = 0
    
    def get_feasible_controls(self, map_size, location):
        feasible_controls = []
        if self.get_controls() == GameFeatures.Controls.LeftRight:
            feasible_controls = self._feasible_leftRight(map_size, location)
        elif self.get_controls() == GameFeatures.Controls.UpDown:
            feasible_controls = self._feasible_upDown(map_size, location)
        elif self.get_controls() == GameFeatures.Controls.AllArrows:
            feasible_controls = self._feasible_allArrows(map_size, location)
        else:
            raise Exception("No Suck controls exists")
        return feasible_controls

    def _feasible_leftRight(self, map_size, location):  #0 is move nothing
       return [0, 1, 2]

    def _feasible_upDown(self, map_size, location):
        return [0, 1, 2]

    def _feasible_allArrows(self, map_size, location):
        return [0, 1, 2, 3, 4]

    def move_action(self, action, location, game_map, map_size):
        self._turn += 1
        self._survival_time += 1
        if self._time_to_move() == True:
            new_location = self._move_action(action, location, game_map, map_size)
        else:
            new_location = location
        return new_location

    def _time_to_move(self):
        for sur_prop in self._survival_properties:
            if GameFeatures.SurvivalProperty.Slowdown == sur_prop["Property"]:
                return True if self._turn % self._health_modifier(sur_prop["Strength"]) == 0 else False
        return True
    
    def _health_modifier(self, factor = 1):
        if self._health > 50:
            return 1
        elif self._health > 20:
            return 2 * factor
        elif self._health > 5:
            return 3 * factor
        else:
            return 4 * factor

    def reaction_action(self, block, game_objects):
        self._interact_with_block(block)
        for obj in game_objects:
            if isinstance(obj, GameMonster):
                self._interact_with_monster(obj)
            elif isinstance(obj, GameItem):
                self._interact_with_item(obj)
        self._health_reaction()

    def _interact_with_block(self, block):
        effect = block.get_effect()
        if effect == GameFeatures.BlockEffect.TakeLife:
            self._health -= block.get_effect_strength()
        elif effect == GameFeatures.BlockEffect.GiveLife:
            if self._health < 100:
                self._health += block.get_effect_strength()
        elif effect == GameFeatures.BlockEffect.TakePoints:
            if self._points > 0:
                self._points -= block.get_effect_strength()
        elif effect == GameFeatures.BlockEffect.GivePoints:
            self._points += block.get_effect_strength()
        elif effect == GameFeatures.BlockEffect.Nothing:
            pass
        elif effect == GameFeatures.BlockEffect.Block:
            raise Exception("Error, not possible to be on this type of Block")
        else:
            raise Exception("No such Block effect is defines")

    def _interact_with_monster(self, monster):
        effect = monster.get_effect()
        if effect == GameFeatures.MonsterEffect.Kill:
            self._health = 0
        elif effect == GameFeatures.MonsterEffect.TakeLife:
            self._health -= monster.get_effect_strength()
        elif effect == GameFeatures.MonsterEffect.GiveLife:
            if self._health < 100:
                self._health += monster.get_effect_strength()
        elif effect == GameFeatures.MonsterEffect.TakePoints:
            if self._points > 0:
                self._points -= monster.get_effect_strength()
        elif effect == GameFeatures.MonsterEffect.GivePoints:
            self._points += monster.get_effect_strength()
        elif effect == GameFeatures.MonsterEffect.Nothing:
            pass
        else:
            raise Exception("No such Monster effect is defines")

    def _interact_with_item(self, item):
        effect = item.get_effect()
        if effect == GameFeatures.ItemEffect.GiveLife:
            if self._health < 100:
                self._health += item.get_effect_strength()
        elif effect == GameFeatures.ItemEffect.TakeLife:
            self._health -= item.get_effect_strength()
        elif effect == GameFeatures.ItemEffect.GivePoints:
            self._points += item.get_effect_strength()
        elif effect == GameFeatures.ItemEffect.TakePoints:
            if self._points > 0:
                self._points -= item.get_effect_strength()
        elif effect == GameFeatures.ItemEffect.Nothing:
            pass
        else:
            raise Exception("No such Item effect is defines")

    def _health_reaction(self):
        for sur_prop in self._survival_properties:
            if GameFeatures.SurvivalProperty.Starve == sur_prop["Property"]:
                if (self._turn % sur_prop["Interval"]) == 0:
                    self._health -= sur_prop["Strength"]

    def _move_action(self, action, location, game_map, map_size):
        new_location = ()
        if action == 0:
            new_location = location
        elif self.get_controls() == GameFeatures.Controls.LeftRight:
            if action == 1:
                new_location = self._action_move_left(location, game_map, map_size)    #Move Left
            elif action == 2:
                 new_location = self._action_move_right(location, game_map, map_size)   #Move Right
        elif self.get_controls() == GameFeatures.Controls.UpDown:
            if action == 1:
                 new_location = self._action_move_up(location, game_map, map_size)   #Move Up
            elif action == 2:
                 new_location = self._action_move_down(location, game_map, map_size)   #Move Down
        elif self.get_controls() == GameFeatures.Controls.AllArrows:
            if action == 1:
                 new_location = self._action_move_up(location, game_map, map_size)   #Move Up
            elif action == 2:
                 new_location = self._action_move_down(location, game_map, map_size)   #Move Down
            elif action == 3:
                 new_location = self._action_move_left(location, game_map, map_size)   #Move Left
            elif action == 4:
                 new_location = self._action_move_right(location, game_map, map_size)   #Move Right
        else:
            raise Exception("No Suck controls exists")
        return new_location

    def _action_move_left(self, location, game_map, map_size):
        new_location = location
        if location[1] > 1:
            if game_map[(location[0], location[1]-1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block:
                new_location = (location[0], location[1]-1)
        return new_location

    def _action_move_right(self, location, game_map, map_size):
        new_location = location
        if location[1] < map_size[1]:
            if game_map[(location[0], location[1]+1)]["Object"].get_effect() != GameFeatures.BlockEffect.Block:
                new_location = (location[0], location[1]+1)
        return new_location

    def _action_move_up(self, location, game_map, map_size):
        new_location = location
        if location[0] > 1:
            if game_map[(location[0]-1, location[1])]["Object"].get_effect() != GameFeatures.BlockEffect.Block:
                new_location = (location[0]-1, location[1])
        return new_location

    def _action_move_down(self, location, game_map, map_size):
        new_location = location
        if location[0] < map_size[0]:
            if game_map[(location[0]+1, location[1])]["Object"].get_effect() != GameFeatures.BlockEffect.Block:
                new_location = (location[0]+1, location[1])
        return new_location