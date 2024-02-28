"""
Module containing the ItemDrop class.
"""
import math
import random as rand
import time

import pygame
from pygame.math import Vector2 as vec

import text

import classbases as cb
import constants as cst
import calculations as calc
import groups
import spritesheet


class ItemDrop(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, item_name: str):
        """An item or material dropped by an enemy that can be collected.

        Args:
            item_name: The item to drop
        """
        print(f'I GOT {pos_x} AND {pos_y}')
        super().__init__(cst.LAYER['drops'])
        self.show(self.layer)
        self.mat = item_name

        self.start_time = time.time()

        self.accel_const = 0.8
        self.pos = vec((pos_x, pos_y))
        self.rand_accel = calc.get_rand_components(self.accel_const)
        
        self.spritesheet = spritesheet.Spritesheet("sprites/textures/item_drops.png", 8)
        self.index = 0

        if self.mat == cst.MAT[0]:
            self.orig_images = self.spritesheet.get_images(32, 32, 1, 0)
            self.images = self.spritesheet.get_images(32, 32, 1, 0)
        elif self.mat == cst.MAT[1]:
            self.orig_images = self.spritesheet.get_images(32, 32, 1, 1)
            self.images = self.spritesheet.get_images(32, 32, 1, 1)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        if self.can_update:
            if calc.get_time_diff(self.start_time) > 0.1:
                self.collide_check(groups.all_walls)

            exist_time = calc.get_time_diff(self.start_time)
            self.accel = self.get_accel()
            
            if exist_time <= 10:
                angle = math.sin(self.period_mult * math.pi * exist_time) * (1 / exist_time)
                self.rotate_image(int(math.degrees(angle)))
                self.rect = self.image.get_rect(center=self.rect.center)
            
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()

        exist_time = calc.get_time_diff(self.start_time)
        if exist_time <= 0.1:
            final_accel += self.rand_accel

        return final_accel

    def update(self):
        for a_player in groups.all_players:
            if self.hitbox.colliderect(a_player):
                groups.all_font_chars.add(
                    text.IndicatorText(a_player.pos.x, a_player.pos.y - a_player.rect.height // 2, self.mat, 1)
                )
                a_player.inventory[self.mat] += 1
                self.kill()

    def __repr__(self):
        return f'ItemDrop({self.pos})'
