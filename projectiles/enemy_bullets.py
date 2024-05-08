import os

from pygame.math import Vector2 as vec

import projectiles as proj

import calc
import constants as cst
import groups


class EnemyStdBullet(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, dmg_mod: int = 1, bounce_count: int = 1):
        """A projectile fired by an enemy that moves at a constant velocity

        :param pos_x: The x-position where the bullet should be spawned
        :param pos_y: The y-position where the bullet should be spawned
        :param vel_x: The x-axis component of the bullet's velocity
        :param vel_y: The y-axis component of the bullet's velocity
        :param dmg_mod: Multiplier for the bullet's damage
        :param bounce_count: The amount of times the bullet should bounce/ricochet
        """
        super().__init__(cst.PROJ_DAMAGE[cst.PROJ_STD])
        self.show()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = self.vel
        self.ric_count = bounce_count

        self.dmg_mod = dmg_mod

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.can_update:
            self.proj_collide(groups.all_players, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_time_diff(self.start_time) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(False)
            else:
                self.kill()

    def update(self):
        super().update()

    def __repr__(self):
        return f'EnemyStdBullet({self.pos}, {self.vel}, {self.ric_count})'
