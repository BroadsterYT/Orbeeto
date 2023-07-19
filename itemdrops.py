import pygame
from math import degrees, pi

from calculations import *
from class_bases import *
from constants import *


class DropBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.ACCELC = 0.8


class ItemDrop(DropBase):
    def __init__(self, dropped_from, item_name):
        """An item or material dropped by an enemey that is able to be collected
        
        ### Arguments
            - dropped_from (``pygame.sprite.Sprite``): The enemy that the item was dropped from
            - item_name (``str``): The item to drop
            - item_frame_start (``int``): The index of the first frame to display from the item drop spritesheet (0 = the first image).
            - image_count (``int``): The number of frames to use
        """        
        super().__init__()
        self.show(LAYER['drops_layer'])
        all_drops.add(self)
        self.droppedFrom = dropped_from
        self.mat = item_name

        self.start_time = time.time()
        self.pos = vec(self.droppedFrom.pos.x, self.droppedFrom.pos.y)
        self.randAccel = getRandComponents(self.ACCELC)
        
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
        if self.visible:
            time_since_start = getTimeDiff(self.start_time)
            if time_since_start <= 0.1:
                self.accel.x = self.randAccel.x
                self.accel.y = self.randAccel.y
            
            if time_since_start <= 10:
                self.original_image = self.original_images[self.index]
                self.image = pygame.transform.rotate(self.original_image, int(degrees(sin(self.period_mult * pi * time_since_start) * (1 / time_since_start))))
                self.rect = self.image.get_rect(center = self.rect.center)
            
            self.accelMovement()

    def update(self):
        self.collideCheck(all_walls)
        self.movement()

        for a_player in all_players:
            if self.hitbox.colliderect(a_player):
                a_player.inventory[self.mat] += 1
                a_player.menu.updateMenuSlots()
                self.kill()
