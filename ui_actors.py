import pygame, time
from pygame.locals import *

from math import floor

from init import *
from class_bases import StatBarBase
from constants import *
from groups import all_sprites, all_stat_bars
from spritesheet import Spritesheet

vec = pygame.math.Vector2


class HealthBar(StatBarBase):
    def __init__(self, entity):
        super().__init__()
        self.show(LAYER['statBar_layer'])
        all_stat_bars.add(self)
        
        self.entity = entity

        self.spritesheet = Spritesheet("sprites/stat_bars/health_bar.png", False)
        self.images = self.spritesheet.get_images(0, 0, 128, 16, 18)
        self.original_images = self.spritesheet.get_images(0, 0, 128, 16, 18)
        self.index = 17

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.rect = pygame.Rect(0, 0, 128, 16)
        
        self.pos = self.entity.pos

    def movement(self):
        self.rect.center = vec(self.entity.pos.x, self.entity.pos.y + 42)

    def update(self):
        self.movement()

        if self.entity.hp > 0:
            self.index = floor((16 * self.entity.hp) / self.entity.max_hp)
            self.image = self.images[self.index]
            self.original_image = self.original_images[self.index]
            self.rect = self.image.get_rect(center = self.rect.center)

        else:
            self.index = 17
            self.image = self.images[self.index]
            self.kill()


class DodgeBar(StatBarBase):
    def __init__(self, entity):
        super().__init__()
        all_sprites.add(self, layer = LAYER['statBar_layer'])
        all_stat_bars.add(self)

        self.spritesheet = Spritesheet("sprites/stat_bars/dodge_bar.png", False)
        self.images = self.spritesheet.get_images(0, 0, 128, 16, 18)
        self.original_images = self.spritesheet.get_images(0, 0, 128, 16, 18)
        self.index = 17

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.rect = pygame.Rect(0, 0, 128, 16)
        self.entity = entity
        self.pos = self.entity.pos
    
    def movement(self):
        self.rect.center = vec(self.entity.pos.x, self.entity.pos.y + 60)

    def update(self):
        self.movement()

        if self.entity.hp > 0:
            if self.entity.hitTime < self.entity.hitTime_charge:
                self.index = floor((17 * self.entity.hitTime) / self.entity.hitTime_charge)
                self.image = self.images[self.index]
                self.original_image = self.original_images[self.index]
                self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.index = 17
            self.image = self.images[self.index]
            self.kill()
