import os

from pygame.math import Vector2 as vec

import projectiles as proj

import calc
import groups
import timer


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
        super().__init__(7)
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)
        self.ric_count = bounce_count

        self.dmg_mod = dmg_mod

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_players, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_game_tdiff(self.start_time) <= 5:
                self.accel = self.get_accel()
                self.accel_movement()
            else:
                self.kill()

    def update(self):
        super().update()

    def __repr__(self):
        return f'EnemyStdBullet({self.pos}, {self.vel}, {self.ric_count})'


class AmbusherDasher(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, launch_angle: float, dmg_mod: int = 1):
        """The projectile launched by Ambushers when they dash.

        :param pos_x: The x-axis position to spawn
        :param pos_y: The y-axis position to spawn
        :param launch_angle: The angle, with respect to the Ambusher, to launch (in degrees)
        :param dmg_mod: The factor to multiply the projectile's damage by
        """
        super().__init__()
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.launch_vel = vec(7, 0)
        self.vel = self.launch_vel.rotate(launch_angle)
        self.vel_const = self.launch_vel.rotate(launch_angle)
        self.seek_time = timer.g_timer.time

        self.dmg_mod = dmg_mod

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 32, 32)
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_players, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            # TODO: Update movement logic to use accel_movement
            if calc.get_game_tdiff(self.start_time) <= 10:
                # self.vel = self.get_vel()
                # self.vel_movement(False)
                pass
            else:
                self.kill()

    # def get_vel(self) -> vec:
    #     room = cb.get_room()
    #
    #     # Homing capability
    #     if 0.2 < calc.get_game_tdiff(self.seek_time) <= 0.75:
    #         angle = 270 - calc.get_angle(self.pos, room.player1.pos)
    #         self.vel_const = self.launch_vel.rotate(calc.eerp(1, angle, self.seek_time))
    #
    #     final_vel = self.vel_const + room.vel.copy()
    #     return final_vel * screen.dt * cst.M_FPS

    def update(self):
        super().update()
