import itertools
import math
import os
import time

import pygame
from pygame.math import Vector2 as vec

import projectiles as proj

import classbases as cb
import calc
import constants as cst
import groups

import portals
import screen
import timer
import visual_elems


class PlayerStdBullet(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        """A projectile fired by a player that moves at a constant velocity.

        :param pos_x: The x-position where the bullet should be spawned
        :param pos_y: The y-position where the bullet should be spawned
        :param vel_x: The x-axis component of the bullet's velocity
        :param vel_y: The y-axis component of the bullet's velocity
        :param bounce_count: The number of times the bullet should bounce. Defaults to 1 (no bounce).
        """
        super().__init__(7)
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)
        self.ric_count = bounce_count

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_sentries, True)
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
        return f'PlayerStdBullet({self.pos}, {self.vel})'


class PlayerLaserBullet(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        super().__init__(11)
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)
        self.ric_count = bounce_count

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1, 2)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 10, 10)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_sentries, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_game_tdiff(self.start_time) <= 5:
                self.accel = self.get_accel()
                self.accel_movement()
            else:
                self.kill()

    def update(self):
        super().update()


class PlayerChakram(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float):
        """A projectile fired by a player that moves at a constant velocity.

        :param pos_x: The x-position where the bullet should be spawned
        :param pos_y: The y-position where the bullet should be spawned
        :param vel_x: The x-axis component of the bullet's velocity
        :param vel_y: The y-axis component of the bullet's velocity
        """
        super().__init__(14)
        self.add_to_gamestate()
        self.start_time = timer.g_timer.time

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y).rotate(-30)
        self.vel_const = vec(vel_x, vel_y).rotate(-30)
        self.ric_count = 1

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1, 3)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.image_angle = 0
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def get_accel(self) -> vec:
        room = cb.get_room()
        final_accel = vec(self.vel_const.x / 15, self.vel_const.y / 15)
        final_accel += room.get_accel()
        return final_accel

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_sentries, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_game_tdiff(self.start_time) <= 5:
                self.accel = self.get_accel()
                self.accel_movement()
                self.vel_const = self.vel_const.rotate(self.get_arc_angle())
            else:
                self.kill()
            pygame.draw.rect(screen.buffer_screen, (255, 0, 0), self.hitbox)

    def get_arc_angle(self) -> float:
        t = calc.get_game_tdiff(self.start_time)
        return math.sin(t) * 3

    def update(self):
        super().update()
        self.rotate_image(self.image_angle)
        self.image_angle += 10

    def __repr__(self):
        return f'PlayerStdBullet({self.pos}, {self.vel})'


class PlayerHomingBullet(proj.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        """A projectile fired by a player that homes in on enemies

        :param pos_x: The x-position where the bullet should be spawned
        :param pos_y: The y-position where the bullet should be spawned
        :param vel_x: The x-axis component of the bullet's velocity
        :param vel_y: The y-axis component of the bullet's velocity
        :param bounce_count: The number of times the bullet should bounce. Defaults to 1 (no bounce).
        """
        super().__init__(7)
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)
        self.launch_vel = vec(vel_x, vel_y)
        self.ric_count = bounce_count

        self.last_homing_time = timer.g_timer.time
        self.seek_time = timer.g_timer.time

        self.dist_dict = {}
        for sprite in [s for s in itertools.chain(groups.all_enemies, groups.all_sentries)
                       if s.in_gamestate]:
            self.dist_dict.update({sprite: calc.get_dist(self.pos, sprite.pos)})
        self.last_homing_time = timer.g_timer.time

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def get_accel(self) -> vec:
        room = cb.get_room()
        final_accel = vec(self.vel_const.x / 15, self.vel_const.y / 15)

        # Getting distances away from every enemy
        if calc.get_game_tdiff(self.last_homing_time) >= 0.3:
            self.dist_dict = {}
            for sprite in [s for s in itertools.chain(groups.all_enemies, groups.all_sentries)
                           if s.in_gamestate]:
                self.dist_dict.update({sprite: calc.get_dist(self.pos, sprite.pos)})
            self.last_homing_time = timer.g_timer.time

        # Homing onto the closest target
        # TODO: MAKE THIS SHIT WORK!
        try:
            closest_target = min(self.dist_dict, key=self.dist_dict.get)
            if self.pos.x < closest_target.pos.x:
                final_accel.x += 0.5
            elif self.pos.x >= closest_target.pos.x:
                final_accel.x -= 0.5

            if self.pos.y < closest_target.pos.y:
                final_accel.y += 0.5
            elif self.pos.y >= closest_target.pos.y:
                final_accel.y -= 0.5
        except ValueError:
            pass

        final_accel += room.get_accel()
        return final_accel

    @staticmethod
    def get_angle_weight(angle) -> float:
        return -5 * math.sin(math.pi * angle / 360)

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_sentries, True)
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
        return f'PlayerStdBullet({self.pos}, {self.vel})'


