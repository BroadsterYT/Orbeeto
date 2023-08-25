import pygame
from math import degrees, pi

from class_bases import *


class DropBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.cAccel = 0.8


class ItemDrop(DropBase):
    def __init__(self, droppedFrom, itemName):
        """An item or material dropped by an enemey that is able to be collected
        
        ### Arguments
            - droppedFrom (``pygame.sprite.Sprite``): The enemy that the item was dropped from
            - itemName (``str``): The item to drop
        """        
        super().__init__()
        self.show(LAYER['drops'])
        all_drops.add(self)
        self.droppedFrom = droppedFrom
        self.mat = itemName

        self.startTime = time.time()
        self.pos = vec(self.droppedFrom.pos.x, self.droppedFrom.pos.y)
        self.randAccel = getRandComponents(self.cAccel)
        
        self.spritesheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.index = 0

        if self.mat == MAT[0]:
            self.original_images = self.spritesheet.get_images(32, 32, 1, 0)
            self.images = self.spritesheet.get_images(32, 32, 1, 0)
        elif self.mat == MAT[1]:
            self.original_images = self.spritesheet.get_images(32, 32, 1, 1)
            self.images = self.spritesheet.get_images(32, 32, 1, 1)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        self.accel = vec(0, 0)
        if self.canUpdate and self.visible:
            existTime = getTimeDiff(self.startTime)
            self.accel = self.getAccel()
            
            if existTime <= 10:
                self.original_image = self.original_images[self.index]
                self.image = pygame.transform.rotate(self.original_image, int(degrees(sin(self.period_mult * pi * existTime) * (1 / existTime))))
                self.rect = self.image.get_rect(center = self.rect.center)
            
            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        room = self.getRoom()
        finalAccel = vec(0, 0)

        finalAccel += room.getAccel()

        existTime = getTimeDiff(self.startTime)
        if existTime <= 0.1:
            finalAccel += self.randAccel

        return finalAccel

    def update(self):
        self.collideCheck(all_walls)
        self.movement()

        for a_player in all_players:
            if self.hitbox.colliderect(a_player):
                a_player.inventory[self.mat] += 1
                a_player.menu.updateMenuSlots()
                self.kill()
