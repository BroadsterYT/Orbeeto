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
        
        self.start = time.time()
        self.pos = vec((posX, posY))

        self.image = textToImage(str(damage), "sprites/ui/font.png", 9, 14, 36)
        self.setRects(self.pos.x, self.pos.y, 9, 14, 9, 14)

    def movement(self):
        self.accel = vec(0, 0)
        if getTimeDiff(self.start) < 0.1:
            self.accel = vec(0, -1)

        self.accelMovement()

    def update(self):
        self.movement()

        if getTimeDiff(self.start) > 0.6:
            self.kill()
