import pygame
import os
from pygame.locals import *

from math import floor, ceil

from init import *
from class_bases import ActorBase
from constants import *
from groups import all_stat_bars


class StatBarBase(ActorBase):
    def __init__(self, owner, order: int):
        super().__init__()
        self.show(LAYER['statbar'])
        all_stat_bars.add(self)
        self.owner = owner

        self.order = order
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)
        self.ownerPos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)

        self.cAccel = 0.58

        if isinstance(self, HealthBar):
            self.setImages('sprites/stat_bars/health_bar.png', 128, 16, 1, 17, 0, 16)
        elif isinstance(self, DodgeBar):
            self.setImages('sprites/stat_bars/dodge_bar.png', 128, 16, 1, 17, 0, 16)
        elif isinstance(self, AmmoBar):
            self.setImages('sprites/stat_bars/ammo_bar.png', 128, 16, 1, 17, 0, 16)
        else:
            raise TypeError()
        
        self.setRects(self.pos.x, self.pos.y, 128, 16, 128, 16)

        self.number = BarNumbers(self)

    def movement(self):
        if self.pos != vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18):
            if self.pos.x < self.owner.pos.x:
                self.accel.x = self.cAccel
            elif self.pos.x > self.owner.pos.x:
                self.accel.x = -self.cAccel

            if self.pos.y < self.owner.pos.y + (42 + self.order * 18):
                self.accel.y = self.cAccel
            elif self.pos.y > self.owner.pos.y + (42 + self.order * 18):
                self.accel.y = -self.cAccel
        
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        self.accelMovement()


class BarNumbers(ActorBase):
    def __init__(self, bar):
        super().__init__()
        self.show(LAYER['statbar'])
        all_stat_bars.add(self)
        
        self.bar = bar
        self.owner = self.bar.owner

        self.renderImages()
        self.setRects(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height(), self.image.get_width(), self.image.get_height())

        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)

    def renderImages(self):
        if isinstance(self.bar, HealthBar):
            self.image = textToImage(str(self.owner.hp) + '/' + str(self.owner.maxHp), 'sprites/ui/small_font.png', 5, 7, 37)

        elif isinstance(self.bar, DodgeBar):
            self.image = textToImage(str(self.owner.hitTime) + '/' + str(self.owner.hitTimeCharge), 'sprites/ui/small_font.png', 5, 7, 37)

        elif isinstance(self.bar, AmmoBar):
            self.image = textToImage(str(self.owner.ammo) + '/' + str(self.owner.maxAmmo), 'sprites/ui/small_font.png', 5, 7, 37)

        else:
            raise TypeError()

    def movement(self):
        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            self.renderImages()
        else:
            self.kill()


class HealthBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 0)

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            self.index = floor((16 * self.owner.hp) / self.owner.maxHp)
            self.renderImages()
        else:
            self.kill()


class DodgeBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 2)

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            if self.owner.hitTime < self.owner.hitTimeCharge:
                self.index = ceil((16 * self.owner.hitTime) / self.owner.hitTimeCharge)
                self.renderImages()
        else:
            self.kill()


class AmmoBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 1)

    def update(self):
        self.movement()

        if self.owner.hp > 0:
            self.index = floor((16 * self.owner.ammo) / self.owner.maxAmmo)
            self.renderImages()
        else:
            self.kill()


if __name__ == '__main__':
    os.system('python main.py')