import pygame
import pandas as pd
import time 


class TravelMapInterface:
    def __init__(self, map:pd.DataFrame):
        pygame.init()
        self.screen = pygame.display.set_mode((420, 420))

    def update(self):
        pygame.display.update()


def draw_grid(map, width, height, spacing=2, **kwargs):
    for y in range(height):
        for x in range(width):
            print('%%-%ds' % spacing % draw_tile(map, (x, y), kwargs), end='')
        print()

def draw_tile(map, coordinates, kwargs):
    
    # Get the map value
    value = map._get_unique_point(coordinates)
    # Check if we should print the path
    if 'path' in kwargs and coordinates in kwargs['path']: value = '+'
    # Check if we should print start point
    if 'start' in kwargs and coordinates == kwargs['start']: value = '@'
    # Check if we should print the goal point
    if 'goal' in kwargs and coordinates == kwargs['goal']: value = '$'
    # Return a tile value
    return value 

    
        

t = TravelMapInterface(pd.DataFrame({}))