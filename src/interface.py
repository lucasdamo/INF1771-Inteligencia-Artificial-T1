import pygame
import pandas as pd


class TravelMapInterface:
    def __init__(self, map:pd.DataFrame):
        pygame.init()
        self.screen = pygame.display.set_mode((420, 420))

    def update(self):
        pygame.display.update()

    
        

t = TravelMapInterface()