import pygame
import os
from constants import *

'''Image Paths'''
# --- GAME OBJECTS ---
YELLOW_CURSOR = pygame.image.load(os.path.join('assets','graphics','cursor.png'))
BLUE_CURSOR = pygame.image.load(os.path.join('assets','graphics','selector.png'))
MOVEABLE_TILE = pygame.image.load(os.path.join('assets','graphics','moveable_tile.png'))
ATTACK_TILE = pygame.image.load(os.path.join('assets','graphics','attack_tile.png'))

# --- UNIT IMAGE FILE PATHS ---
R_BASIC = pygame.image.load(os.path.join('assets','graphics','red_unit.png'))
B_BASIC = pygame.image.load(os.path.join('assets','graphics','blue_unit.png'))
R_FAIRY = pygame.image.load(os.path.join('assets','graphics','red_fairy.png'))
B_FAIRY = pygame.image.load(os.path.join('assets','graphics','blue_fairy.png'))


#Image dictionaries for when images are needed based on type
red_units = {'basic':R_BASIC,'fairy':R_FAIRY}
blue_units = {'basic':B_BASIC,'fairy':B_FAIRY}
flora = {}