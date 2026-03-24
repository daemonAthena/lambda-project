#pip install pygame
from numpy import empty
import pygame
import os
from constants import *
from classes import *
from graphics import *

def draw_map(surface, terrain_list):
    for point in terrain_list:
        #creates preddy grid squares to map
        grid_square=pygame.Rect(render(point[0]), render(point[1]), TILE_SIZE, TILE_SIZE)
        #draws those squares
        pygame.draw.rect(surface, terrain_list[point].color, grid_square)

def draw_grid(surface):
    for i in range(GRID_SIZE):
        #it's like the mouth of a river but it's the mouth of our line
        mouth = render(i)
        #draws lines from one end to the other based on what grid square we're on
        pygame.draw.line(surface, BLACK, (0, mouth), (SCREEN_WIDTH, mouth), 2) 
        pygame.draw.line(surface, BLACK, (mouth, 0), (mouth, SCREEN_HEIGHT), 2)

#creates a new unit using its type and ideal position
def create_unit(unit_list,color,type='basic',position=(0,0)):
    unit_list[position] = Unit(color,type,position)

#destroys the unit at the position
def destroy_unit(unit_list,position):
    unit_list[position] = ''

def combat(unit,other,advantage):
        defender_strength = other.strength + advantage
        if unit.strength >= defender_strength:
            return 'w'
    
def move_unit(unit, new_position, unit_list, terrain_list,initial_position):
    if new_position in unit.range(unit_list,terrain_list).union(unit.attack_range(unit_list,terrain_list,unit.color)):
        if unit_list[new_position] != '' and unit_list[new_position].color != unit.color:
            #combat processing
            enemy = unit_list[new_position]

            if combat(unit,enemy,terrain_list[new_position].advantage) == 'w':
                destroy_unit(unit_list,new_position)
            else:
                destroy_unit(unit_list,unit.position)
                return

        unit.movement -= distance(unit.position,new_position)
        unit.position = new_position
        unit_list[initial_position] = ''
        unit_list[unit.position] = unit
        


def end_turn(color_controller,unit_list):
    for index in unit_list:
        if unit_list[index] != '':
            unit = unit_list[index]
            unit.movement = mobility_types[unit.type]

    if color_controller == 'red':
        return (GRID_SIZE-1,GRID_SIZE-1)

    if color_controller == 'blue':
        return (0,0)



def game_loop(surface, unit_list, terrain_list):
#creates a loop so the game won't stop running until the player inputs something
    x,y = 0,0
    cursor=YELLOW_CURSOR

    color_controller = 'red'
    selection = ''

    clock=pygame.time.Clock()

    while True:
        #it's more efficient to store (x,y) as abstract points and render (see render function for more details)
        pixex = render(x)
        pixey = render(y)
        dx,dy = 0,0
        #this loop also allows the calling of events using player input using the event.get method
        for event in pygame.event.get():
            #this lets the player quit the game if they x out or press esc
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #events for if you press a key down
            if event.type == pygame.KEYDOWN:
                #exit loop
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #cursor movement
                if event.key == pygame.K_RIGHT and pixex < SCREEN_WIDTH - TILE_SIZE:
                    dx = 1
                if event.key == pygame.K_LEFT and pixex > 0:
                    dx = -1
                if event.key == pygame.K_UP and pixey > 0:
                    dy = -1
                if event.key == pygame.K_DOWN and pixey < SCREEN_HEIGHT - TILE_SIZE:
                    dy = 1
                #selection events  
                if event.key == pygame.K_z and selection =='':
                    if unit_list[(x,y)] != '' and unit_list[(x,y)].color == color_controller:
                        cursor = BLUE_CURSOR
                        selection = unit_list[(x,y)]
                        #without this variable the object would stay in one spot
                        initial_position = selection.position
                #selection movement
                if event.key == pygame.K_z and selection != '' and (x,y) != initial_position:
                    #changes unit position
                    move_unit(unit= selection,new_position= (x,y), unit_list= unit_list, terrain_list= terrain_list,initial_position=initial_position)
                    #changes cursor
                    cursor = YELLOW_CURSOR
                    #deselection
                    selection = ''

                #deselect
                if event.key == pygame.K_x:
                    cursor = YELLOW_CURSOR
                    selection = ''

                #unit builder
                #if event.key == pygame.K_z and (x,y) == (0,0):
                    #menu()

                #spawns unit for debugging purposes
                if event.key == pygame.K_LSHIFT:
                    create_unit(unit_list,color= color_controller,type= 'basic',position= (x,y))
                #kills the unit on a square
                if event.key == pygame.K_RSHIFT:
                    destroy_unit(unit_list,(x,y))
                #ends turn
                if event.key == pygame.K_RETURN:
                    (x,y) = end_turn(color_controller,unit_list)
                    if color_controller == 'red':
                        color_controller = 'blue'
                    else:
                        color_controller = 'red'
        draw_map(surface,terrain_list)
        draw_grid(surface)
            #updates positions
        x += dx
        y += dy
            #now that the positions are updated we can display the cursor on screen!
        surface.blit(cursor,render((x,y)))
        #blits all units currently on the unit list
        for unit in unit_list.values():
            if unit != '':
                surface.blit(unit.image,render(unit.position))

        if selection != '':
            #attack sqaures
            attack_set = selection.attack_range(unit_list,terrain_list,color_controller)
            for position in attack_set:
                surface.blit(ATTACK_TILE,render(position))

            #render movement squares
            for position in selection.range(unit_list,terrain_list):
                surface.blit(MOVEABLE_TILE,render(position))

        #the frequency of screen updates is controlled by framerate using the clock.tick method
        clock.tick(60)
        #finally, the update method updates the window with any new changes
        pygame.display.update()

def initialize_game():
#creates a screen for us to view the game, ugly pink is used for debugging missing tiles
    pygame.init()
    #the set_mode method of the display class lets us create a window W x H resolution
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    #the fill method fills the window with a color
    surface.fill(UGLY_PINK)
    return surface


def map_terrain_objects(map):
    terrain_list = {}
    #emumerate helps us turn our map file into a cartesian grid
    for y,line in enumerate(map):
        for x,square in enumerate(line):
            #the terrain type is defined by the character of the square from the map we plug in
            #we add each terrain object to a dictionary that we give as the output
            terrain_list[(x,y)] = Terrain(type= square, position= (x,y))
    return terrain_list

def map_unit_objects(point_set):
    #creates an empty list ready to be filled with unit objects
    unit_list = {}
    for point in point_set:
        unit_list[point] = ''

    return unit_list

def read_map(mapfile):
    #used for reading map files so the program knows what the map layout should be
    with open(mapfile, 'r') as f:
        world_map=f.readlines()
    world_map=[line.strip() for line in world_map]
    return world_map

def define_points():
    #takes two integers in a tuple (i,j) where 0<=i<=11 and 0<=j<=11
    #these will be our coordinate points
    point_set = set()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            new_point = (j,i)
            point_set.add(new_point)
    
    return point_set

def main():
#our two types of point sets
    #one for when we want to apply distance in our game's units
    point_set = define_points()

#gives us all the lines of our world map in a list
    world_map = read_map(MAPFILE)

#creates a dictionary of units at points
    unit_list = map_unit_objects(point_set)

#this is how we get a list of terrain objects with attributes relative to our map
    terrain_list = map_terrain_objects(world_map)

#creates a window for us to render objects on
    surface = initialize_game()

#now like soup we mix them all together in our game loop
    game_loop(surface, unit_list, terrain_list)

if __name__=='__main__':
    #by existing as main it shall run
    main()
