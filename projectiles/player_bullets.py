import math
import time

from pygame.math import Vector2 as vec

from projectiles import bulletbase as bb

import classbases as cb
import calculations as calc
import constants as cst
import groups

import portals
import visuals


# ============================================================================ #
#                                Player Bullets                                #
# ============================================================================ #
class PlayerStdBullet(bb.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        """A projectile fired by a player that moves at a constant velocity.

        Args:
            pos_x: The x-position where the bullet should be spawned
            pos_y: The y-position where the bullet should be spawned
            vel_x: The x-axis component of the bullet's velocity
            vel_y: The y-axis component of the bullet's velocity
            bounce_count: The amount of times the bullet should bounce. (1 = no bounce)
        """
        super().__init__(cst.PROJ_DAMAGE[cst.PROJ_STD])
        self.layer = cst.LAYER['proj']
        self.show(self.layer)

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = self.vel
        self.ricCount = bounce_count

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.can_update:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_time_diff(self.start_time) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(False)
            else:
                self.kill()

    def update(self):
        # self.movement()
        super().update()

    def __repr__(self):
        return f'PlayerStdBullet({self.pos}, {self.vel}, {self.ricCount})'


class PlayerLaserBullet(bb.BulletBase):
    def __init__(self, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        super().__init__(cst.PROJ_DAMAGE[cst.PROJ_LASER])
        self.layer = cst.LAYER['proj']
        self.show(self.layer)

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = self.vel
        self.ricCount = bounce_count

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 1, 4)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 10, 10)

        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.can_update:
            self.proj_collide(groups.all_enemies, True)
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_time_diff(self.start_time) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(False)
            else:
                self.kill()

    def update(self):
        self.movement()
        super().update()


# ------------------------------ Utility Bullets ----------------------------- #
class PortalBullet(bb.BulletBase):
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        super().__init__()
        self.layer = cst.LAYER['proj']
        self.show(self.layer)

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = self.vel

        self.hitbox_adjust = vec(0, 0)

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 5, 8)
        self.set_rects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def proj_collide(self, sprite_group, can_hurt: bool):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
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

        Args:
            surface: The surface the portal bullet landed on.

        Returns:
            None
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
        if self.can_update:
            self.proj_collide(groups.all_walls, False)
            self.proj_collide(groups.all_portals, False)

            if calc.get_time_diff(self.start_time) <= 5:
                self.vel = self.get_vel()
                self.vel_movement(False)
            else:
                self.kill()

    def update(self):
        if calc.get_time_diff(self.last_frame) > 0.1:  # TODO: Use SPF to standardize animation
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.last_frame = time.time()

        rotate_angle = int(calc.get_vec_angle(self.vel_const.x, self.vel_const.y))
        self.rotate_image(rotate_angle)
        # self.movement()

    def __repr__(self):
        return f'PortalBullet({self.pos}, {self.vel}, {self.ric_count})'


class GrappleBullet(bb.BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float):
        super().__init__()
        self.layer = cst.LAYER['grapple']
        self.show(self.layer)
        self.damage = cst.PROJ_DAMAGE[cst.PROJ_GRAPPLE]
        
        self.shot_from = shot_from

        self.isHooked = False
        self.grappledTo = None
        self.posOffset = vec(0, 0)
        
        self.returning = False

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.vel_const = self.vel
        self.accel = vec(0, 0)
        self.accel_const = 1.5

        self.chain = visuals.Beam(self, self.shot_from)
        self.portalList = []

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 2, 16)
        self.set_rects(0, 0, 32, 32, 16, 16)
        self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def land(self, grappled_to):
        if not self.returning:  # Hook won't scoop thing up on the way back to the player
            self.isHooked = True
            self.grappledTo = grappled_to
            self.grappledTo.grappled_by = self
            if self.grappledTo is not None:
                self.grappledTo.is_grappled = True
                self.posOffset = vec(self.pos.x - self.grappledTo.pos.x, self.pos.y - self.grappledTo.pos.y)

    def shatter(self):
        """Completely destroys the grappling hook.
        """
        self.returning = False
        self.shot_from.grapple = None
        if self.grappledTo is not None:
            self.grappledTo.is_grappled = False

        self.portalList = []

        self.chain.kill()
        self.kill()

    def proj_collide(self, sprite_group, can_hurt):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, collidingSprite)
                self.land(collidingSprite)

            elif not can_hurt:
                if sprite_group == groups.all_portals:
                    if len(groups.all_portals) == 2:
                        for portal in groups.all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.portalList.append(portal)
                                self.portalList.append(calc.get_other_portal(portal))
                                self.teleport(portal)
                                self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))
                        return

                else:
                    self.land(collidingSprite)

    def send_back(self):
        if self.grappledTo not in groups.all_walls:
            # Hook returns to portal it entered
            if len(self.portalList) > 1:
                angle = calc.get_angle(self, self.portalList[1])
                room = cb.get_room()
                room_accel = room.get_accel()
                self.accel.x = self.accel_const * -math.sin(math.radians(angle)) + room_accel.x
                self.accel.y = self.accel_const * -math.cos(math.radians(angle)) + room_accel.y
                # self.pos = self.grappledTo.pos

                if self.hitbox.colliderect(self.portalList[1]):
                    self.portalList = []
            
            # Hook returns to player
            else:
                angle = calc.get_angle(self, self.shot_from)
                room = cb.get_room()
                room_accel = room.get_accel()
                self.accel.x = self.accel_const * -math.sin(math.radians(angle)) + room_accel.x
                self.accel.y = self.accel_const * -math.cos(math.radians(angle)) + room_accel.y

                # Hook disappears once it returns
                if self.hitbox.colliderect(self.shot_from.hitbox):
                    self.shatter()
            
            self.accel_movement()

            # Hook follows whatever it has grabbed
            if self.grappledTo is not None and self.grappledTo not in groups.all_portals:
                if self.grappledTo not in groups.all_walls:
                    self.grappledTo.pos = self.pos

        # Player should accelerate to the hook
        else:
            self.pos = self.grappledTo.pos + self.posOffset
            if self.hitbox.colliderect(self.shot_from.hitbox):
                self.shatter()

    def movement(self):
        if not self.returning:
            if not self.isHooked:
                self.vel = self.get_vel()
                self.vel_movement(True)

            elif self.isHooked:
                if self.grappledTo is not None and self.grappledTo not in groups.all_walls:
                    self.pos.x = self.grappledTo.pos.x
                    self.pos.y = self.grappledTo.pos.y
                
                elif self.grappledTo is not None and self.grappledTo in groups.all_walls:
                    self.pos = self.grappledTo.pos + self.posOffset
                
                else:
                    self.pos = self.pos
        
        elif self.returning:
            self.send_back()

        self.center_rects()

    def bind_proj(self):
        if self.can_update and self.visible:
            if not self.isHooked:
                self.proj_collide(groups.all_enemies, True)
                self.proj_collide(groups.all_movable, False)
                self.proj_collide(groups.all_portals, False)
                self.proj_collide(groups.all_walls, False)
                self.proj_collide(groups.all_drops, False)

            self.movement()

    def update(self):
        self.bind_proj()
