import os
import pygame

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
TITLE = "The Lambda Project"
# ----
GRID_SIZE=12
# ----
TILE_SIZE = 64
SCREEN_WIDTH = TILE_SIZE * GRID_SIZE
SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
FRAME_RATE = 20
# ----

# ---- COLORS ----
UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
GREEN = (0, 200, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURBLE = (255, 153, 255)
LIGHT_BLUE = (135,206,235)
ORANGE = (255, 128, 0)
PURPLE = (128,  0, 128)
# ----
BG_COLOR = UGLY_PINK

# ---- FILES ----
MAPFILE = "map"


# ---- ENVIRONMENT ----
GRASS_IMG = "grass.png"
HILL_IMG = "hill.png"
RIVER_IMG = 'river.png'
TREE_IMG = 'tree.png'


# ---- PLAYER ----
PLAYER_ORIGINAL_DATA_FILE = "player_original_data_file.txt"
PLAYER_DATA_FILE = "player_data_file.txt"
PLAYER1_IMG = 'blue_capital.png'
PLAYER1_IMG_DEAD = 'blue_capital_destroyed.png'
PLAYER2_IMG = 'red_capital.png'
PLAYER2_IMG_DEAD = 'red_capital_destroyed.png'