# ------------------------------ Utility Bullets ----------------------------- #
class PortalBullet(proj.BulletBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        super().__init__()
        self.add_to_gamestate()

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)

        self.hitbox_adjust = vec(0, 0)

        self.set_images(os.path.join(os.getcwd(), 'sprites/bullets/bullets.png'), 32, 32, 8, 5, 8)
        self.set_rects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def proj_collide(self, sprite_group, can_hurt: bool):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.in_gamestate:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, collidingSprite)
                self.land(collidingSprite)

            elif not can_hurt:
                # If the projectile hits a portal
                if sprite_group == groups.all_portals:
                    if len(groups.all_portals) == 2:
                        for portal in groups.all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)

                elif sprite_group == groups.all_walls:
                    self.land(collidingSprite)
                    self._spawn_portal(collidingSprite)
                
                else:
                    self.land(collidingSprite)

    def _spawn_portal(self, surface) -> None:
        """Spawns a portal on the surface that the portal bullet hit.

        :param surface: The surface the portal bullet landed on.
        :return: None
        """
        side = calc.triangle_collide(self, surface)
        if side == cst.SOUTH:
            groups.all_portals.add(portals.Portal(self, self.pos.x, surface.pos.y + surface.hitbox.height // 2, side))
            portals.portal_count_check()
        if side == cst.NORTH:
            groups.all_portals.add(portals.Portal(self, self.pos.x, surface.pos.y - surface.hitbox.height // 2, side))
            portals.portal_count_check()
        if side == cst.EAST:
            groups.all_portals.add(portals.Portal(self, surface.pos.x + surface.hitbox.width // 2, self.pos.y, side))
            portals.portal_count_check()
        if side == cst.WEST:
            groups.all_portals.add(portals.Portal(self, surface.pos.x - surface.hitbox.width // 2, self.pos.y, side))
            portals.portal_count_check()

    def movement(self):
        if self.in_gamestate:
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portal_blockers, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_game_tdiff(self.start_time) <= 5:
                self.accel = self.get_accel()
                self.accel_movement()
            else:
                self.kill()

    def update(self):
        if calc.get_time_diff(self.last_frame) > 0.1:
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.last_frame = time.time()

        rotate_angle = int(calc.get_vec_angle(self.vel_const.x, self.vel_const.y))
        self.rotate_image(rotate_angle)
        super().update()

    def __repr__(self):
        return f'PortalBullet({self.pos}, {self.vel}, {self.ric_count})'


class GrappleBullet(proj.BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float):
        super().__init__()
        self.layer = cst.LAYER['grapple']
        self.add_to_gamestate()
        self.damage = 0
        
        self.shot_from = shot_from

        self.is_hooked = False
        self.grappled_to = None
        self.pos_offset = vec(0, 0)

        self.returning = False

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = vec(vel_x, vel_y)
        self.accel = vec(0, 0)
        self.accel_const = 1.5

        self.chain = visual_elems.Beam(self, self.shot_from)
        self.portal_list = []
        self.portal_check = True

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 2, 16)
        self.set_rects(0, 0, 32, 32, 16, 16)
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def land(self, grappled_to):
        if not self.returning:  # Hook won't scoop thing up on the way back to the player
            self.is_hooked = True
            self.grappled_to = grappled_to
            self.grappled_to.grappled_by = self
            if self.grappled_to is not None:
                self.grappled_to.is_grappled = True
                self.pos_offset = vec(self.pos.x - self.grappled_to.pos.x, self.pos.y - self.grappled_to.pos.y)

    def shatter(self):
        """Completely destroys the grappling hook.
        """
        self.returning = False
        self.shot_from.grapple = None
        if self.grappled_to is not None:
            self.grappled_to.is_grappled = False

        self.portal_list = []
        self.portal_check = True

        self.chain.kill()
        self.kill()

    def proj_collide(self, sprite_group, can_hurt):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue

            if not collidingSprite.in_gamestate:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, collidingSprite)
                self.land(collidingSprite)

            elif not can_hurt:
                if sprite_group == groups.all_portals:
                    if len(groups.all_portals) == 2:
                        for portal in groups.all_portals:
                            if self.hitbox.colliderect(portal.hitbox) and self.portal_check:
                                self.portal_list.append(portal)
                                self.portal_list.append(calc.get_other_portal(portal))
                                self.portal_check = False
                                self.teleport(portal)
                                self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))
                        return

                else:
                    self.land(collidingSprite)

    def send_back(self):
        if self.grappled_to not in groups.all_walls:
            # Hook returns to portal it entered
            if len(self.portal_list) > 1:
                angle = calc.get_angle(self.pos, self.portal_list[1].pos)
                room = cb.get_room()
                room_accel = room.get_accel()
                self.accel.x = self.accel_const * -math.sin(math.radians(angle)) + room_accel.x
                self.accel.y = self.accel_const * -math.cos(math.radians(angle)) + room_accel.y

                if self.hitbox.colliderect(self.portal_list[1]):
                    print('send to other')
                    self.pos = self.portal_list[0].pos
                    self.portal_list = []

            # Hook returns to player
            else:
                angle = calc.get_angle(self.pos, self.shot_from.pos)
                room = cb.get_room()
                room_accel = room.get_accel()
                self.accel.x = self.accel_const * -math.sin(math.radians(angle)) + room_accel.x
                self.accel.y = self.accel_const * -math.cos(math.radians(angle)) + room_accel.y

                # Hook disappears once it returns
                if self.hitbox.colliderect(self.shot_from.hitbox):
                    self.shatter()

            self.accel_movement()

            # Hook follows whatever it has grabbed
            if self.grappled_to is not None and self.grappled_to not in groups.all_portals:
                if self.grappled_to not in groups.all_walls:
                    self.grappled_to.pos = self.pos

        # Player should accelerate to the hook
        else:
            self.pos = self.grappled_to.pos + self.pos_offset
            if self.hitbox.colliderect(self.shot_from.hitbox):
                self.shatter()

    def movement(self):
        if not self.returning:
            if not self.is_hooked:
                self.accel = self.get_accel()
                self.accel_movement()

            elif self.is_hooked:
                if self.grappled_to is not None and self.grappled_to not in groups.all_walls:
                    self.pos.x = self.grappled_to.pos.x
                    self.pos.y = self.grappled_to.pos.y

                elif self.grappled_to is not None and self.grappled_to in groups.all_walls:
                    self.pos = self.grappled_to.pos + self.pos_offset
                
                else:
                    self.pos = self.pos
        
        elif self.returning:
            self.send_back()

        self.center_rects()

    def bind_proj(self):
        if self.in_gamestate:
            if not self.is_hooked:
                self.proj_collide(groups.all_enemies, True)
                self.proj_collide(groups.all_movable, False)
                self.proj_collide(groups.all_portals, False)
                self.proj_collide(groups.all_walls, False)
                self.proj_collide(groups.all_drops, False)

            self.movement()

    def update(self):
        self.bind_proj()
