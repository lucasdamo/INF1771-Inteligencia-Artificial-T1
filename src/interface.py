import pygame
from pygame.locals import *
from pygame import mixer
import pandas as pd
import time
from controllers import Map
import sys
import numpy as np
from spritesheet import Spritesheet
from astar import Astar
from pathlib import Path

BLACK = (0, 0, 0)
GREY = (160,160,160)
WHITE = (200, 200, 200)
RED = (255,0,0)
WINDOW_HEIGHT = 0
WINDOW_WIDTH = 0
SCREEN = 0
blockSize = 16 #Set the size of the grid block
input_path = Path(__file__).parents[1].joinpath('input')
img_path = Path(__file__).parents[1].joinpath('imagens')
sound_path = Path(__file__).parents[1].joinpath('sound')
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

    pandas_map = Map(input_path.joinpath("map.csv"),input_path.joinpath("cellweights.csv"))

    aStar_struct = Astar(pandas_map)

    WINDOW_HEIGHT  = pandas_map.xlen * blockSize # blocksize in px * tiles for map = size of window 
    WINDOW_WIDTH = pandas_map.ylen * blockSize
    map_list = pandas_map.map.values.tolist()


    #initialize visual componets
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Pokémon IA')
    trainer_sprites = setupTrainer()
    trainer_sprite_index = 0
    pokeball_sprites = setupPokeballPath()
    trainer_pokeball_index = 0
    #invert position because map is inverted
    player_position = (pandas_map.start_point[1],pandas_map.start_point[0])
    
    battle_list,trainers_list = setupBattles()

    while running:
        checkEvents()
        drawGrid()
        drawBattles(battle_list,trainers_list)
        drawTrainer(trainer_sprites,trainer_sprite_index,player_position)
        drawAstar(open_nodes,closed_nodes)
        drawPokeballPath(pokeball_sprites,trainer_pokeball_index,best_path)
        pygame.display.update()
        trainer_pokeball_index = (trainer_pokeball_index + 1) % 8
        clock.tick(60) #60 FPS

def checkEvents():
    global sprite_index
    global trainer_sprites

    global open_nodes
    global closed_nodes
    global best_path
    global aStar_struct

    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        aStar_struct.advance(1)
        best_path,open_nodes,closed_nodes = aStar_struct.get_visual_elements()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                aStar_struct.solve()
            best_path,open_nodes,closed_nodes = aStar_struct.get_visual_elements()
                
                

def drawGrid():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global map_list
    global SCREEN
    tiles_src = pygame.image.load(img_path.joinpath("BW_PublicOutside_New.png"))
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
    

    trainers_list = [
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar001.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar002.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar003.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar004.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar011.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar014.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar016.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar024.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar031.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar056.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar065.png'))),
        scaleToBlocksize(pygame.image.load(img_path.joinpath( 'trchar066.png')))
    ]

    return battle_list, trainers_list


    #TODO:make routine to remove coordinates from list if battle is won

def drawBattles(battle_list,trainers_list):
    #draw pokeballs of battles yet to occur
    i = 0
    for coordinates in battle_list:
        coordinates = scaleCoordinates(coordinates)
        coordinates[1] = coordinates[1] - blockSize/2 #raises trainer by half blocksize to level to ground
        SCREEN.blit(trainers_list[i],coordinates,(0,0,blockSize, 3/2 * blockSize))
        i = i + 1
    
    #draw each trainer in coordinate
    return

def setupTrainer():
    trainer_file = 'trchar000.png'
    trainer_spritesheet = Spritesheet(img_path.joinpath( trainer_file))
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

def setupPokeballPath():
    pokeball_file = 'ball_00.png'
    pokeball_spritesheet = Spritesheet(img_path.joinpath( pokeball_file))
    pokeball_list = [
        pokeball_spritesheet.parse_sprite('pokeball1.png'),
        pokeball_spritesheet.parse_sprite('pokeball2.png'),
        pokeball_spritesheet.parse_sprite('pokeball3.png'),
        pokeball_spritesheet.parse_sprite('pokeball4.png'),
        pokeball_spritesheet.parse_sprite('pokeball5.png'),
        pokeball_spritesheet.parse_sprite('pokeball6.png'),
        pokeball_spritesheet.parse_sprite('pokeball7.png'),
        pokeball_spritesheet.parse_sprite('pokeball8.png'),
    ]
    return pokeball_list

def drawTrainer(trainer_sprites,index,player_position):
    global SCREEN
    player_position = scaleCoordinates(player_position)
    player_position[1] = player_position[1] - blockSize/2 #raises trainer by half blocksize to level to ground
    SCREEN.blit(trainer_sprites[index],player_position)
    return

def drawPokeballPath(pokeball_sprites,trainer_pokeball_index,best_path):
    global SCREEN

    index = trainer_pokeball_index

    for coordinates in best_path[:-1]: #won't show the ball on trainer
        coordinates = scaleCoordinates(coordinates)
        coordinates[0] = coordinates[0] + blockSize/4 #moves ball by half blocksize to center to ground
        SCREEN.blit(scaleToBlocksize(pokeball_sprites[index]),coordinates)
        index = (index + 1) % 8
    return 

def drawAstar(open_nodes,closed_nodes):
    global SCREEN

    open_node_img = 'safari_bait.png'

    closed_node_img = 'safari_rock.png'


    open_node_src = pygame.image.load(img_path.joinpath( open_node_img))
    open_node_src = scaleToBlocksize(scaleToBlocksize(open_node_src))
    
    closed_node_src = pygame.image.load(img_path.joinpath( closed_node_img))
    closed_node_src = scaleToBlocksize(scaleToBlocksize(closed_node_src))


    for node_coordinates in open_nodes:
        node_coordinates = scaleCoordinates(node_coordinates)
        node_coordinates[0] = node_coordinates[0] + blockSize/4 #moves ball by half blocksize to center to ground
        SCREEN.blit(open_node_src,node_coordinates,(0,0,blockSize,blockSize))
    

    for node_coordinates in closed_nodes:
        node_coordinates = scaleCoordinates(node_coordinates)
        node_coordinates[0] = node_coordinates[0] + blockSize/4 #moves ball by half blocksize to center to ground
        SCREEN.blit(closed_node_src,node_coordinates,(0,0,blockSize,blockSize))
    return


# since all sprites are 16 bits we scale down to fit the screen
def scaleToBlocksize(image):
    image_dimensions = image.get_rect()
    return pygame.transform.scale(image,(image_dimensions.bottomright[0]//2,image_dimensions.bottomright[1]//2))

def scaleCoordinates(coordinates):
    coordinates = list([blockSize*x for x in coordinates])
    return coordinates

main()