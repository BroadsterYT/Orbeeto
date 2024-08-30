import os
import random as rand
import time

import pygame
from pygame.math import Vector2 as vec

import calc
import classbases as cb
import constants as cst


class StdBulletExplode(cb.ActorBase):
    def __init__(self, owner, pos_x: float, pos_y: float):
        """An explosion that is displayed on-screen when a projectile hits something.

        :param owner: The entity to render an explosion for
        :param pos_x: The x-position to spawn the explosion at
        :param pos_y: The y-position to spawn the explosion at
        """
        super().__init__(cst.LAYER['explosion'])
        self.add_to_gamestate()
        self.owner = owner

        self.pos = vec((pos_x, pos_y))
        self.pos_offset = vec(self.pos.x - self.owner.hit.pos.x, self.pos.y - self.owner.hit.pos.y)
        self.set_images(os.path.join(os.getcwd(), 'sprites/textures/explosions.png'), 32, 32, 8, 4, 0, 1)
        self.set_rects(self.pos.x, self.pos.y, 32, 32, 32, 32)

        self.render_images()
        self.rand_rotation = rand.randint(1, 360)

    def movement(self):
        self.center_rects()
        self.pos = self.owner.hit.hitbox.center + self.pos_offset

    def update(self):
        self.movement()
        self._animate()
        self.center_rects()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) >= cst.SPF:
            if self.index > 3:
                self.kill()
            else:
                self.render_images()
                self.index += 1
            self.last_frame = time.time()
        self.image = pygame.transform.rotate(self.orig_image, self.rand_rotation)

    def __repr__(self):
        return f'StdBulletExplode({self.owner}, {self.pos})'
