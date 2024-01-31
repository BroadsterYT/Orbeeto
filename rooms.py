"""
Contains the room class.
"""
import pygame
from pygame.locals import *

import time
import math
import copy

import calculations as calc
import classbases as cb
import constants as cst
import controls as ctrl

import enemies
import groups
import players
import roomcontainers
import tiles
import trinkets

vec = pygame.math.Vector2
rad = math.radians


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

        self.isScrollingX = True
        self.isScrollingY = True

        self.canSwitchX = True
        self.canSwitchY = True

        self.centeringX = False
        self.centeringY = False
        self.lastRecenterX = time.time()
        self.lastRecenterY = time.time()
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
        self.lastPresses = copy.copy(ctrl.key_released)

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

    def get_accel(self) -> vec:
        final_accel = vec(0, 0)
        if self.isScrollingX:
            final_accel.x += self.__get_x_axis_output()
        if self.isScrollingY:
            final_accel.y += self.__get_y_axis_output()

        return final_accel

    def __get_x_axis_output(self) -> float:
        """Determines the amount of acceleration the room's x-axis component should have

        Returns:
            float: The room's acceleration's x-axis component
        """
        output: float = 0.0
        if ctrl.is_input_held[K_a]:
            output += self.player1.accel_const
        if ctrl.is_input_held[K_d]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grapple_speed * math.sin(rad(angle))

        return output

    def __get_y_axis_output(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have

        Returns:
            float: The room's acceleration's y-axis component
        """
        output: float = 0.0
        if ctrl.is_input_held[K_w]:
            output += self.player1.accel_const
        if ctrl.is_input_held[K_s]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grapple_speed * math.cos(rad(angle))

        return output

    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player.
        """
        if self.can_update:
            self.accel = self.get_accel()
            self.accel_movement()

            self._sprite_collide_check(self.player1, groups.all_walls)

            if self.isScrollingX and self.isScrollingY:
                for sprite in groups.all_movable:
                    self._sprite_collide_check(sprite, groups.all_walls)

            # Teleports the player
            for portal in groups.all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portal_in = portal
                    portal_out = calc.get_other_portal(portal_in)

                    if len(groups.all_portals) == 2:
                        self._teleport_player(portal_in, portal_out)

            # TODO: Find a way to implement these without having to call them every frame
            self.__recenter_player_x()
            self.__recenter_player_y()

            for sprite in self._get_sprites_to_recenter():
                sprite.movement()

    def __set_vel(self, value_x: int | float, value_y: int | float, is_additive: bool = False) -> None:
        """Sets the velocity components of the room, as well as all the sprites within the room, to zero.

        Args:
            value_x: X-axis component
            value_y: Y-axis component
            is_additive: Should the values be added to the current vel or override it?
        """
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

    def __recenter_player_x(self) -> None:
        """Moves all the objects in the room so that the player is centered along the x-axis.
        """
        if self.isScrollingX:
            if not self.centeringX:
                if self.player1.pos.x != cst.WINWIDTH // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetX = self.posCopy.x - cst.WINWIDTH // 2
                    for sprite in self._get_sprites_to_recenter():
                        sprite.pos_copy = sprite.pos.copy()

                    self.lastRecenterX = time.time()
                    self.centeringX = True

            if self.centeringX:
                weight = calc.get_time_diff(self.lastRecenterX)
                if weight <= self.recenter_weight_limit:
                    self.player1.pos.x = calc.cerp(self.posCopy.x, cst.WINWIDTH // 2, weight * 4)
                    for sprite in self._get_sprites_to_recenter():
                        sprite.pos.x = calc.cerp(sprite.pos_copy.x,
                                                 sprite.pos_copy.x - self.offsetX,
                                                 weight * (1 / self.recenter_weight_limit))
                else:
                    self.player1.pos.x = cst.WINWIDTH // 2
                    self.centeringX = False

    def __recenter_player_y(self) -> None:
        """Moves all the objects in the room so that the player is centered along the y-axis.
        """
        if self.isScrollingY:
            if not self.centeringY:
                if self.player1.pos.y != cst.WINHEIGHT // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetY = self.posCopy.y - cst.WINHEIGHT // 2
                    for sprite in self._get_sprites_to_recenter():
                        sprite.pos_copy = sprite.pos.copy()

                    self.lastRecenterY = time.time()
                    self.centeringY = True

            if self.centeringY:
                weight = calc.get_time_diff(self.lastRecenterY)
                if weight <= self.recenter_weight_limit:
                    self.player1.pos.y = calc.cerp(self.posCopy.y, cst.WINHEIGHT // 2, weight * 4)
                    for sprite in self._get_sprites_to_recenter():
                        sprite.pos.y = calc.cerp(sprite.pos_copy.y,
                                                 sprite.pos_copy.y - self.offsetY,
                                                 weight * (1 / self.recenter_weight_limit))
                else:
                    self.player1.pos.y = cst.WINHEIGHT // 2
                    self.centeringY = False

    def _get_sprites_to_recenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is centered.

        Returns:
            list: A list containing all sprites that should be relocated when the player is centered
        """
        output_list = []
        for sprite in self.sprites():
            output_list.append(sprite)

        for drop in groups.all_drops:
            if drop.visible:
                output_list.append(drop)

        for container in groups.all_containers:
            if container.room == self.room:
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

        if self.isScrollingX and self.isScrollingY:
            if direction_in == cst.EAST:
                direction_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif direction_in == cst.NORTH:
                direction_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif direction_in == cst.WEST:
                direction_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self._sprites_rotate_trajectory(direction_angles[direction_out])

        elif self.isScrollingX and not self.isScrollingY:
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

        elif not self.isScrollingX and self.isScrollingY:
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

        elif not self.isScrollingX and not self.isScrollingY:
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

    # ----------------------------- Sprite Collisions ---------------------------- #
    # noinspection SpellCheckingInspection
    def _sprite_collide_check(self, instig, *contact_list) -> None:
        """Collide check for when the room is scrolling.

        Args:
            instig: The sprite instigating the collision
            *contact_list: The sprite group(s) to check for a collision with

        Returns:
            None
        """
        for group in contact_list:
            for sprite in group:
                if sprite.visible and isinstance(instig, players.Player):
                    self._player_block_from_side(instig, sprite)
                elif sprite.visible:
                    self._sprite_block_from_side(instig, sprite)

    def _player_block_from_side(self, instig, sprite):
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if calc.triangle_collide(instig, sprite) == cst.SOUTH and (
                    instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self.accel.y = 0
                self.vel.y = 0
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y + height
                # self.__recenter_player_y()

            if calc.triangle_collide(instig, sprite) == cst.EAST and (
                    instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self.accel.x = 0
                self.vel.x = 0
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x + width
                # self.__recenter_player_x()

            if calc.triangle_collide(instig, sprite) == cst.NORTH and (
                    instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self.accel.y = 0
                self.vel.y = 0
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y - height
                # self.__recenter_player_y()

            if calc.triangle_collide(instig, sprite) == cst.WEST and (
                    instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self.accel.x = 0
                self.vel.x = 0
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x - width
                # self.__recenter_player_x()

    @staticmethod
    def _sprite_block_from_side(instig, sprite) -> None:
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

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

    def _check_room_change(self) -> None:
        """If the player touches a room border, he/she will change rooms.
        """
        if not self.centeringX and not self.centeringY:
            self._change_room()

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

        scroll_copy_x = copy.copy(self.isScrollingX)
        scroll_copy_y = copy.copy(self.isScrollingY)
        self.isScrollingX = can_scroll_x
        self.isScrollingY = can_scroll_y

        self._get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                         player_vel_copy)

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
                self.__set_vel(-player_vel.x, 0)

        if prev_room_scroll_y:
            if not new_room_scroll_y:
                self.player1.vel.y = -self.vel.y

        elif not prev_room_scroll_y:
            if new_room_scroll_y:
                self.__set_vel(0, -player_vel.y)

    def layout_update(self) -> None:
        """Updates the layout of the room
        """
        for sprite in self.sprites():
            sprite.kill()

        for container in groups.all_containers:
            container.hide_sprites()

        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            self.add(
                tiles.Wall(32, cst.WINHEIGHT // 2, 4, cst.WINHEIGHT // 16)
            )

            try:
                container = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    roomcontainers.RoomContainer(
                        self.room.x, self.room.y,
                        trinkets.Button(1, 14, 16),
                        trinkets.Box(cst.WINWIDTH // 2, cst.WINHEIGHT // 2),
                        trinkets.LockedWall(64, 64, 120, 120, 1, 4, 4),
                        enemies.StandardGrunt(200, 200),
                        # enemies.Ambusher(500, 500),
                    )
                )
            self._init_room(cst.WINWIDTH, cst.WINHEIGHT, True, True)

        if self.room == vec(0, 1):
            self.add(
                tiles.Wall(cst.WINWIDTH // 4 + 32, cst.WINHEIGHT // 4 + 32, 4, 4)
            )

            try:
                container = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    roomcontainers.RoomContainer(
                        self.room.x, self.room.y,
                        # Box(300, 400)
                    )
                )
            self._init_room(cst.WINWIDTH // 2, cst.WINHEIGHT // 2, False, False)

        if self.room == vec(1, 0):
            self.add()

            try:
                container = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    roomcontainers.RoomContainer(
                        self.room.x, self.room.y,
                        # Box(300, 400)
                    )
                )
            self._init_room(cst.WINWIDTH, cst.WINHEIGHT, False, False)

    def update(self):
        self._check_room_change()
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'
