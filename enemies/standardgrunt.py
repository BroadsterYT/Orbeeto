import time
import math
import random as rand

import pygame
from pygame.math import Vector2 as vec

from enemies import enemybase

import bullets
import calculations as calc
import classbases as cb
import constants as cst
import groups


class StandardGrunt(enemybase.EnemyBase):
    def __init__(self, pos_x: float, pos_y: float):
        """A simple enemy that moves to random locations and shoots at players.

        Args:
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
        """
        super().__init__()
        self.show(self.layer)
        groups.all_enemies.add(self)

        self.last_relocate = time.time()
        self.last_shot = time.time()

        self.pos = vec((pos_x, pos_y))
        self.rand_pos = vec(rand.randint(64, cst.WINWIDTH - 64), rand.randint(64, cst.WINHEIGHT - 64))

        self.set_room_pos()

        self.set_images('sprites/enemies/standard_grunt.png', 64, 64, 5, 5, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        # ---------------------- Game stats & UI ----------------------#
        self._set_stats(15, 5, 40)

# --------------------------------- Movement --------------------------------- #
    def movement(self, can_shoot: bool = True):
        if self.can_update and self.hp > 0:
            self.__set_rand_pos()
            self.accel = self.get_accel()
            self.set_room_pos()

            if can_shoot:
                self.shoot(calc.get_closest_player(self), 6, rand.uniform(0.4, 0.9))

            self.accel_movement()

    def __set_rand_pos(self):
        """Assigns a random value within the proper range for the enemy to travel to.
        """
        if calc.get_time_diff(self.last_relocate) > rand.uniform(2.5, 5.0):
            self.rand_pos.x = rand.randint(self.image.get_width(), cst.WINWIDTH - self.image.get_width())
            self.rand_pos.y = rand.randint(self.image.get_height(), cst.WINHEIGHT - self.image.get_height())

            pass_check = True
            # If the assigned random position is within a border or wall, it will run again and assign a new one.
            for border in groups.all_borders:
                if border.hitbox.collidepoint(self.rand_pos.x, self.rand_pos.y):
                    pass_check = False

            for wall in groups.all_walls:
                if wall.hitbox.collidepoint(self.rand_pos.x, self.rand_pos.y):
                    pass_check = False

            if pass_check:
                self.lastRelocate = time.time()

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)

        final_accel += room.get_accel()

        if self.pos.x != self.rand_pos.x or self.pos.y != self.rand_pos.y:
            # Moving to proper x-position
            if self.pos.x < self.rand_pos.x - self.hitbox.width // 2:
                final_accel.x += self.accel_const
            if self.pos.x > self.rand_pos.x + self.hitbox.width // 2:
                final_accel.x -= self.accel_const

            # Moving to proper y-position
            if self.pos.y < self.rand_pos.y - self.hitbox.height // 2:
                final_accel.y += self.accel_const
            if self.pos.y > self.rand_pos.y + self.hitbox.height // 2:
                final_accel.y -= self.accel_const

        return final_accel

# ---------------------------------- Actions --------------------------------- #
    def shoot(self, target, vel: float, shoot_time: float) -> None:
        """Shoots a bullet at a specific velocity at a specified interval.

        Args:
            target: The target the enemy is firing at
            vel: The velocity of the bullet
            shoot_time: How often the enemy should fire
        """
        if calc.get_time_diff(self.last_shot) > shoot_time:
            self.is_shooting = True
            angle = calc.get_angle(self, target)

            cos_angle = math.cos(math.radians(angle))
            sin_angle = math.sin(math.radians(angle))

            vel_x = vel * -sin_angle
            vel_y = vel * -cos_angle
            offset = vec(21, 30)

            groups.all_projs.add(
                bullets.EnemyStdBullet(self.pos.x - (offset.x * cos_angle) - (offset.y * sin_angle),
                                       self.pos.y + (offset.x * sin_angle) - (offset.y * cos_angle),
                                       vel_x, vel_y)
            )
            self.last_shot = time.time()

# --------------------------------- Updating --------------------------------- #
    def update(self):
        if self.visible and self.hp > 0:
            self.collide_check(groups.all_players, groups.all_walls)

            # Animation
            self.__animate()
            self.rotate_image(calc.get_angle(self, calc.get_closest_player(self)))

        self._destroy_check(6, 75, 0)

    def __animate(self):
        if calc.get_time_diff(self.last_frame) > 0.1:  # TODO: Use SPF to standardize animations
            if self.is_shooting:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.isShooting = False
            self.lastFrame = time.time()

    def __str__(self):
        return f'StandardGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xp}'

    def __repr__(self):
        return f'StandardGrunt({self.pos}, {self.vel}, {self.accel}, {self.xp})'
