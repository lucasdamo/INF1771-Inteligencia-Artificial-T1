#https://www.youtube.com/watch?v=ePiMYe7JpJo&t=0s
#https://github.com/ChristianD37/YoutubeTutorials/tree/master/spritesheet

import pygame
import json

BLACK = (0, 0, 0)

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)
        self.sprite_sheet_dimensions = self.sprite_sheet.get_rect()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,(self.sprite_sheet_dimensions.bottomright[0]//2,self.sprite_sheet_dimensions.bottomright[1]//2))
        self.meta_data = str(self.filename).replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey(BLACK)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image