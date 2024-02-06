"""
Contains the object classes that the player can interact with/manipulate within the game.
"""
import pygame
from pygame.math import Vector2 as vec

from text import display_text

import classbases as cb
import constants as cst
import calculations as calc

import groups
import tiles


class Box(cb.ActorBase):
    def __init__(self, pos_x, pos_y):
        """A box that can be pushed around and activate buttons.

        Args:
            pos_x: The position on the x-axis to spawn the box
            pos_y: The position on the y-axis to spawn the box
        """
        super().__init__()
        self.layer = cst.LAYER['trinket']
        self.show(self.layer)
        groups.all_movable.add(self)

        self.pos = vec((pos_x, pos_y))
        self.accel_const = 0.58

        room = cb.get_room()
        self.roomPos = vec((self.pos.x - room.pos.x, self.pos.y - room.pos.y))

        self.set_images("sprites/textures/box.png", 64, 64, 5, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 64, 64, True)

    def movement(self):
        if self.can_update and self.visible:
            self.collide_check(groups.all_walls)

            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = cb.get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()

        for a_player in groups.all_players:
            if self.hitbox.colliderect(a_player.hitbox):
                if calc.triangle_collide(self, a_player) == cst.SOUTH:
                    final_accel.y += 0.8
                if calc.triangle_collide(self, a_player) == cst.EAST:
                    final_accel.x += 0.8
                if calc.triangle_collide(self, a_player) == cst.NORTH:
                    final_accel.y -= 0.8
                if calc.triangle_collide(self, a_player) == cst.WEST:
                    final_accel.x -= 0.8

        return final_accel

    def update(self):
        # Teleporting
        for portal in groups.all_portals:
            if self.hitbox.colliderect(portal.hitbox) and len(groups.all_portals) == 2:
                self.teleport(portal)

    def __repr__(self):
        return f'Box({self.pos}, {self.vel}, {self.accel})'


class Button(cb.ActorBase):
    def __init__(self, id_value: int, block_pos_x: int, block_pos_y: int):
        """A button that can be activated and deactivated

        Args:
            id_value: The ID vale of the button. Will activate any trinket with the same ID value.
            block_pos_x: The x-axis position of the button (in blocks)
            block_pos_y: The y-axis position of the button (in blocks)
        """
        super().__init__()
        self.layer = cst.LAYER['button']
        self.show(self.layer)
        groups.all_trinkets.add(self)

        self.id_value = id_value
        self.activated = False

        self.pos = vec((block_pos_x * 16, block_pos_y * 16))
        self.accel_const = 0.58

        self.set_room_pos()

        self.set_images('sprites/trinkets/button.png', 64, 64, 2, 2)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def get_state(self) -> bool:
        """Checks if the button is being pressed by a box. Returns true if yes and false if no.

        Returns:
            bool: If button is activated (true/false)
        """
        is_active = False
        for box in groups.all_movable:
            if not self.hitbox.colliderect(box.hitbox):
                return is_active
            else:
                is_active = True
                return is_active

    def movement(self):
        if self.can_update and self.visible:
            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def update(self):
        if self.get_state():
            self.index = 1
        elif not self.get_state():
            self.index = 0
        self.render_images()

    def __repr__(self):
        return f'Button({self.id_value}, {self.pos}, {self.get_state()})'


class LockedWall(tiles.Wall):
    """A locked wall that can be opened by triggering it via a switch with an identical ID value."""
    def __init__(self, start_pos_x, start_pos_y, end_pos_x, end_pos_y, id_value: int,
                 block_width: int, block_height: int):
        super().__init__(start_pos_x, start_pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.show(self.layer)
        groups.all_walls.add(self)
        groups.all_trinkets.add(self)
        self.id_value = id_value

        self.activator = self._get_activator()
        self.last_state = self.activator.get_state()

        self.start_pos = vec((start_pos_x, start_pos_y))
        self.end_pos = vec((end_pos_x, end_pos_y))

        self.start_room_pos = vec((0, 0))
        self.end_room_pos = vec((0, 0))

        self._is_moving = False

    def _get_activator(self):
        """Finds the switch/trigger/activator sprite with the same ID value.

        Returns:
            The trinket that activates the locked wall
        """
        try:
            activator = next(s for s in groups.all_trinkets if s.id_value == self.id_value)
            return activator
        except StopIteration:
            raise IndexError

    def _set_room_points(self):
        room = cb.get_room()
        self.start_room_pos = vec((self.start_pos.x + room.pos.x, self.start_pos.y + room.pos.y))
        self.end_room_pos = vec((self.end_pos.x + room.pos.x, self.end_pos.y + room.pos.y))

    def movement(self):
        if self.can_update:
            self.set_room_pos()
            self._set_room_points()

            # Controls movement of wall when activator is activated/deactivated
            if self.last_state is not self.activator.get_state():
                if self.activator.get_state():
                    self.pos = self.end_room_pos
                else:
                    self.pos = self.start_room_pos
                self.last_state = self.activator.get_state()

            self.accel = self.get_accel()
            self.accel_movement()

    def update(self):
        display_text.draw_text(str(self), 0, 64)

    def __repr__(self):
        return f'LockedWall({self.id_value}, {self.pos}, {self.start_room_pos})'

    def __str__(self):
        return (f'ID value: {self.id_value}, pos: {self.pos}, Start pos: {self.start_room_pos}, '
                f'End pos: {self.end_room_pos}')
