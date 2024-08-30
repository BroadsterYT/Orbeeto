import copy
import os

import pygame
from pygame.math import Vector2 as vec

import calc
import classbases as cb
import constants as cst
import groups


class Box(cb.ActorBase):
    def __init__(self, pos_x, pos_y):
        """A box that can be pushed around and activate buttons.

        :param pos_x: The position on the x-axis to spawn the box
        :param pos_y: The position on the y-axis to spawn the box
        """
        super().__init__(cst.LAYER['trinket'])
        self.add_to_gamestate()
        groups.all_movable.add(self)

        self.pos = vec((pos_x, pos_y))
        self.accel_const = 0.58

        self.set_room_pos()

        self.set_images(os.path.join(os.getcwd(), 'sprites/textures/box.png'), 64, 64, 5, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 64, 64, True)

    def movement(self):
        if self.in_gamestate:
            self.collide_check(groups.all_walls)

            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()

        if self.hitbox.colliderect(room.player1.hitbox):
            if calc.triangle_collide(self, room.player1) == cst.SOUTH:
                final_accel.y += 0.8
            if calc.triangle_collide(self, room.player1) == cst.EAST:
                final_accel.x += 0.8
            if calc.triangle_collide(self, room.player1) == cst.NORTH:
                final_accel.y -= 0.8
            if calc.triangle_collide(self, room.player1) == cst.WEST:
                final_accel.x -= 0.8

        return final_accel

    def teleport(self, portal_in):
        portal_out = calc.get_other_portal(portal_in)
        dir_in = portal_in.facing
        dir_out = portal_out.facing

        dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
        dir_list = {cst.SOUTH: 180, cst.EAST: 90, cst.NORTH: 0, cst.WEST: 270}

        if dir_in == cst.SOUTH:
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)

        elif dir_in == cst.EAST:
            dir_list.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

        elif dir_in == cst.NORTH:
            dir_list.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)

        elif dir_in == cst.WEST:
            dir_list.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

        # This part is changed from ActorBase to account for the room's acceleration, as well as the fact that the box
        # uses acceleration, not velocity, as its movement standard
        room = cb.get_room()
        self._align_sprite(portal_out, dist_offset, dir_out)
        true_vel = self.vel.copy() - room.vel.copy()
        self.vel = true_vel.rotate(dir_list[dir_out]) + room.vel

    def update(self):
        # Teleporting
        for portal in groups.all_portals:
            if self.hitbox.colliderect(portal.hitbox) and len(groups.all_portals) == 2 and not self.is_grappled:
                self.teleport(portal)

    def __repr__(self):
        return f'Box({self.pos}, {self.vel}, {self.accel})'
