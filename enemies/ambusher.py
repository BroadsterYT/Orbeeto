import math
import time

import pygame
from pygame.math import Vector2 as vec

from enemies import enemybase

import classbases as cb
import calculations as calc
import groups


class Ambusher(enemybase.EnemyBase):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.show(self.layer)
        groups.all_enemies.add(self)

        self.pos = vec((pos_x, pos_y))
        self.set_room_pos()

        self.movement_timer = time.time()
        self.movement_angle = calc.get_angle(self, calc.get_closest_player(self))

        self.set_images('../sprites/enemies/ambusher.png', 64, 64, 1, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self._set_stats(40, 15, 150)

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)

        self.movement_angle = calc.get_angle(self, calc.get_closest_player(self))
        dash_timer = calc.eerp(0.5, 0.8, self.hp / self._max_hp)  # Moves for longer as health gets lower

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
        if self.can_update and self.hp > 0:
            self.accel = self.get_accel()
            self.set_room_pos()

            self.accel_movement()

    def update(self):
        self.rotate_image(calc.get_angle(self, calc.get_closest_player(self)))
        self._destroy_check(6, 75, 2)
