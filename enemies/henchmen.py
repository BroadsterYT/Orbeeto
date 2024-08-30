import math
import os
import random as rand
import time

import pygame
from pygame.math import Vector2 as vec

from enemies import enemybase
import projectiles as proj
import screen

import calc
import classbases as cb
import constants as cst
import groups
import timer


class StandardGrunt(enemybase.EnemyBase):
    def __init__(self, pos_x: float, pos_y: float):
        """A simple enemy that moves to random locations and shoots at players.

        :param pos_x: The x-position to spawn at
        :param pos_y: The y-position to spawn at
        """
        super().__init__()
        self.add_to_gamestate()
        groups.all_enemies.add(self)

        self.last_relocate = time.time()
        self.last_shot = time.time()

        self.pos = vec((pos_x, pos_y))
        self.rand_pos = vec(rand.randint(64, cst.WINWIDTH - 64), rand.randint(64, cst.WINHEIGHT - 64))

        self.set_room_pos()

        self.set_images(os.path.join(os.getcwd(), 'sprites/enemies/standard_grunt.png'), 64, 64, 5, 5, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        # ---------------------- Game stats & UI ----------------------#
        self._set_stats(15, 5, 40)

    # --------------------------------- Movement --------------------------------- #
    def movement(self, can_shoot: bool = True):
        if self.hp > 0:
            self._set_rand_pos()
            self.accel = self.get_accel()
            self.set_room_pos()

            if can_shoot:
                self.shoot(calc.get_closest_player(), 6, rand.uniform(0.4, 0.9))

            self.accel_movement()

    def _set_rand_pos(self):
        """Assigns a random value within the proper range for the enemy to travel to.
        """
        if calc.get_time_diff(self.last_relocate) > rand.uniform(2.5, 5):
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
                self.last_relocate = time.time()

    def get_accel(self) -> pygame.math.Vector2:
        final_accel = vec(0, 0)

        room = cb.get_room()
        final_accel += room.get_accel()

        adjust_loc_x = self.rand_pos.x + room.pos.x
        adjust_loc_y = self.rand_pos.y + room.pos.y

        if self.pos.x < adjust_loc_x - self.hitbox.width // 2:
            final_accel.x += self.accel_const
        if self.pos.x > adjust_loc_x + self.hitbox.width // 2:
            final_accel.x -= self.accel_const

        if self.pos.y < adjust_loc_y - self.hitbox.height // 2:
            final_accel.y += self.accel_const
        if self.pos.y > adjust_loc_y + self.hitbox.height // 2:
            final_accel.y -= self.accel_const

        return final_accel

    # ---------------------------------- Actions --------------------------------- #
    def shoot(self, target, vel: float, shoot_time: float) -> None:
        """Shoots a bullet at a specific velocity at a specified interval.

        :param target: The target the enemy is firing at
        :param vel: The velocity of the bullet
        :param shoot_time: How often the enemy should fire
        :return: None
        """
        if calc.get_time_diff(self.last_shot) > shoot_time:
            self.is_shooting = True
            angle = calc.get_angle(self.pos, target.pos)

            cos_angle = math.cos(math.radians(angle))
            sin_angle = math.sin(math.radians(angle))

            vel_x = vel * -sin_angle
            vel_y = vel * -cos_angle
            offset = vec(21, 30)

            groups.all_projs.add(
                proj.EnemyStdBullet(self.pos.x - (offset.x * cos_angle) - (offset.y * sin_angle),
                                    self.pos.y + (offset.x * sin_angle) - (offset.y * cos_angle),
                                    vel_x, vel_y)
            )
            self.last_shot = time.time()

    # --------------------------------- Updating --------------------------------- #
    def update(self):
        if self.hp > 0:
            self.collide_check(groups.all_players, groups.all_walls)

            self._animate()
            self.rotate_image(calc.get_angle(self.pos, calc.get_closest_player().pos))

        self._destroy_check(6, 75, 0)

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 0.1:
            if self.is_shooting:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.is_shooting = False
            self.last_frame = time.time()

    def __str__(self):
        return f'StandardGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xp}'

    def __repr__(self):
        return f'StandardGrunt({self.pos}, {self.rand_pos}, {self.vel}, {self.accel}, {self.xp})'


class Turret(enemybase.EnemyBase):
    def __init__(self, pos_x: float, pos_y: float):
        """An enemy that stays in place and shoots volleys of bullets.

        :param pos_x: The x-position to spawn at
        :param pos_y: The y-position to spawn at
        """
        super().__init__()
        self.add_to_gamestate()
        groups.all_sentries.add(self)

        self.bullet_vel = vec(0, 6)
        self.bullet_angle = math.degrees(1) * screen.dt * cst.FPS
        self.last_shot = time.time()

        self.pos = vec((pos_x, pos_y))
        self.set_room_pos()

        self.set_images(os.path.join(os.getcwd(), 'sprites/enemies/standard_grunt.png'), 64, 64, 5, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self._set_stats(10, 10, 68)

    def movement(self, can_shoot: bool = True):
        if can_shoot:
            self.shoot(0.2)

        self.accel = self.get_accel()
        self.accel_movement()
        self.set_room_pos()

    def shoot(self, shoot_time: float) -> None:
        """Shoots a volley of bullets.

        :param shoot_time: How often the volleys should be fired
        :return: None
        """
        if calc.get_time_diff(self.last_shot) > shoot_time:
            self.bullet_angle = math.degrees(1) * screen.dt * cst.M_FPS
            self.is_shooting = True

            vel_rot1 = self.bullet_vel.rotate(90)

            groups.all_projs.add(
                proj.EnemyStdBullet(self.pos.x + 6, self.pos.y, self.bullet_vel.x, self.bullet_vel.y),
                proj.EnemyStdBullet(self.pos.x + 6, self.pos.y, -self.bullet_vel.x, -self.bullet_vel.y),
                proj.EnemyStdBullet(self.pos.x + 6, self.pos.y, vel_rot1.x, vel_rot1.y),
                proj.EnemyStdBullet(self.pos.x + 6, self.pos.y, -vel_rot1.x, -vel_rot1.y),
            )
            self.bullet_vel = self.bullet_vel.rotate(self.bullet_angle)
            self.last_shot = time.time()

    def update(self):
        if self.hp > 0:
            self._animate()
        self._destroy_check(15, 80, 2)

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > cst.SPF:
            if self.is_shooting:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.is_shooting = False
            self.last_frame = time.time()

    def __str__(self):
        return f'Turret at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xp}'

    def __repr__(self):
        return f'Turret({self.pos}, {self.vel}, {self.accel}, {self.xp})'


class Ambusher(enemybase.EnemyBase):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.add_to_gamestate()
        groups.all_enemies.add(self)

        self.pos = vec((pos_x, pos_y))
        self.set_room_pos()
        self.last_shot = timer.g_timer.time

        self.movement_timer = time.time()
        self.movement_angle = calc.get_angle(self.pos, calc.get_closest_player().pos)

        self.set_images('sprites/enemies/ambusher.png', 64, 64, 1, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self._set_stats(40, 15, 150)

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)

        self.movement_angle = calc.get_angle(self.pos, calc.get_closest_player().pos)
        dash_timer = calc.eerp(0.6, 0.8, self.hp / self.max_hp)  # Moves for longer as health gets lower

        # Rush towards the nearest player
        if calc.get_time_diff(self.movement_timer) >= dash_timer:
            intensity = 2
            final_accel.x += intensity * -math.sin(math.radians(self.movement_angle))
            final_accel.y += intensity * -math.cos(math.radians(self.movement_angle))

            # Stop movement and change direction
            if calc.get_time_diff(self.movement_timer) >= 1:
                groups.all_projs.add(
                    proj.AmbusherDasher(self.pos.x, self.pos.y, 90),
                    proj.AmbusherDasher(self.pos.x, self.pos.y, 270),
                )
                self.movement_timer = time.time()

        final_accel += room.get_accel()
        return final_accel

    def movement(self):
        if self.hp > 0:
            self.collide_check(groups.all_walls)
            self.accel = self.get_accel()
            self.set_room_pos()
            self.accel_movement()

    def update(self):
        self.rotate_image(calc.get_angle(self.pos, calc.get_closest_player().pos))
        self._destroy_check(6, 75, 2)
