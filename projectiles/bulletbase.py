import random as rand
import time

import pygame

from projectiles import explosions
from text import display_text

import calculations as calc
import classbases as cb
import constants as cst
import groups


class BulletBase(cb.ActorBase):
    def __init__(self):
        """The base class for all projectiles"""
        super().__init__()
        self.ric_count = 1
        self.start_time = time.time()

        self.hit = None
        self.sideHit = None

    def get_vel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_vel = self.vel_const + room.vel

        return final_vel

    def land(self, target) -> None:
        self.hit = target
        self.sideHit = calc.triangle_collide(self, self.hit)
        self.ric_count -= 1

        boom_pos_x = 0
        boom_pos_y = 0

        # Bullet explodes
        if self.ric_count <= 0 or self.hit in groups.all_enemies:
            if self.sideHit == cst.SOUTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y + self.hit.hitbox.height // 2
            if self.sideHit == cst.EAST:
                boom_pos_x = self.hit.pos.x + self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y
            if self.sideHit == cst.NORTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y - self.hit.hitbox.height // 2
            if self.sideHit == cst.WEST:
                boom_pos_x = self.hit.pos.x - self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y

            groups.all_explosions.add(explosions.StdBulletExplode(self, boom_pos_x, boom_pos_y))
            self.kill()

        # Bullet ricochets
        else:
            room = cb.get_room()
            room_vel = room.vel

            if self.sideHit == cst.SOUTH:
                self.pos.y = self.hit.pos.y + self.hit.hitbox.height // 2 + self.hitbox.height // 2 + abs(room_vel.y)
                self.vel_const.y = -self.vel_const.y
                self.vel.y = -self.vel.y
                print(cst.SOUTH)

            elif self.sideHit == cst.EAST:
                self.pos.x = self.hit.pos.x + self.hit.hitbox.width // 2 + self.hitbox.width // 2 + abs(room_vel.x)
                self.vel_const.x = -self.vel_const.x
                self.vel.x = -self.vel.x
                print(cst.EAST)

            elif self.sideHit == cst.NORTH:
                self.pos.y = self.hit.pos.y - self.hit.hitbox.height // 2 - self.hitbox.height // 2 - abs(room_vel.y)
                self.vel_const.y = -self.vel_const.y
                self.vel.y = -self.vel.y
                print(cst.NORTH)

            elif self.sideHit == cst.WEST:
                self.pos.x = self.hit.pos.x - self.hit.hitbox.width // 2 - self.hitbox.width // 2 - abs(room_vel.x)
                self.vel_const.x = -self.vel_const.x
                self.vel.x = -self.vel.x
                print(cst.WEST)

            self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def proj_collide(self, sprite_group, can_hurt) -> None:
        """Destroys the projectile upon a collision and renders an explosion

        Args:
            sprite_group: The group to check for a collision with.
            can_hurt: Can the projectile damage sprites in the group to check for? True if yes, false if no.

        Returns:
            None
        """
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue

            if not collidingSprite.visible:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, collidingSprite)
                if hasattr(collidingSprite, 'last_hit'):
                    collidingSprite.last_hit = time.time()
                self.land(collidingSprite)

            elif not can_hurt:
                if sprite_group == groups.all_portals:
                    if len(groups.all_portals) == 2:
                        for portal in groups.all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))
                        return

                    elif len(groups.all_portals) < 2:
                        self.land(collidingSprite)
                        return

                else:
                    self.land(collidingSprite)

    def inflict_damage(self, sprite_group, receiver) -> None:
        """Executes the subtraction of ``hp`` after a sprite is struck by a projectile

        ### Arguments
            - spriteGroup (``pygame.sprite.Group``): The group that the receiving sprite is a member of
            - sender (``ActorBase``): The sprite that fired the projectile
            - receiver (``ActorBase``): The sprite being hit by the projectile
        """
        damage = calc.calculate_damage(receiver, self)
        if sprite_group == groups.all_enemies:
            if rand.randint(1, 20) == 1:
                receiver.hp -= damage * 3
                if damage > 0:
                    groups.all_font_chars.add(display_text.IndicatorText(receiver.pos.x, receiver.pos.y, damage * 3))
            else:
                receiver.hp -= damage
                if damage > 0:
                    groups.all_font_chars.add(display_text.IndicatorText(receiver.pos.x, receiver.pos.y, damage))

        elif sprite_group == groups.all_players:
            receiver.hp -= damage
            if damage > 0:
                groups.all_font_chars.add(display_text.IndicatorText(receiver.pos.x, receiver.pos.y, damage))
            receiver.dodge_time = 0
            receiver.last_hit = time.time()

        else:
            receiver.hp -= damage
            if damage > 0:
                groups.all_font_chars.add(display_text.IndicatorText(receiver.pos.x, receiver.pos.y, damage))

    def update(self):
        room = cb.get_room()
        if (
                self.pos.y > room.borderSouth.pos.y or
                self.pos.x > room.borderEast.pos.x or
                self.pos.y < room.borderNorth.pos.y or
                self.pos.x < room.borderWest.pos.x
        ):
            self.kill()
