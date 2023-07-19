import pygame

from class_bases import *
from constants import *


class DamageChar(ActorBase):
    def __init__(self, posX: float, posY: float, damage: int):
        """A number that pops up after a player or enemy is hit that indicates how much damage that entity has taken
        
        ### Arguments
            - posX (``float``): _description_
            - posY (``float``): _description_
            - damage (``int``): _description_
        """        
        super().__init__()
        self.show(LAYER['text_layer'])
        all_font_chars.add(self)
        self.start_time = time.time()

        self.pos = vec((posX, posY))
        self.vel = vec(0, -2)

        self.image = textToImage(str(damage), "sprites/ui/font.png", 9, 14, 36)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos

    def update(self):
        self.movement()

        if getTimeDiff(self.start_time) > 0.75:
            self.kill()
