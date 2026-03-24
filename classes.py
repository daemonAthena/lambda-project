import pygame
import sys
from constants import *
from graphics import *
from math import *



def form(point= (0,0)):
    #returns a rendered point transformed back into an abstract point
    #named after Plato's world of forms
    #must not use unless necessary division is harder than multiplying
    return (point[0]//TILE_SIZE,point[1]//TILE_SIZE)

def render(position= (0,0)):
    #this was necessary since a custom Point class won't work for some reason (believe me I tried)
    if type(position) == tuple:
        return (position[0]*TILE_SIZE,position[1]*TILE_SIZE)
    elif type(position) == int or type(position) == float:
        return position * TILE_SIZE

def distance(distance1=(0,0),distance2=(0,0)):
    #the distance formula, used to find the distance between two cartesian points
    return sqrt((distance2[0]-distance1[0])**2 + (distance2[1]-distance1[1])**2)

def min_distance(points=set,end=(0,0)):
    #very helpful
    minimum = GRID_SIZE
    for p in points:
        if distance(p,end) <= minimum:
            minimum = distance(p,end)
            minp = p
    return minp

def add_point(point=(0,0),s=0,direction='down'):
    #returns a line of vertices going a particular direction
    point_set = set()
    if direction == 'down':
        for i in range(1,s):
            point_set.add((point[0],point[1]+i))
    elif direction == 'up':
        for i in range(1,s):
            point_set.add((point[0],point[1]-i))
    elif direction == 'left':
        for i in range(1,s):
            point_set.add((point[0]-i,point[1]))
    elif direction == 'right':
        for i in range(1,s):
            point_set.add((point[0]+i,point[1]))
    return point_set

def get_ring(point=(0,0),n=1):
    #returns a ring distance n away
    #an n-ring has 8n vertices surrounding the center
    #take the corner points ex. (-1,-1),(1,1),(-1,1),(1,-1)
    #add the amount to them
    x = point[0]
    y = point[1]
    corners = [(x+n,y+n),(x-n,y+n),(x+n,y-n),(x-n,y-n)]
    ring_set = set(corners)
    ring_set =ring_set.union(add_point(corners[0],2*n,'up'))
    ring_set =ring_set.union(add_point(corners[0],2*n,'left'))
    ring_set =ring_set.union(add_point(corners[3],2*n,'down'))
    ring_set =ring_set.union(add_point(corners[3],2*n,'right'))
    return ring_set

def create_route(start=(0,0),finish=(0,0)):
    #takes two points and returns the direct path as a list
    path = [start]
    r = int(distance(start,finish))
    for i in range(1,r):
        path.append(min_distance(get_ring(start,i),finish))

    if finish not in path:
        path.append(finish)

    return path

class Game:
    def __init__(self):
        self.init_pygame()
        self.all_sprites=pygame.sprite.Group()
        #---------------
        self.keep_looping=True
        #---------------

#terrain dictionaries
colors = {'.':GREEN,'t':DARKGREEN,'n':BROWN,'w':LIGHT_BLUE,'1':RED,'2':BLUE}
penalties = {'.':0,'t':1,'n':1,'w':3,'1':0,'2':0}
advantages = {'.':0,'t':1,'n':1,'w':0,'1':1,'2':1}

class Terrain:
    def __init__(self,type,position):
        self.type = type
        self.position = position
        #since the position cannot change this is fine
        self.render = render(position)
        self.color = colors[type]
        self.penalty = penalties[type]
        self.advantage = advantages[type]
    def __repr__(self) -> str:
        return f'{self.type}'

#unit dictionaries
mobility_types={'basic':2,'fairy':4}
strength_types={'basic':2,'fairy':1}

class Unit:
    def __init__(self,color,type,position=(0,0)):
        self.color = color
        self.type = type
        self.position = position

        self.movement = mobility_types[self.type]
        self.strength = strength_types[self.type]
        #since the graphics differ this had to be split up into if
        if self.color == 'red':
            self.image = red_units[self.type]
        elif self.color == 'blue':
            self.image = blue_units[self.type]

    def range(self,unit_list,terrain_list):
        #range is not dictated by terrain for fairies
        range_set = set()
        if self.type == 'fairy':
            for position in unit_list:
                if unit_list[position] == '' and distance(position,self.position) <= self.movement:
                    range_set.add(position)
            return range_set
        else:
            for position in unit_list:
                # if the position is empty and in movement range
                if unit_list[position] == '' and distance(position,self.position) <= self.movement:
                    path = create_route(self.position,position)
                    tmprng = self.movement
                    # if we can get through the whole path from A to B
                    # without running out of movement we add
                    for i in range(1,len(path)):
                        penalty = terrain_list[path[i]].penalty
                        tmprng += -(1 + penalty)

                    if tmprng >= 0:
                        range_set.add(position)
            return range_set

    def attack_range(self,unit_list,terrain_list,color):
        #range is not dictated by terrain for fairies
        range_set = set()
        if self.type == 'fairy':
            for position in unit_list:
                if unit_list[position] != '' and unit_list[position].color != color and distance(position,self.position) <= self.movement:
                    range_set.add(position)
            return range_set
        else:
            for position in unit_list:
                # if the position is empty and in movement range
                if unit_list[position] != '' and unit_list[position].color != color and distance(position,self.position) <= self.movement:
                    path = create_route(self.position,position)
                    tmprng = self.movement
                    # if we can get through the whole path from A to B
                    # without running out of movement we add
                    for i in range(1,len(path)):
                        penalty = terrain_list[path[i]].penalty
                        tmprng += -(1 + penalty)

                    if tmprng >= 0:
                        range_set.add(position)
            return range_set