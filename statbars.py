import pygame
from pygame.locals import *

from math import floor

from init import *
from class_bases import ActorBase
from constants import *
from groups import all_sprites, all_stat_bars
from spritesheet import Spritesheet


class StatBarBase(ActorBase):
    def __init__(self):
        super().__init__()


class HealthBar(StatBarBase):
    def __init__(self, owner):
        super().__init__()
        self.show(LAYER['statBar_layer'])
        all_stat_bars.add(self)
        
        self.owner = owner
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42)

        self.setImages('sprites/stat_bars/health_bar.png', 128, 16, 1, 17, 0, 16)
        self.setRects(self.pos.x, self.pos.y, 128, 16, 128, 16)

    def movement(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            self.index = floor((16 * self.owner.hp) / self.owner.maxHp)
            self.renderImages()
        else:
            self.kill()


class DodgeBar(StatBarBase):
    def __init__(self, owner):
        super().__init__()
        self.show(LAYER['statBar_layer'])
        all_stat_bars.add(self)

        self.owner = owner
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 60)

        self.setImages('sprites/stat_bars/dodge_bar.png', 128, 16, 1, 17, 0, 16)
        self.setRects(self.pos.x, self.pos.y, 128, 16, 128, 16)
    
    def movement(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 60)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            if self.owner.hitTime < self.owner.hitTimeCharge:
                self.index = floor((16 * self.owner.hitTime) / self.owner.hitTimeCharge)
                self.renderImages()
        else:
            self.kill()


class AmmoBar(StatBarBase):
    def __init__(self, owner):
        super().__init__()
        self.show(LAYER['statBar_layer'])
        all_stat_bars.add(self)

        self.owner = owner
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 78)

        self.setImages('sprites/stat_bars/ammo_bar.png', 128, 16, 1, 17, 0, 16)
        self.setRects(self.pos.x, self.pos.y, 128, 16, 128, 16)

    def movement(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 78)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            self.index = floor((16 * self.owner.ammo) / self.owner.maxAmmo)
            self.renderImages()
        else:
            self.kill()