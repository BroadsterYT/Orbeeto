"""
Contains the room class.
"""
import time
import copy
import math

import itertools
import pygame
from pygame.math import Vector2 as vec

import controls.key_trackers as kt
import text.display_text
from controls.keybinds import *

import calculations as calc
import classbases as cb
import constants as cst
import enemies
import groups
import players
import roomcontainers
import tiles
import trinkets


# noinspection PyTypeChecker
class Room(cb.AbstractBase):
    def __init__(self, room_x: float, room_y: float):
        """The room where all the current action is taking place

        Args:
            room_x: The room's x-axis location in the grid of the room layout
            room_y: The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        groups.all_rooms.append(self)
        self.room = vec((room_x, room_y))
        self.size = vec((1280, 720))

        self.lastEntranceDir = None

        self.player1 = players.Player()
        self.posCopy = self.player1.pos.copy()
        self.offset = vec(self.player1.pos.x - 608, self.player1.pos.y - cst.WINHEIGHT // 2)

        self.borderSouth = tiles.RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.borderEast = tiles.RoomBorder(cst.WINWIDTH // 16, 0, 1, self.size.y // 16)
        self.borderNorth = tiles.RoomBorder(0, -1, self.size.x // 16, 1)
        self.borderWest = tiles.RoomBorder(-1, 0, 1, self.size.y // 16)
        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

        self.is_scrolling_x = True
        self.is_scrolling_y = True

        self.centering_x = False
        self.centering_y = False
        self.recenter_weight_limit = 0.25

        self.offsetX = self.player1.pos.x - cst.WINWIDTH // 2
        self.offsetY = self.player1.pos.y - cst.WINHEIGHT // 2

        # --------------------------------- Movement --------------------------------- #
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.accel_const = self.player1.accel_const

        self.dashCooldown = time.time()
        self.dashTimer = time.time()
        self.dashCheck = True
        self.lastPresses = copy.copy(kt.key_released)

        self.layout_update()

    # ------------------------------- Room Movement ------------------------------ #
    def accel_movement(self) -> None:
        """Calculates the room's acceleration, velocity, and position
        """
        self.accel.x += self.vel.x * cst.FRIC
        self.accel.y += self.vel.y * cst.FRIC
        self.vel += self.accel

        self.pos = vec(self.borderWest.pos.x + self.borderWest.hitbox.width // 2,
                       self.borderNorth.pos.y + self.borderNorth.height // 2)

        # if self.size.x >= cst.WINWIDTH:
        #     self.pos.x = self.borderWest.pos.x + self.borderWest.hitbox.width // 2
        # else:
        #     pass
        #
        # if self.size.y >= cst.WINHEIGHT:
        #     self.pos.y = self.borderNorth.pos.y + self.borderNorth.height // 2
        # else:
        #     pass

    def get_accel(self) -> vec:
        final_accel = vec(0, 0)
        if self.is_scrolling_x:
            final_accel.x += self._get_x_axis_output()
        if self.is_scrolling_y:
            final_accel.y += self._get_y_axis_output()

        # Centering player in scrolling room
        scroll_weight = calc.get_scroll_weight(self.player1)
        if self.is_scrolling_x:
            if self.player1.pos.x != cst.WINWIDTH // 2:
                final_accel.x += scroll_weight.x
        if self.is_scrolling_y:
            if self.player1.pos.y != cst.WINHEIGHT // 2:
                final_accel.y += scroll_weight.y

        return final_accel

    def _get_x_axis_output(self) -> float:
        """Determines the amount of acceleration the room's x-axis component should have

        Returns:
            float: The room's acceleration's x-axis component
        """
        output = 0.0
        if kt.is_input_held[K_MOVE_LEFT]:
            output += self.player1.accel_const
        if kt.is_input_held[K_MOVE_RIGHT]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle(self.player1, self.player1.grapple)
            output += self.player1.grapple_speed * math.sin(math.radians(angle))

        return output

    def _get_y_axis_output(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have

        Returns:
            float: The room's acceleration's y-axis component
        """
        output = 0.0
        if kt.is_input_held[K_MOVE_UP]:
            output += self.player1.accel_const
        if kt.is_input_held[K_MOVE_DOWN]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle(self.player1, self.player1.grapple)
            output += self.player1.grapple_speed * math.cos(math.radians(angle))

        return output

    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player.
        """
        if self.can_update:
            self.accel = self.get_accel()
            self.accel_movement()

            self._sprite_collide_check(self.player1, groups.all_walls)

            if self.is_scrolling_x and self.is_scrolling_y:
                for sprite in groups.all_movable:
                    self._sprite_collide_check(sprite, groups.all_walls)

            # Teleports the player
            for portal in groups.all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portal_in = portal
                    portal_out = calc.get_other_portal(portal_in)

                    if len(groups.all_portals) == 2:
                        self._teleport_player(portal_in, portal_out)

            for sprite in self._get_sprites_to_recenter():
                sprite.movement()

    def _set_vel(self, value_x: int | float, value_y: int | float, is_additive: bool = False) -> None:
        """Sets the velocity components of the room, as well as all the sprites within the room, to zero.

        Args:
            value_x: X-axis component
            value_y: Y-axis component
            is_additive: Should the values be added to the current vel or override it?
        """
        # TODO: Make an exception for enemies when the player is pushing up against something
        if not is_additive:
            self.vel = vec(value_x, value_y)
            for sprite in self._get_sprites_to_recenter():
                sprite.vel = vec(value_x, value_y)
        if is_additive:
            self.vel.x += value_x
            self.vel.y += value_y
            for sprite in self._get_sprites_to_recenter():
                sprite.vel.x += value_x
                sprite.vel.y += value_y

    def _recenter_player_x(self) -> None:
        """Moves all the objects in the room so that the player is centered along the x-axis.
        """
        if self.is_scrolling_x and self.player1.pos.x != cst.WINWIDTH // 2:
            self.posCopy = self.player1.pos.copy()
            self.offsetX = self.posCopy.x - cst.WINWIDTH // 2
            for sprite in self._get_sprites_to_recenter():
                sprite.pos_copy = sprite.pos.copy()
                sprite.pos.x = sprite.pos_copy.x - self.offsetX
            self.player1.pos.x = cst.WINWIDTH // 2

    def _recenter_player_y(self) -> None:
        """Moves all the objects in the room so that the player is centered along the y-axis.
        """
        if self.is_scrolling_y and self.player1.pos.y != cst.WINHEIGHT // 2:
            self.posCopy = self.player1.pos.copy()
            self.offsetY = self.posCopy.y - cst.WINHEIGHT // 2
            for sprite in self._get_sprites_to_recenter():
                sprite.pos_copy = sprite.pos.copy()
                sprite.pos.y = sprite.pos_copy.y - self.offsetY
            self.player1.pos.y = cst.WINHEIGHT // 2

    def _get_sprites_to_recenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is centered.

        Returns:
            list: A list containing all sprites that should be relocated when the player is centered
        """
        output_list = []
        for sprite in [s for s in
                       itertools.chain(self.sprites(), groups.all_projs, groups.all_drops)
                       if s.visible]:
            output_list.append(sprite)

        for container in [c for c in groups.all_containers if c.room == self.room]:
            for sprite in container:
                output_list.append(sprite)

        return output_list

    # -------------------------------- Teleporting ------------------------------- #
    def _align_player_after_tp(self, offset: float, direction: str, portal_out, width, height) -> None:
        """Sets the player at the proper position after teleporting when the room can scroll.

        Args:
            offset: The distance the player is (on either x or y-axis, not both) from the center of the entering portal
            direction: The direction the exit portal is facing
            portal_out: The exit portal sprite
            width: Half the sum of the player's hitbox width plus the portal's hitbox width
            height: Half the sum of the player's hitbox height plus the portal's hitbox height
        """
        if direction == cst.SOUTH:
            self.player1.pos.x = portal_out.pos.x - offset
            self.player1.pos.y = portal_out.pos.y + height

        elif direction == cst.EAST:
            self.player1.pos.x = portal_out.pos.x + width
            self.player1.pos.y = portal_out.pos.y - offset

        elif direction == cst.NORTH:
            self.player1.pos.x = portal_out.pos.x + offset
            self.player1.pos.y = portal_out.pos.y - height

        elif direction == cst.WEST:
            self.player1.pos.x = portal_out.pos.x - width
            self.player1.pos.y = portal_out.pos.y + offset

    def _teleport_player(self, portal_in, portal_out) -> None:
        """Teleports the player when the room is scrolling.

        Args:
            portal_in: The portal the player is entering
            portal_out: The portal the player is exiting
        """
        combined_width = (portal_out.hitbox.width + self.player1.hitbox.width) // 2
        combined_height = (portal_out.hitbox.height + self.player1.hitbox.height) // 2
        direction_in = portal_in.facing
        direction_out = portal_out.facing
        direction_angles = {cst.SOUTH: 180, cst.EAST: 90, cst.NORTH: 0, cst.WEST: 270}

        # Calculating where player should exit portal relative to the position entered
        distance_offset = 0.0
        if direction_in in [cst.SOUTH, cst.NORTH]:
            distance_offset = self.player1.pos.x - portal_in.pos.x
        elif direction_in in [cst.EAST, cst.WEST]:
            distance_offset = self.player1.pos.y - portal_in.pos.y

        # Actually teleporting the player
        self._align_player_after_tp(distance_offset, direction_out, portal_out, combined_width, combined_height)

        if self.is_scrolling_x and self.is_scrolling_y:
            if direction_in == cst.EAST:
                direction_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif direction_in == cst.NORTH:
                direction_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif direction_in == cst.WEST:
                direction_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self._sprites_rotate_trajectory(direction_angles[direction_out])

        elif self.is_scrolling_x and not self.is_scrolling_y:
            if direction_in == cst.SOUTH:
                direction_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self._translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == cst.EAST:
                direction_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if direction_out == direction_in:
                    self._sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

            if direction_in == cst.NORTH:
                direction_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self._translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == cst.WEST:
                direction_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if direction_out == direction_in:
                    self._sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

        elif not self.is_scrolling_x and self.is_scrolling_y:
            if direction_in == cst.SOUTH:
                direction_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if direction_out == direction_in:
                    self._sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self._translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == cst.EAST:
                direction_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

            if direction_in == cst.NORTH:
                direction_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if direction_out == direction_in:
                    self._sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self._translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == cst.WEST:
                direction_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

        elif not self.is_scrolling_x and not self.is_scrolling_y:
            if direction_in == cst.EAST:
                direction_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif direction_in == cst.NORTH:
                direction_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif direction_in == cst.WEST:
                direction_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])

    def _sprites_rotate_trajectory(self, angle: float) -> None:
        """Rotates the velocities and accelerations of all the sprites within the room's sprites.

        Args:
            angle: The angle to rotate the vectors by

        Returns:
            None
        """
        self.accel = self.accel.rotate(angle)
        self.vel = self.vel.rotate(angle)

        for sprite in self._get_sprites_to_recenter():
            sprite.accel = sprite.accel.rotate(angle)
            sprite.vel = sprite.vel.rotate(angle)

    def _translate_trajectory(self, is_player_to_room: bool, angle: float) -> None:
        """Translates the velocity of the room's sprites to the player, or vice versa.

        Args:
            is_player_to_room: Should velocity be swapped from player to room (True), or from room to player (False)?
            angle: The angle to rotate the trajectory by
        """
        if is_player_to_room:
            for sprite in self._get_sprites_to_recenter():
                sprite.vel = self.player1.vel.rotate(angle)

        elif not is_player_to_room:
            self.player1.vel = self.vel.rotate(angle)

    # noinspection SpellCheckingInspection
    def _sprite_collide_check(self, instig, *contact_list) -> None:
        """Collide check for when the room is scrolling.

        Args:
            instig: The sprite instigating the collision
            *contact_list: The sprite group(s) to check for a collision with

        Returns:
            None
        """
        for sprite in [s
                       for group in contact_list
                       for s in group
                       if s.visible]:
            self._sprite_block_from_side(instig, sprite)

    def _sprite_block_from_side(self, instig, sprite) -> None:
        width = (instig.hitbox.width + sprite.hitbox.width) // 2
        height = (instig.hitbox.height + sprite.hitbox.height) // 2
        if isinstance(instig, players.Player) and instig.hitbox.colliderect(sprite.hitbox):
            if calc.triangle_collide(instig, sprite) == cst.SOUTH and (
                    instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self._set_vel(self.vel.x, 0)
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y + height
                self._recenter_player_y()

            if calc.triangle_collide(instig, sprite) == cst.EAST and (
                    instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self._set_vel(0, self.vel.y)
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x + width
                self._recenter_player_x()

            if calc.triangle_collide(instig, sprite) == cst.NORTH and (
                    instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self._set_vel(self.vel.x, 0)
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y - height
                self._recenter_player_y()

            if calc.triangle_collide(instig, sprite) == cst.WEST and (
                    instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self._set_vel(0, self.vel.y)
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x - width
                self._recenter_player_x()

        elif instig.hitbox.colliderect(sprite.hitbox):
            if (calc.triangle_collide(instig, sprite) == cst.SOUTH and
                    instig.pos.y <= sprite.pos.y + height and (
                    instig.vel.y < 0 or sprite.vel.y > 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if (calc.triangle_collide(instig, sprite) == cst.EAST and
                    instig.pos.x <= sprite.pos.x + width and (
                    instig.vel.x < 0 or sprite.vel.x > 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if (calc.triangle_collide(instig, sprite) == cst.NORTH and
                    instig.pos.y >= sprite.pos.y - height and (
                    instig.vel.y > 0 or sprite.vel.y < 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if (calc.triangle_collide(instig, sprite) == cst.WEST and
                    instig.pos.x >= sprite.pos.x - width and (
                    instig.vel.x > 0 or sprite.vel.x < 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    # -------------------------------- Room Layout ------------------------------- #
    def _change_room(self) -> None:
        width = self.player1.hitbox.width // 2
        height = self.player1.hitbox.height // 2

        # TODO: Reset room position after changing rooms
        if self.player1.pos.y >= self.borderSouth.pos.y - height:
            self.room.y -= 1
            self.lastEntranceDir = cst.SOUTH
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.x >= self.borderEast.pos.x - width:
            self.room.x += 1
            self.lastEntranceDir = cst.EAST
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.y <= self.borderNorth.pos.y + height:
            self.room.y += 1
            self.lastEntranceDir = cst.NORTH
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.x <= self.borderWest.pos.x + width:
            self.room.x -= 1
            self.lastEntranceDir = cst.WEST
            self.layout_update()
            calc.kill_groups(groups.all_projs)

    def _set_room_borders(self, room_width: int, room_height: int) -> None:
        """Sets the borders of the room.

        Args:
            room_width: The width of the room (in pixels)
            room_height: The height of the room (in pixels)
        """
        west_coords = vec(-8, room_height // 2)
        north_coords = vec(room_width // 2, -8)
        south_coords = vec(north_coords.x, north_coords.y + room_height + 16)
        east_coords = vec(west_coords.x + room_width + 16, room_height // 2)

        if room_width < cst.WINWIDTH:
            west_coords.x = cst.WINWIDTH / 2 - room_width / 2 - 8
            east_coords.x = west_coords.x + room_width + 16
            south_coords.x = west_coords.x + room_width / 2 + 8
            north_coords.x = south_coords.x

        if room_height < cst.WINHEIGHT:
            north_coords.y = cst.WINHEIGHT / 2 - room_height / 2 - 8
            south_coords.y = north_coords.y + room_height + 16
            east_coords.y = north_coords.y + room_height / 2 + 8
            west_coords.y = east_coords.y

        self.borderSouth = tiles.RoomBorder(south_coords.x, south_coords.y, room_width / 16, 1)
        self.borderEast = tiles.RoomBorder(east_coords.x, east_coords.y, 1, room_height / 16)
        self.borderNorth = tiles.RoomBorder(north_coords.x, north_coords.y, room_width / 16, 1)
        self.borderWest = tiles.RoomBorder(west_coords.x, west_coords.y, 1, room_height / 16)

        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

    def _init_room(self, room_size_x: int, room_size_y: int, can_scroll_x: bool, can_scroll_y: bool) -> None:
        """Initializes a room's properties. This function must be called once for every room iteration.

        Args:
            room_size_x: The width of the room (in pixels).
            room_size_y: The height of the room (in pixels).
            can_scroll_x: Should the room scroll with the player along the x-axis?
            can_scroll_y: Should the room scroll with the player along the y-axis?
        """
        self._set_room_borders(room_size_x, room_size_y)
        if self.lastEntranceDir == cst.SOUTH:
            self.player1.pos.x = self.borderNorth.pos.x
            self.player1.pos.y = (self.borderNorth.pos.y + self.borderNorth.hitbox.height // 2
                                  + self.player1.hitbox.height // 2)

        elif self.lastEntranceDir == cst.EAST:
            self.player1.pos.x = (self.borderWest.pos.x +
                                  self.borderWest.hitbox.width // 2 + self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderWest.pos.y

        elif self.lastEntranceDir == cst.NORTH:
            self.player1.pos.x = self.borderSouth.pos.x
            self.player1.pos.y = (self.borderSouth.pos.y -
                                  self.borderSouth.hitbox.height // 2 - self.player1.hitbox.height // 2)

        elif self.lastEntranceDir == cst.WEST:
            self.player1.pos.x = (self.borderEast.pos.x -
                                  self.borderEast.hitbox.width // 2 - self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderEast.pos.y

        player_vel_copy = self.player1.vel.copy()
        self.player1.vel = vec(0, 0)
        self.size = vec((room_size_x, room_size_y))

        scroll_copy_x = copy.copy(self.is_scrolling_x)
        scroll_copy_y = copy.copy(self.is_scrolling_y)
        self.is_scrolling_x = can_scroll_x
        self.is_scrolling_y = can_scroll_y

        self._get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.is_scrolling_x, self.is_scrolling_y,
                                         player_vel_copy)

        # if self.is_scrolling_x:
        #     self._recenter_player_x()
        # if self.is_scrolling_y:
        #     self._recenter_player_y()

    def _get_room_change_trajectory(self, prev_room_scroll_x: bool, prev_room_scroll_y: bool, new_room_scroll_x: bool,
                                    new_room_scroll_y: bool, player_vel: pygame.math.Vector2) -> None:
        """Transfers the velocity from the room to the player or vice versa when changing rooms.

        Args:
            prev_room_scroll_x: Did the previous room scroll along the x-axis?
            prev_room_scroll_y: Did the previous room scroll along the y-axis?
            new_room_scroll_x: Does the new room scroll along the x-axis?
            new_room_scroll_y: Does the new room scroll along the y-axis?
            player_vel: The player's velocity
        """
        if prev_room_scroll_x:
            if not new_room_scroll_x:
                self.player1.vel.x = -self.vel.x

        elif not prev_room_scroll_x:
            if new_room_scroll_x:
                self._set_vel(-player_vel.x, 0)

        if prev_room_scroll_y:
            if not new_room_scroll_y:
                self.player1.vel.y = -self.vel.y

        elif not prev_room_scroll_y:
            if new_room_scroll_y:
                self._set_vel(0, -player_vel.y)

    def layout_update(self) -> None:
        """Updates the layout of the room
        """
        for sprite in self.sprites():
            sprite.kill()

        for container in groups.all_containers:
            container.hide_sprites()

        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            try:
                container = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    roomcontainers.RoomContainer(
                        self.room.x, self.room.y,
                        # tiles.Wall(32, 512, 4, 64),
                        # tiles.Wall(self.pos.x, self.pos.y, 4, 64),
                        # tiles.Floor(cst.WINWIDTH // 2, cst.WINHEIGHT // 2, 80, 80),

                        trinkets.Button(1, 14, 16),
                        trinkets.Box(cst.WINWIDTH // 2, cst.WINHEIGHT // 2),
                        trinkets.LockedWall(128, 64, 256, 100, 1, 4, 4),
                        enemies.StandardGrunt(0, 0),
                        enemies.Ambusher(600, 600)
                    )
                )
            self._init_room(1280, 720, True, True)

        if self.room == vec(0, 1):
            try:
                container = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    roomcontainers.RoomContainer(
                        self.room.x, self.room.y,
                        tiles.Wall(0, 0, 4, 4),
                        enemies.StandardGrunt(0, 0),
                    )
                )
            self._init_room(640, 360, True, True)
            # print(self.borderWest.pos.x, self.pos.x, self.borderWest.pos.x - self.pos.x)
            print(self.borderSouth.pos.y)

    def generate_room(self, *sprites) -> None:
        """

        Args:
            *sprites:

        Returns:
            None
        """
        try:
            container = next(c for c in groups.all_containers if c.room == self.room)
            container.show_sprites()
            print(f'Found container for room {self.room}')

        except StopIteration:
            print(f'Failed search for room {self.room}')
            new_container = roomcontainers.RoomContainer(
                self.room.x, self.room.y,
                *sprites
            )
            groups.all_containers.append(new_container)

    def update(self):
        text.display_text.draw_text(self.__repr__(), 0, 0)
        self._change_room()
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'
