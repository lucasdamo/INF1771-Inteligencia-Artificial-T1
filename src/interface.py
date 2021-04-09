import pygame
from pygame.locals import *
import pandas as pd
import time
from controllers import Map
import sys
import numpy as np
from spritesheet import Spritesheet
from astar import Astar

BLACK = (0, 0, 0)
GREY = (160,160,160)
WHITE = (200, 200, 200)
RED = (255,0,0)
WINDOW_HEIGHT = 0
WINDOW_WIDTH = 0
SCREEN = 0
blockSize = 16 #Set the size of the grid block
pokeball_img = 'pokeball.ico'
path = "input/"
img_path = "imagens/"
map_list = 0
sprite_index = 0
trainer_sprites = []
running = True
open_nodes = []
closed_nodes = []
best_path = []
aStar_struct = []

 # https://stackoverflow.com/questions/38535330/load-only-part-of-an-image-in-pygame
 # https://stackoverflow.com/questions/27867073/how-to-put-an-image-onto-a-sprite-pygame

def main():
    global SCREEN
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global map_list
    global sprite_index
    global trainer_sprites
    global aStar_struct

    #Create map 
    map_path = "map.csv"
    cellweights_path = "cellweights.csv"
    pandas_map = Map(path + map_path,path + cellweights_path)

    aStar_struct = Astar(pandas_map)

    WINDOW_HEIGHT  = pandas_map.xlen * blockSize # blocksize in px * tiles for map = size of window 
    WINDOW_WIDTH = pandas_map.ylen * blockSize
    map_list = pandas_map.map.values.tolist()


    #initialize visual componets
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Pokémon IA')
    trainer_sprites = setupTrainer()
    #invert position because map is inverted
    player_position = (pandas_map.start_point[1],pandas_map.start_point[0])
    sprite_index = 0
    battle_list = setupBattles()

    while running:
        checkEvents()
        drawGrid()
        drawBattles(battle_list)
        drawTrainer(trainer_sprites,sprite_index,player_position)
        drawAstar(open_nodes,closed_nodes,best_path)
        pygame.display.update()

def checkEvents():
    global sprite_index
    global trainer_sprites

    global open_nodes
    global closed_nodes
    global best_path
    global aStar_struct

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                aStar_struct.advance(1)
                open_nodes = aStar_struct.get_all_open_nodes()
                closed_nodes = aStar_struct.get_all_closed_nodes()
                best_path = aStar_struct.get_best_path()
                

def drawGrid():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global map_list
    global SCREEN
    tiles_src = pygame.image.load(img_path +  "BW_PublicOutside_New.png")
    tiles_src = scaleToBlocksize(tiles_src)
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] == 'M':
                sprite_crop = (192/2,480/2,blockSize,blockSize)
            elif map_list[y][x] == 'R':
                sprite_crop = (64/2,0,blockSize,blockSize)
            elif map_list[y][x] == '.':
                sprite_crop = (32/2,0,blockSize,blockSize)
            elif map_list[y][x] == 'B':
                sprite_crop = (32/2,0,blockSize,blockSize)
            elif map_list[y][x] == 'I':
                sprite_crop = (192/2,0,blockSize,blockSize)
            elif map_list[y][x] == 'F':
                sprite_crop = (128/2,0,blockSize,blockSize)
            SCREEN.blit(tiles_src,(x*blockSize,y*blockSize),sprite_crop)


def setupBattles():
    global map_list
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    #create list of cordinates of battles to draw pokeballs
    battle_list = []
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] == 'B':
                battle_list.append((x,y))
    return battle_list
    #TODO:make routine to remove coordinates from list if battle is won

def drawBattles(battle_list):
    #draw pokeballs of battles yet to occur
    pokeball_src = pygame.image.load(img_path + pokeball_img)
    pokeball_src = scaleToBlocksize(pokeball_src)
    for (x,y) in battle_list:
        x = x*blockSize
        y = y*blockSize
        SCREEN.blit(pokeball_src,(x,y),(0,0,blockSize,blockSize))
    return

def setupTrainer():
    trainer_file = 'trchar000.png'
    trainer_spritesheet = Spritesheet(img_path + trainer_file)
    trainer_list = [
        trainer_spritesheet.parse_sprite('trainerD1.png'),
        trainer_spritesheet.parse_sprite('trainerD2.png'),
        trainer_spritesheet.parse_sprite('trainerD3.png'),
        trainer_spritesheet.parse_sprite('trainerD4.png'),
        trainer_spritesheet.parse_sprite('trainerL1.png'),
        trainer_spritesheet.parse_sprite('trainerL2.png'),
        trainer_spritesheet.parse_sprite('trainerL3.png'),
        trainer_spritesheet.parse_sprite('trainerL4.png'),
        trainer_spritesheet.parse_sprite('trainerR1.png'),
        trainer_spritesheet.parse_sprite('trainerR2.png'),
        trainer_spritesheet.parse_sprite('trainerR3.png'),
        trainer_spritesheet.parse_sprite('trainerR4.png'),
        trainer_spritesheet.parse_sprite('trainerU1.png'),
        trainer_spritesheet.parse_sprite('trainerU2.png'),
        trainer_spritesheet.parse_sprite('trainerU3.png'),
        trainer_spritesheet.parse_sprite('trainerU4.png'),
    ]
    return trainer_list

def drawTrainer(trainer_list,index,player_position):
    global SCREEN
    player_position = list([blockSize*x for x in player_position])
    player_position[1] = player_position[1] - blockSize/2 #raises trainer by half blocksize to level to ground
    SCREEN.blit(trainer_list[index],player_position)

def drawAstar(open_nodes,closed_nodes,best_path):
    global SCREEN

    stubRect = pygame.Surface((blockSize,blockSize))

    stubRect.fill(WHITE)

    for node_coordinates in open_nodes:
        node_coordinates = scaleCoordinates(node_coordinates)
        SCREEN.blit(stubRect,node_coordinates)
    
    stubRect.fill(BLACK)
    
    for node_coordinates in closed_nodes:
        node_coordinates = scaleCoordinates(node_coordinates)
        SCREEN.blit(stubRect,node_coordinates)

    stubRect.fill(RED)
    
    for node_coordinates in best_path:
        node_coordinates = scaleCoordinates(node_coordinates)
        SCREEN.blit(stubRect,node_coordinates)
    return

# since all sprites are 16 bits we scale down to fit the screen
def scaleToBlocksize(image):
    image_dimensions = image.get_rect()
    return pygame.transform.scale(image,(image_dimensions.bottomright[0]//2,image_dimensions.bottomright[1]//2))

def scaleCoordinates(coordinates):
    coordinates = list([blockSize*x for x in coordinates])
    return coordinates

main()