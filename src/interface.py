import pygame
from pygame.locals import *
from pygame import mixer
import pandas as pd
import time
from map_model import Map
import sys
import numpy as np
from spritesheet import Spritesheet
from astar import Astar
from pathlib import Path


WINDOW_HEIGHT = 0
WINDOW_WIDTH = 0
SCREEN = 0
blockSize = 16 #Set the size of the grid block
input_path = Path(__file__).parents[1].joinpath('input')
img_path = Path(__file__).parents[1].joinpath('imagens')
map_list = 0
sprite_index = 0
trainer_sprites = []
running = True
open_nodes = []
closed_nodes = []
best_path = []
aStar_struct = []


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

    dict_sprites = {'M' : (192/2,480/2,blockSize,blockSize),
                    'R' : (64/2,0,blockSize,blockSize),
                    'I' : (192/2,0,blockSize,blockSize),
                    'F' : (128/2,0,blockSize,blockSize)
                    }

    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            sprite_crop = dict_sprites.get(map_list[y][x],(32/2,0,blockSize,blockSize))
            SCREEN.blit(tiles_src,(x*blockSize,y*blockSize),sprite_crop)


def setupBattles():
    global map_list
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    #create list of cordinates of battles to draw pokeballs
    battle_list = []

    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x][0] == 'B':
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

def drawBattles(battle_list,trainers_list):
    #draw each trainer in coordinate
    i = -1

    for coordinates in battle_list:
        coordinates = scaleCoordinates(coordinates)
        coordinates[1] = coordinates[1] - blockSize/2 #raises trainer by half blocksize to level to ground
        SCREEN.blit(trainers_list[i],coordinates,(0,0,blockSize, 3/2 * blockSize))
        i = i - 1
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

