import random as rand
import math
import time
import pygame

import constants as cst
import calculations as calc
import bullets
import groups
import classbases as cb
import statbars
import itemdrops

vec = pygame.math.Vector2
rad = math.radians


class EnemyBase(cb.ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It gives you better control over enemy objects."""
        super().__init__()
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.isShooting = False

        # -------------------- In-game Stats --------------------#
        self.maxHp = None
        self.hp = None
        self.maxAtk = None
        self.atk = None
        self.maxDef = None
        self.defense = None
        self.xpWorth = None

        self.healthBar = statbars.HealthBar(self)

    def _set_stats(self, hp: int, attack: int, defense: int, xp: int):
        self.maxHp = hp
        self.hp = hp
        self.maxAtk = attack
        self.atk = attack
        self.maxDef = defense
        self.defense = defense
        self.xpWorth = xp

    def _award_xp(self):
        for a_player in groups.all_players:
            a_player.xp += self.xpWorth
            a_player.update_level()
            a_player.update_max_stats()

    def _drop_items(self, table_index):
        drops = cst.LOOTDROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)
        
        for item in drops[row][column]:
            groups.all_drops.add(
                itemdrops.ItemDrop(self, item)
            )

    def _destroy_check(self, amplitude, duration, loot_table_index: int) -> None:
        """Checks if the enemy's health has been fully depleted and will explode.

        Args:
            amplitude: The amplitude of the explosion
            duration: The duration of the explosion
            loot_table_index: Which loot table to select drops from
        """
        if self.hp <= 0:
            calc.screen_shake_queue.add(amplitude, duration)
            self._drop_items(loot_table_index)
            self._award_xp()
            self.kill()


class StandardGrunt(EnemyBase):
    def __init__(self, pos_x: float, pos_y: float):
        """A simple enemy that moves to random locations and shoots at players.

        Args:
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
        """
        super().__init__()
        self.show(cst.LAYER['enemy'])
        groups.all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((pos_x, pos_y))
        self.randPos = vec(rand.randint(64, cst.WINWIDTH - 64), rand.randint(64, cst.WINHEIGHT - 64))

        self.set_room_pos()

        self.set_images('sprites/enemies/standard_grunt.png', 64, 64, 5, 5, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        # ---------------------- Game stats & UI ----------------------#
        self._set_stats(15, 10, 10, 40)

# --------------------------------- Movement --------------------------------- #
    def movement(self, can_shoot: bool = True):
        if self.canUpdate and self.hp > 0:
            self.__set_rand_pos()
            self.accel = self.get_accel()
            self.set_room_pos()
            
            if can_shoot:
                self.shoot(calc.get_closest_player(self), 6, rand.uniform(0.4, 0.9))

            self.accel_movement()

    def __set_rand_pos(self):
        """Assigns a random value within the proper range for the enemy to travel to.
        """
        if calc.get_time_diff(self.lastRelocate) > rand.uniform(2.5, 5.0):
            self.randPos.x = rand.randint(self.image.get_width(), cst.WINWIDTH - self.image.get_width())
            self.randPos.y = rand.randint(self.image.get_height(), cst.WINHEIGHT - self.image.get_height())

            pass_check = True
            # If the assigned random position is within a border or wall, it will run again and assign a new one.
            for border in groups.all_borders:
                if border.hitbox.collidepoint(self.randPos.x, self.randPos.y):
                    pass_check = False

            for wall in groups.all_walls:
                if wall.hitbox.collidepoint(self.randPos.x, self.randPos.y):
                    pass_check = False
            
            if pass_check:
                self.lastRelocate = time.time()

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)

        final_accel += room.get_accel()

        if self.pos.x != self.randPos.x or self.pos.y != self.randPos.y:
            # Moving to proper x-position
            if self.pos.x < self.randPos.x - self.hitbox.width // 2:
                final_accel.x += self.cAccel
            if self.pos.x > self.randPos.x + self.hitbox.width // 2:
                final_accel.x -= self.cAccel

            # Moving to proper y-position
            if self.pos.y < self.randPos.y - self.hitbox.height // 2:
                final_accel.y += self.cAccel
            if self.pos.y > self.randPos.y + self.hitbox.height // 2:
                final_accel.y -= self.cAccel

        return final_accel

# ---------------------------------- Actions --------------------------------- #
    def shoot(self, target, vel: float, shoot_time: float) -> None:
        """Shoots a bullet at a specific velocity at a specified interval.

        Args:
            target: The target the enemy is firing at
            vel: The velocity of the bullet
            shoot_time: How often the enemy should fire
        """
        if calc.get_time_diff(self.lastShot) > shoot_time:
            self.isShooting = True
            angle = calc.get_angle_to_sprite(self, target)

            cos_angle = math.cos(rad(angle))
            sin_angle = math.sin(rad(angle))

            vel_x = vel * -sin_angle
            vel_y = vel * -cos_angle
            offset = vec(21, 30)

            groups.all_projs.add(
                bullets.EnemyStdBullet(self,
                                       self.pos.x - (offset.x * cos_angle) - (offset.y * sin_angle),
                                       self.pos.y + (offset.x * sin_angle) - (offset.y * cos_angle),
                                       vel_x,
                                       vel_y)
                )
            self.lastShot = time.time()

# --------------------------------- Updating --------------------------------- #
    def update(self):
        if self.canUpdate and self.visible and self.hp > 0:
            self.collide_check(groups.all_players, groups.all_walls)

            # Animation
            self.__animate()
            self.rotate_image(calc.get_angle_to_sprite(self, calc.get_closest_player(self)))

        self._destroy_check(6, 75, 0)

    def __animate(self):
        if calc.get_time_diff(self.lastFrame) > cst.ANIMTIME:
            if self.isShooting:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.isShooting = False
            self.lastFrame = time.time()

    def __str__(self):
        return f'StandardGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xpWorth}'

    def __repr__(self):
        return f'StandardGrunt({self.pos}, {self.vel}, {self.accel}, {self.xpWorth})'


class Ambusher(EnemyBase):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.show(cst.LAYER['enemy'])
        groups.all_enemies.add(self)

        self.pos = vec((pos_x, pos_y))
        self.set_room_pos()

        self.movement_timer = time.time()
        self.movement_angle = calc.get_angle_to_sprite(self, calc.get_closest_player(self))

        self.set_images('sprites/enemies/ambusher.png', 64, 64, 1, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self._set_stats(40, 10, 20, 150)

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)

        self.movement_angle = calc.get_angle_to_sprite(self, calc.get_closest_player(self))
        dash_timer = calc.eerp(0.5, 0.8, self.hp / self.maxHp)  # Moves for longer as health gets lower

        # Rush towards the nearest player
        if calc.get_time_diff(self.movement_timer) >= dash_timer:
            intensity = 2
            final_accel.x += intensity * -math.sin(math.radians(self.movement_angle))
            final_accel.y += intensity * -math.cos(math.radians(self.movement_angle))

            # Stop movement and change direction
            if calc.get_time_diff(self.movement_timer) >= 1:
                self.movement_timer = time.time()

        final_accel += room.get_accel()
        return final_accel

    def movement(self):
        self.accel = self.get_accel()
        self.set_room_pos()

        self.accel_movement()

    def update(self):
        self.rotate_image(calc.get_angle_to_sprite(self, calc.get_closest_player(self)))
        self._destroy_check(6, 75, 2)
