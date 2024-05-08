import random as rand
import time

import pygame

from projectiles import explosions
from text import display_text
import screen

import calc
import classbases as cb
import constants as cst
import groups


class BulletBase(cb.ActorBase):
    def __init__(self, damage: int = 0, dmg_mod: int = 1):
        """The base class for all projectiles

        :param damage: The amount of damage the projectile should inflict (if any)
        :param dmg_mod: The multiplier to give to the damage field
        """
        super().__init__(cst.LAYER['proj'])
        self.ric_count = 1
        self.start_time = time.time()

        self.damage = damage
        self.dmg_mod = dmg_mod

        self.hit = None
        self.side_hit = None

    def get_vel(self) -> pygame.math.Vector2:
        """Returns the velocity the bullet should have

        :return: The velocity vector to assign to the bullet
        """
        room = cb.get_room()
        final_vel = self.vel_const + room.vel.copy()

        return final_vel * screen.dt * cst.M_FPS

    def land(self, target) -> None:
        """Destroys the bullet and renders an explosion or bounces the bullet

        :param target: The sprite the bullet collided with
        :return: None
        """
        self.hit = target
        self.side_hit = calc.triangle_collide(self, self.hit)
        self.ric_count -= 1

        boom_pos_x = 0
        boom_pos_y = 0

        # Bullet explodes
        if self.ric_count <= 0 or self.hit in groups.all_enemies:
            if self.side_hit == cst.SOUTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y + self.hit.hitbox.height // 2
            if self.side_hit == cst.EAST:
                boom_pos_x = self.hit.pos.x + self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y
            if self.side_hit == cst.NORTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y - self.hit.hitbox.height // 2
            if self.side_hit == cst.WEST:
                boom_pos_x = self.hit.pos.x - self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y

            self.kill()
            groups.all_explosions.add(explosions.StdBulletExplode(self, boom_pos_x, boom_pos_y))
            # TODO: Fix extra explosion spawns on player bullets that hit portals

        # Bullet ricochets
        else:
            room = cb.get_room()
            room_vel = room.vel

            if self.side_hit == cst.SOUTH:
                self.pos.y = self.hit.pos.y + self.hit.hitbox.height // 2 + self.hitbox.height // 2 + abs(room_vel.y)
                self.vel_const.y = -self.vel_const.y
                self.vel.y = -self.vel.y

            elif self.side_hit == cst.EAST:
                self.pos.x = self.hit.pos.x + self.hit.hitbox.width // 2 + self.hitbox.width // 2 + abs(room_vel.x)
                self.vel_const.x = -self.vel_const.x
                self.vel.x = -self.vel.x

            elif self.side_hit == cst.NORTH:
                self.pos.y = self.hit.pos.y - self.hit.hitbox.height // 2 - self.hitbox.height // 2 - abs(room_vel.y)
                self.vel_const.y = -self.vel_const.y
                self.vel.y = -self.vel.y

            elif self.side_hit == cst.WEST:
                self.pos.x = self.hit.pos.x - self.hit.hitbox.width // 2 - self.hitbox.width // 2 - abs(room_vel.x)
                self.vel_const.x = -self.vel_const.x
                self.vel.x = -self.vel.x

            self.rotate_image(calc.get_vec_angle(self.vel.x, self.vel.y))

    def proj_collide(self, sprite_group, can_hurt) -> None:
        """Checks for a collision with all sprites within a specific sprite group and allows the bullet to act
        accordingly.

        :param sprite_group: The group to check for a collision with
        :param can_hurt: Can the projectile damage sprites in the group to check for? True if yes, false if no.
        :return: None
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
                        self.land(self)
                        return

                else:
                    self.land(collidingSprite)
                    return

    def inflict_damage(self, sprite_group, receiver) -> None:
        """Calculates the damage a bullet should inflict on a sprite and subtracts it from that sprite's HP

        :param sprite_group: The group the sprite being shot is in
        :param receiver: The sprite being hit by the bullet
        :return: None
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
            self.pos.y > room.border_south.pos.y or
            self.pos.x > room.border_east.pos.x or
            self.pos.y < room.border_north.pos.y or
            self.pos.x < room.border_west.pos.x
        ):
            self.kill()
        pygame.draw.rect(screen.buffer_screen, cst.RED, self.hitbox)
