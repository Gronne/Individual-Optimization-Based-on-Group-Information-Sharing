import math
import cv2

from GameFeatures import *

class GameVisualizer:
    def _visualize_game(window, name, window_size, game_map_size, player, game_map, game_objects):
        GameVisualizer._print_game_on_window(window, window_size, game_map_size, player, game_map, game_objects)
        cv2.imshow(name, window)

    def _print_game_on_window(window, window_size, game_map_size, player, game_map, game_objects):
        block_size = GameVisualizer._calc_block_size(window_size, game_map_size)
        map_start_position = GameVisualizer._map_start_position(block_size, window_size, game_map_size)
        GameVisualizer._print_blocks(window, game_map, block_size, map_start_position)
        GameVisualizer._print_objects(window, game_objects, block_size, map_start_position)
        GameVisualizer._print_user(window, player, block_size, map_start_position)

    def _calc_block_size(window_size, game_map_size): #Blocks should be square, even if they cannot fillout the full screen = get smallest side
        side_1 = math.floor(window_size[0] / game_map_size[0])
        side_2 = math.floor(window_size[1] / game_map_size[1])
        smallest_side = side_1 if side_1 < side_2 else side_2
        return (smallest_side, smallest_side)

    def _map_start_position(block_size, window_size, game_map_size):
        height_size = block_size[0] * game_map_size[0]
        width_size = block_size[1] * game_map_size[1]
        height_leftover_pixels = window_size[0] - height_size
        width_leftover_pixels = window_size[1] - width_size
        start_height = math.floor(height_leftover_pixels / 2)
        start_width = math.floor(width_leftover_pixels / 2)
        return (start_height, start_width)

    def _print_blocks(window, game_map, block_size, map_start_position):
        for coordinate in game_map:
            block_color = game_map[coordinate]["Object"].get_color()
            start_height = map_start_position[0] + block_size[0] * (coordinate[0]-1)
            start_width = map_start_position[1] + block_size[1] * (coordinate[1]-1)
            cv2.rectangle(window, (start_width, start_height), (start_width+block_size[0], start_height+block_size[1]), block_color,-1)
            cv2.rectangle(window, (start_width, start_height), (start_width+block_size[0], start_height+block_size[1]), (0, 0, 0),1)

    def _print_objects(window, game_objects, block_size, map_start_position):
        for game_object in game_objects:
            color = game_object["Object"].get_color()
            start_height = map_start_position[0] + block_size[0] * (game_object["Location"][0]-1)
            start_width = map_start_position[1] + block_size[1] * (game_object["Location"][1]-1)
            center_coor_height = start_height + int(block_size[0]/2)
            center_coor_width = start_width + int(block_size[1]/2)
            radius = GameVisualizer._get_object_radius(game_object["Object"], block_size)
            cv2.circle(window, (center_coor_width, center_coor_height), radius,color,-1)

    def _get_object_radius(game_object, block_size):
        if isinstance(game_object, GameMonster):
            return int((block_size[0]/2)*0.8)
        elif isinstance(game_object, GameItem):
             return int((block_size[0]/2)*0.5)
        elif isinstance(game_object, Player):
             return int((block_size[0]/2)*0.9)
        else:
            raise Exception("No such object exists")

    def _print_user(window, player, block_size, map_start_position):
        start_height = map_start_position[0] + block_size[0] * (player["Location"][0]-1)
        start_width = map_start_position[1] + block_size[1] * (player["Location"][1]-1)
        center_coor_height = start_height + int(block_size[0]/2)
        center_coor_width = start_width + int(block_size[1]/2)
        radius = GameVisualizer._get_object_radius(player["Object"], block_size)
        cv2.circle(window, (center_coor_width, center_coor_height), radius,(90, 190, 40),-1)