"""
Module containing the ItemDrop class.
"""
import math
import os
import random as rand

import pygame
from pygame.math import Vector2 as vec

import items
import text

import classbases as cb
import constants as cst
import calc
import groups
import spritesheet
import time

import timer


class ItemDrop(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, item_name: str):
        """An item or material dropped by an enemy that can be collected

        :param pos_x: The x-axis position to spawn the item
        :param pos_y: The y-axis position to spawn the item
        :param item_name: The name of the item to drop. Should be chosen from 'items.MATERIALS'.
        """
        super().__init__(cst.LAYER['drops'])
        groups.all_drops.add(self)
        self.add_to_gamestate()
        self.mat = item_name

        self.start_time = timer.g_timer.time

        self.accel_const = 0.58
        self.pos = vec((pos_x, pos_y))
        self.rand_accel = calc.get_rand_components(self.accel_const)
        
        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/textures/item_drops.png'), 3)
        self.index = 0

        if self.mat == items.MATERIALS[0]:
            self.orig_images = self.spritesheet.get_images(32, 32, 3, 0)
            self.images = self.spritesheet.get_images(32, 32, 3, 0)
        elif self.mat == items.MATERIALS[1]:
            self.orig_images = self.spritesheet.get_images(32, 32, 1, 3)
            self.images = self.spritesheet.get_images(32, 32, 1, 3)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        if self.can_update:
            if calc.get_time_diff(self.start_time) > 0.5:
                self.collide_check(groups.all_walls)

            self.rect = self.image.get_rect(center=self.rect.center)

            self.accel = self.get_accel()
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
        self._animate()
        for a_player in groups.all_players:
            if self.hitbox.colliderect(a_player.hitbox):
                groups.all_font_chars.add(
                    text.IndicatorText(a_player.pos.x, a_player.pos.y - a_player.rect.height // 2, self.mat, 1)
                )
                a_player.my_materials[self.mat] += 1
                self.kill()

    def _animate(self):
        if self.mat == items.MATERIALS[0] and calc.get_time_diff(self.last_frame) > 0.1:
            self.image = self.images[self.index]
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.last_frame = time.time()

        if self.mat == items.MATERIALS[1] and calc.get_time_diff(self.last_frame) > 0.1:
            self.image = self.images[self.index]

        exist_time = calc.get_game_tdiff(self.start_time)
        if exist_time <= 10:
            angle = math.sin(self.period_mult * math.pi * exist_time) * (1 / exist_time)
            self.rotate_image(math.degrees(angle))

    def __repr__(self):
        return f'ItemDrop({self.pos})'
