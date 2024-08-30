"""
Module containing the room class.
"""
import copy
import math
import time

import itertools
import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import screen

import calc
import classbases as cb
import constants as cst
import enemies
import groups
import players
import roomcontainers
import tiles
import trinkets
import visual_elems


class RoomTransition(cb.ActorBase):
    def __init__(self, owner):
        """The screen that fades up during a room switch

        :param owner: The active room object
        """
        super().__init__(999)
        self.add_to_gamestate()
        self.owner = owner

        self.pos = vec(cst.WINWIDTH // 2, cst.WINHEIGHT + cst.WINHEIGHT // 2)
        self.active = False
        self.phase = 'enter'
        self.last_trans = time.time()

        self.image = pygame.Surface(vec(cst.WINWIDTH, cst.WINHEIGHT))
        self.image.fill((0, 0, 0))

        self.set_rects(self.pos.x, self.pos.y, cst.WINWIDTH, cst.WINHEIGHT, cst.WINWIDTH, cst.WINHEIGHT)

    def update(self):
        if self.active and self.phase == 'enter':
            weight = calc.get_time_diff(self.last_trans)
            if self.owner.last_dir_entered == cst.SOUTH:
                self.pos.x = cst.WINWIDTH // 2
                self.pos.y = calc.cerp(-cst.WINHEIGHT // 2, cst.WINHEIGHT // 2, weight)
                if self.pos.y >= cst.WINHEIGHT // 2:
                    self.owner.can_update = True
                    self.owner.player1.can_update = True
                    self.owner.layout_update()
                    self.phase = 'exit'
                    self.last_trans = time.time()

            elif self.owner.last_dir_entered == cst.EAST:
                self.pos.y = cst.WINHEIGHT // 2
                self.pos.x = calc.cerp(-cst.WINWIDTH // 2, cst.WINWIDTH // 2, weight)
                if self.pos.x >= cst.WINWIDTH // 2:
                    self.owner.can_update = True
                    self.owner.player1.can_update = True
                    self.owner.layout_update()
                    self.phase = 'exit'
                    self.last_trans = time.time()

            elif self.owner.last_dir_entered == cst.NORTH:
                self.pos.x = cst.WINWIDTH // 2
                self.pos.y = calc.cerp(cst.WINHEIGHT + cst.WINHEIGHT // 2, cst.WINHEIGHT // 2, weight)
                if self.pos.y <= cst.WINHEIGHT // 2:
                    self.owner.can_update = True
                    self.owner.player1.can_update = True
                    self.owner.layout_update()
                    self.phase = 'exit'
                    self.last_trans = time.time()

            elif self.owner.last_dir_entered == cst.WEST:
                self.pos.y = cst.WINHEIGHT // 2
                self.pos.x = calc.cerp(cst.WINWIDTH + cst.WINWIDTH // 2, cst.WINWIDTH // 2, weight)
                if self.pos.x <= cst.WINWIDTH // 2:
                    self.owner.can_update = True
                    self.owner.player1.can_update = True
                    self.owner.layout_update()
                    self.phase = 'exit'
                    self.last_trans = time.time()

        # ----- Exiting ----- #
        elif self.active and self.phase == 'exit':
            weight = calc.get_time_diff(self.last_trans)
            if self.owner.last_dir_entered == cst.SOUTH:
                self.pos.y = calc.cerp(cst.WINHEIGHT // 2, cst.WINHEIGHT + cst.WINHEIGHT // 2, weight)
                if self.pos.y >= cst.WINHEIGHT + cst.WINHEIGHT // 2:
                    self.active = False
                    self.phase = 'enter'

            elif self.owner.last_dir_entered == cst.EAST:
                self.pos.x = calc.cerp(cst.WINWIDTH // 2, cst.WINWIDTH + cst.WINWIDTH // 2, weight)
                if self.pos.x >= cst.WINWIDTH + cst.WINWIDTH // 2:
                    self.active = False
                    self.phase = 'enter'

            elif self.owner.last_dir_entered == cst.NORTH:
                self.pos.y = calc.cerp(cst.WINHEIGHT // 2, -cst.WINHEIGHT // 2, weight)
                if self.pos.y <= -cst.WINHEIGHT // 2:
                    self.active = False
                    self.phase = 'enter'

            elif self.owner.last_dir_entered == cst.WEST:
                self.pos.x = calc.cerp(cst.WINWIDTH // 2, -cst.WINWIDTH // 2, weight)
                if self.pos.x <= -cst.WINWIDTH // 2:
                    self.active = False
                    self.phase = 'enter'

        self.center_rects()


class RoomSpecs:
    """Contains all information regarding the details of a room."""
    def __init__(self, room_width, room_height, scroll_x, scroll_y):
        """Contains all information regarding the details of a room

        :param room_width: The width of the room (in pixels)
        :param room_height: The height of the room (in pixels)
        :param scroll_x: Can the room scroll along the x-axis? (True if yes)
        :param scroll_y: Can the room scroll along the y-axis? (True if yes)
        """
        self.width = room_width
        self.height = room_height
        self.scroll = vec(scroll_x, scroll_y)


# noinspection PyTypeChecker
class Room(cb.AbstractBase):
    def __init__(self, room_x: float, room_y: float):
        """The room where all the current action is taking place

        :param room_x: The room's x-axis location in the grid of the room layout
        :param room_y: The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        groups.all_rooms.append(self)
        self.room = vec((room_x, room_y))
        self.size = vec((0, 0))
        self.last_dir_entered = None

        self.player1 = players.Player()

        self.last_mvm_rel = {  # Last movement key release
            cst.SOUTH: ctrl.key_released[ctrl.K_MOVE_DOWN],
            cst.EAST: ctrl.key_released[ctrl.K_MOVE_RIGHT],
            cst.NORTH: ctrl.key_released[ctrl.K_MOVE_UP],
            cst.WEST: ctrl.key_released[ctrl.K_MOVE_LEFT]
        }
        self.binds = {cst.SOUTH: ctrl.K_MOVE_DOWN,
                      cst.EAST: ctrl.K_MOVE_RIGHT,
                      cst.NORTH: ctrl.K_MOVE_UP,
                      cst.WEST: ctrl.K_MOVE_LEFT}

        self.last_tp_dirs = (cst.SOUTH, cst.SOUTH)

        self.border_south = tiles.RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.border_east = tiles.RoomBorder(cst.WINWIDTH // 16, 0, 1, self.size.y // 16)
        self.border_north = tiles.RoomBorder(0, -1, self.size.x // 16, 1)
        self.border_west = tiles.RoomBorder(-1, 0, 1, self.size.y // 16)
        self.add(self.border_south, self.border_east, self.border_north, self.border_west)

        self.is_scrolling_x = True
        self.is_scrolling_y = True

        self.trans_screen = RoomTransition(self)

        self.pos = vec(0, 0)
        self.pos_offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.accel_const = self.player1.accel_const

        self._room_specs = {
            (0, 0): RoomSpecs(1280, 720, True, True),
            (0, 1): RoomSpecs(640, 360, True, True),
            (0, 2): RoomSpecs(1280, 720, False, True),

            (1, 0): RoomSpecs(1280*2, 720, True, False),
            (2, 0): RoomSpecs(1280*2, 720, True, False),
        }

        self.layout_update()

    def _update_binds(self, dir_in, dir_out) -> None:
        """Updates the movement binds of the room to smooth movement between portals

        :param dir_in: The direction of the entrance portal
        :param dir_out: The direction of the exit portal
        :return: None
        """
        new_binds = {cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT,
                     cst.NORTH: ctrl.K_MOVE_UP, cst.WEST: ctrl.K_MOVE_LEFT}

        if dir_in == cst.SOUTH:
            if dir_out == cst.SOUTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_UP, cst.EAST: ctrl.K_MOVE_LEFT,
                                  cst.NORTH: ctrl.K_MOVE_DOWN, cst.WEST: ctrl.K_MOVE_RIGHT})
            if dir_out == cst.EAST:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_RIGHT, cst.EAST: ctrl.K_MOVE_UP,
                                  cst.NORTH: ctrl.K_MOVE_LEFT, cst.WEST: ctrl.K_MOVE_DOWN})
            if dir_out == cst.WEST:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_LEFT, cst.EAST: ctrl.K_MOVE_DOWN,
                                  cst.NORTH: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_UP})
        elif dir_in == cst.EAST:
            if dir_out == cst.SOUTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_LEFT, cst.EAST: ctrl.K_MOVE_DOWN,
                                  cst.NORTH: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_UP})
            if dir_out == cst.EAST:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_UP, cst.EAST: ctrl.K_MOVE_LEFT,
                                  cst.NORTH: ctrl.K_MOVE_DOWN, cst.WEST: ctrl.K_MOVE_RIGHT})
            if dir_out == cst.NORTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_RIGHT, cst.EAST: ctrl.K_MOVE_UP,
                                  cst.NORTH: ctrl.K_MOVE_LEFT, cst.WEST: ctrl.K_MOVE_DOWN})
        elif dir_in == cst.NORTH:
            if dir_out == cst.EAST:  # Same as (dir_in == cst.SOUTH and dir_out == cst.WEST)
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_LEFT, cst.EAST: ctrl.K_MOVE_DOWN,
                                  cst.NORTH: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_UP})
            if dir_out == cst.NORTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_UP, cst.EAST: ctrl.K_MOVE_LEFT,
                                  cst.NORTH: ctrl.K_MOVE_DOWN, cst.WEST: ctrl.K_MOVE_RIGHT})
            if dir_out == cst.WEST:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_RIGHT, cst.EAST: ctrl.K_MOVE_UP,
                                  cst.NORTH: ctrl.K_MOVE_LEFT, cst.WEST: ctrl.K_MOVE_DOWN})
        elif dir_in == cst.WEST:
            if dir_out == cst.SOUTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_RIGHT, cst.EAST: ctrl.K_MOVE_UP,
                                  cst.NORTH: ctrl.K_MOVE_LEFT, cst.WEST: ctrl.K_MOVE_DOWN})
            if dir_out == cst.NORTH:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_LEFT, cst.EAST: ctrl.K_MOVE_DOWN,
                                  cst.NORTH: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_UP})
            if dir_out == cst.WEST:
                new_binds.update({cst.SOUTH: ctrl.K_MOVE_UP, cst.EAST: ctrl.K_MOVE_LEFT,
                                  cst.NORTH: ctrl.K_MOVE_DOWN, cst.WEST: ctrl.K_MOVE_RIGHT})
        self.binds = new_binds

    def _readjust_binds_after_tp(self, dir_in: str, dir_out: str) -> None:
        """Readjusts the movement binds set when teleporting to account for keys that were not held.
        The binds for the keys not held will be reset to their defaults.

        :param dir_in: The direction the entrance portal is facing
        :param dir_out: The direction the exit portal is facing
        :return: None
        """
        if dir_in == dir_out or dir_in == calc.get_opposite(dir_out):
            if not ctrl.is_input_held[ctrl.K_MOVE_UP] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
                self.binds[cst.NORTH] = ctrl.K_MOVE_UP
                self.binds[cst.SOUTH] = ctrl.K_MOVE_DOWN
            if not ctrl.is_input_held[ctrl.K_MOVE_LEFT] and not ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
                self.binds[cst.EAST] = ctrl.K_MOVE_RIGHT
                self.binds[cst.WEST] = ctrl.K_MOVE_LEFT

        # ----- Entrance South ----- #
        if dir_in == cst.SOUTH and dir_out == cst.WEST:
            if not ctrl.is_input_held[ctrl.K_MOVE_UP]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and not ctrl.is_input_held[ctrl.K_MOVE_UP]:
                self.binds[cst.EAST] = ctrl.K_MOVE_LEFT
                self.binds[cst.WEST] = ctrl.K_MOVE_RIGHT

        if dir_in == cst.SOUTH and dir_out == cst.EAST:
            if not ctrl.is_input_held[ctrl.K_MOVE_UP]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_LEFT] and not ctrl.is_input_held[ctrl.K_MOVE_UP]:
                self.binds[cst.EAST] = ctrl.K_MOVE_LEFT
                self.binds[cst.WEST] = ctrl.K_MOVE_RIGHT

        # ----- Entrance North ----- #
        if dir_in == cst.NORTH and dir_out == cst.WEST:
            if not ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
                self.binds[cst.EAST] = ctrl.K_MOVE_LEFT
                self.binds[cst.WEST] = ctrl.K_MOVE_RIGHT

        if dir_in == cst.NORTH and dir_out == cst.EAST:
            if not ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_LEFT] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
                self.binds[cst.EAST] = ctrl.K_MOVE_LEFT
                self.binds[cst.WEST] = ctrl.K_MOVE_RIGHT

        # ----- Entrance West ------ #
        if dir_in == cst.WEST and dir_out == cst.SOUTH:
            if not ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_UP] and not ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
                self.binds[cst.SOUTH] = ctrl.K_MOVE_UP
                self.binds[cst.NORTH] = ctrl.K_MOVE_DOWN

        if dir_in == cst.WEST and dir_out == cst.NORTH:
            if not ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_DOWN] and not ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
                self.binds[cst.SOUTH] = ctrl.K_MOVE_UP
                self.binds[cst.NORTH] = ctrl.K_MOVE_DOWN

        # ----- Entrance East ----- #
        if dir_in == cst.EAST and dir_out == cst.SOUTH:
            if not ctrl.is_input_held[ctrl.K_MOVE_LEFT]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_UP] and not ctrl.is_input_held[ctrl.K_MOVE_LEFT]:
                self.binds[cst.SOUTH] = ctrl.K_MOVE_UP
                self.binds[cst.NORTH] = ctrl.K_MOVE_DOWN

        if dir_in == cst.EAST and dir_out == cst.NORTH:
            if not ctrl.is_input_held[ctrl.K_MOVE_LEFT]:
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
            if ctrl.is_input_held[ctrl.K_MOVE_DOWN] and not ctrl.is_input_held[ctrl.K_MOVE_LEFT]:
                self.binds[cst.SOUTH] = ctrl.K_MOVE_UP
                self.binds[cst.NORTH] = ctrl.K_MOVE_DOWN

    def _hard_reset_binds(self) -> None:
        """Completely resets the key binds after teleporting

        :return: None
        """
        if (self.last_tp_dirs[0] == self.last_tp_dirs[1]
                or self.last_tp_dirs[0] == calc.get_opposite(self.last_tp_dirs[1])):
            if self.last_mvm_rel[cst.NORTH] != ctrl.key_released[ctrl.K_MOVE_UP]:
                self.binds.update({cst.NORTH: ctrl.K_MOVE_UP, cst.SOUTH: ctrl.K_MOVE_DOWN})
                self.last_mvm_rel[cst.NORTH] = ctrl.key_released[ctrl.K_MOVE_UP]

            if self.last_mvm_rel[cst.SOUTH] != ctrl.key_released[ctrl.K_MOVE_DOWN]:
                self.binds.update({cst.NORTH: ctrl.K_MOVE_UP, cst.SOUTH: ctrl.K_MOVE_DOWN})
                self.last_mvm_rel[cst.SOUTH] = ctrl.key_released[ctrl.K_MOVE_DOWN]

            if self.last_mvm_rel[cst.WEST] != ctrl.key_released[ctrl.K_MOVE_LEFT]:
                self.binds.update({cst.EAST: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_LEFT})
                self.last_mvm_rel[cst.WEST] = ctrl.key_released[ctrl.K_MOVE_LEFT]

            if self.last_mvm_rel[cst.EAST] != ctrl.key_released[ctrl.K_MOVE_RIGHT]:
                self.binds.update({cst.EAST: ctrl.K_MOVE_RIGHT, cst.WEST: ctrl.K_MOVE_LEFT})
                self.last_mvm_rel[cst.EAST] = ctrl.key_released[ctrl.K_MOVE_RIGHT]

        # ----- Entrance South ----- #
        if self.last_tp_dirs[0] == cst.SOUTH and self.last_tp_dirs[1] == cst.WEST:
            # If up is released, as long as right key isn't held
            if ((not ctrl.is_input_held[ctrl.K_MOVE_UP] and not ctrl.is_input_held[ctrl.K_MOVE_RIGHT])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_UP] and ctrl.is_input_held[ctrl.K_MOVE_RIGHT])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        if self.last_tp_dirs[0] == cst.SOUTH and self.last_tp_dirs[1] == cst.EAST:
            # If up is released, as long as left key isn't held
            if ((not ctrl.is_input_held[ctrl.K_MOVE_UP] and not ctrl.is_input_held[ctrl.K_MOVE_LEFT])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_UP] and ctrl.is_input_held[ctrl.K_MOVE_LEFT])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        # ----- Entrance North ----- #
        if self.last_tp_dirs[0] == cst.NORTH and self.last_tp_dirs[1] == cst.WEST:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_DOWN] and not ctrl.is_input_held[ctrl.K_MOVE_RIGHT])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_DOWN] and ctrl.is_input_held[ctrl.K_MOVE_RIGHT])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        if self.last_tp_dirs[0] == cst.NORTH and self.last_tp_dirs[1] == cst.EAST:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_DOWN] and not ctrl.is_input_held[ctrl.K_MOVE_LEFT])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_DOWN] and ctrl.is_input_held[ctrl.K_MOVE_LEFT])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        # ----- Entrance West ----- #
        if self.last_tp_dirs[0] == cst.WEST and self.last_tp_dirs[1] == cst.SOUTH:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and not ctrl.is_input_held[ctrl.K_MOVE_UP])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and ctrl.is_input_held[ctrl.K_MOVE_UP])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        if self.last_tp_dirs[0] == cst.WEST and self.last_tp_dirs[1] == cst.NORTH:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_RIGHT] and ctrl.is_input_held[ctrl.K_MOVE_DOWN])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

        # ----- Entrance East ----- #
        if self.last_tp_dirs[0] == cst.EAST and self.last_tp_dirs[1] == cst.SOUTH:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_LEFT] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_LEFT] and ctrl.is_input_held[ctrl.K_MOVE_UP])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})
        #
        if self.last_tp_dirs[0] == cst.EAST and self.last_tp_dirs[1] == cst.NORTH:
            if ((not ctrl.is_input_held[ctrl.K_MOVE_LEFT] and not ctrl.is_input_held[ctrl.K_MOVE_DOWN])
                    or (not ctrl.is_input_held[ctrl.K_MOVE_LEFT] and ctrl.is_input_held[ctrl.K_MOVE_UP])):
                self.binds.update({cst.WEST: ctrl.K_MOVE_LEFT, cst.NORTH: ctrl.K_MOVE_UP,
                                   cst.SOUTH: ctrl.K_MOVE_DOWN, cst.EAST: ctrl.K_MOVE_RIGHT})

    def accel_movement(self) -> None:
        """Calculates the room's acceleration, velocity, and position
        """
        self.accel.x += self.vel.x * cst.FRIC
        self.accel.y += self.vel.y * cst.FRIC
        self.vel += self.accel * (screen.dt * cst.M_FPS)

        self.pos = vec(self.border_west.pos.x + self.border_west.hitbox.width // 2,
                       self.border_north.pos.y + self.border_north.height // 2) - self.pos_offset

    def get_accel(self) -> vec:
        """Returns the acceleration value to give to the room

        Returns:
            pygame.math.Vector2: The acceleration value the room should have
        """
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

        if ctrl.is_input_held[self.binds[cst.WEST]]:
            output += self.player1.accel_const
        if ctrl.is_input_held[self.binds[cst.EAST]]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle(self.player1.pos, self.player1.grapple.pos)
            output += self.player1.grapple_speed * math.sin(math.radians(angle))

        return output

    def _get_y_axis_output(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have

        Returns:
            float: The room's acceleration's y-axis component
        """
        output = 0.0

        if ctrl.is_input_held[self.binds[cst.NORTH]]:
            output += self.player1.accel_const

        if ctrl.is_input_held[self.binds[cst.SOUTH]]:
            output -= self.player1.accel_const

        if self.player1.is_swinging():
            angle = calc.get_angle(self.player1.pos, self.player1.grapple.pos)
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

            for proj in groups.all_projs:
                proj.movement()

    def _set_vel(self, value_x: int | float, value_y: int | float, is_additive: bool = False) -> None:
        """Sets the velocity components of the room, as well as all the sprites within the room, to specified values

        :param value_x: X-axis component
        :param value_y: Y-axis component
        :param is_additive: Should the values be added to the current vel or override it? Defaults to False
        :return: None
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

    def _get_sprites_to_recenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is centered.

        Returns:
            list: A list containing all sprites that should be relocated when the player is centered
        """
        output_list = []
        for sprite in [s
                       for s in itertools.chain(self.sprites(), groups.all_drops)
                       if s.in_gamestate]:
            output_list.append(sprite)

        for container in [c for c in groups.all_containers if c.room == self.room]:
            for sprite in container:
                output_list.append(sprite)

        return output_list

    # -------------------------------- Teleporting ------------------------------- #
    def _align_player_tp(self, portal_out, width, height) -> None:
        """Sets the player at the proper position after teleporting when the room can scroll.

        :param portal_out: The exit portal sprite
        :param width: Half the sum of the player's hitbox width plus the portal's hitbox width
        :param height: Half the sum of the player's hitbox height plus the portal's hitbox height
        :return: None
        """
        if portal_out.facing == cst.SOUTH:
            self.player1.pos.x = portal_out.pos.x
            self.player1.pos.y = portal_out.pos.y + height

        elif portal_out.facing == cst.EAST:
            self.player1.pos.x = portal_out.pos.x + width
            self.player1.pos.y = portal_out.pos.y

        elif portal_out.facing == cst.NORTH:
            self.player1.pos.x = portal_out.pos.x
            self.player1.pos.y = portal_out.pos.y - height

        elif portal_out.facing == cst.WEST:
            self.player1.pos.x = portal_out.pos.x - width
            self.player1.pos.y = portal_out.pos.y

    def _teleport_player(self, portal_in, portal_out) -> None:
        """Teleports the player when the room is scrolling.

        :param portal_in: The portal the player is entering
        :param portal_out: The portal the player is exiting
        :return: None
        """
        dir_in = portal_in.facing
        dir_out = portal_out.facing
        self.last_tp_dirs = (dir_in, dir_out)
        dir_angles = {cst.SOUTH: 180, cst.EAST: 90, cst.NORTH: 0, cst.WEST: 270}

        # Actually teleporting the player
        self._align_player_tp(portal_out,
                              (portal_out.hitbox.width + self.player1.hitbox.width) // 2,
                              (portal_out.hitbox.height + self.player1.hitbox.height) // 2)
        self._update_binds(dir_in, dir_out)
        self._readjust_binds_after_tp(dir_in, dir_out)  # If the key wasn't held while tp-ing, don't reverse binding

        if self.is_scrolling_x and self.is_scrolling_y:
            if dir_in == cst.EAST:
                dir_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif dir_in == cst.NORTH:
                dir_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif dir_in == cst.WEST:
                dir_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self._sprites_rotate_trajectory(dir_angles[dir_out])

        elif self.is_scrolling_x and not self.is_scrolling_y:
            if dir_in == cst.SOUTH:
                dir_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if dir_out == dir_in:
                    self.player1.vel = self.player1.vel.rotate(dir_angles[dir_out])
                if dir_out in [cst.EAST, cst.WEST]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.EAST:
                dir_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if dir_out == dir_in:
                    self._sprites_rotate_trajectory(dir_angles[dir_out])
                if dir_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.NORTH:
                dir_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if dir_out == dir_in:
                    self.player1.vel = self.player1.vel.rotate(dir_angles[dir_out])
                if dir_out in [cst.EAST, cst.WEST]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.WEST:
                dir_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if dir_out == dir_in:
                    self._sprites_rotate_trajectory(dir_angles[dir_out])
                if dir_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_vel(dir_angles[dir_out])

        elif not self.is_scrolling_x and self.is_scrolling_y:
            if dir_in == cst.SOUTH:
                dir_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if dir_out == dir_in:
                    self._sprites_rotate_trajectory(dir_angles[dir_out])
                if dir_out in [cst.EAST, cst.WEST]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.EAST:
                dir_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if dir_out == dir_in:
                    self.player1.vel = self.player1.vel.rotate(dir_angles[dir_out])
                if dir_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.NORTH:
                dir_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if dir_out == dir_in:
                    self._sprites_rotate_trajectory(dir_angles[dir_out])
                if dir_out in [cst.EAST, cst.WEST]:
                    self._translate_vel(dir_angles[dir_out])

            if dir_in == cst.WEST:
                dir_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if dir_out == dir_in:
                    self.player1.vel = self.player1.vel.rotate(dir_angles[dir_out])
                if dir_out in [cst.SOUTH, cst.NORTH]:
                    self._translate_vel(dir_angles[dir_out])

        elif not self.is_scrolling_x and not self.is_scrolling_y:
            if dir_in == cst.EAST:
                dir_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif dir_in == cst.NORTH:
                dir_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif dir_in == cst.WEST:
                dir_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self.player1.vel = self.player1.vel.rotate(dir_angles[dir_out])

    def _sprites_rotate_trajectory(self, angle: float) -> None:
        """Rotates the velocities and accelerations of all the sprites within the room's sprites

        :param angle: The angle to rotate the vectors by
        :return: None
        """
        self.vel = self.vel.rotate(angle)

        for sprite in self._get_sprites_to_recenter():
            sprite.vel = sprite.vel.rotate(angle)

    def _translate_vel(self, angle: float) -> None:
        """Sets the room's velocity equal to the player's rotated velocity and vice versa

        :param angle: The angle to rotate the velocities by
        :return: None
        """
        room_vel_copy = self.vel.copy()
        player_vel_copy = self.player1.vel.copy()
        for sprite in self._get_sprites_to_recenter():
            sprite.vel = player_vel_copy.rotate(angle)
        self.player1.vel = room_vel_copy.rotate(angle)

    def _sprite_collide_check(self, instig, *contact_list) -> None:
        """Collide check for when the room is scrolling

        :param instig: The sprite instigating the collision
        :param contact_list: The sprite group(s) to check for a collision with
        :return: None
        """
        if instig == self.player1:
            for sprite in [s
                           for group in contact_list
                           for s in group
                           if s.in_gamestate]:
                self._player_block_from_side(sprite)
        else:
            for sprite in [s
                           for group in contact_list
                           for s in group
                           if s.in_gamestate]:
                self._sprite_block_from_side(instig, sprite)

    def _player_block_from_side(self, sprite) -> None:
        width = (self.player1.hitbox.width + sprite.hitbox.width) // 2
        height = (self.player1.hitbox.height + sprite.hitbox.height) // 2
        if calc.triangle_collide(self.player1, sprite) == cst.SOUTH and (
                self.player1.vel.y < 0 or sprite.vel.y > 0) and self.player1.pos.y <= sprite.pos.y + height:
            self.player1.vel.y = 0
            self.player1.pos.y = sprite.pos.y + height

        elif calc.triangle_collide(self.player1, sprite) == cst.EAST and (
                self.player1.vel.x < 0 or sprite.vel.x > 0) and self.player1.pos.x <= sprite.pos.x + width:
            self.player1.vel.x = 0
            self.player1.pos.x = sprite.pos.x + width

        elif calc.triangle_collide(self.player1, sprite) == cst.NORTH and (
                self.player1.vel.y > 0 or sprite.vel.y < 0) and self.player1.pos.y >= sprite.pos.y - height:
            self.player1.vel.y = 0
            self.player1.pos.y = sprite.pos.y - height

        elif calc.triangle_collide(self.player1, sprite) == cst.WEST and (
                self.player1.vel.x > 0 or sprite.vel.x < 0) and self.player1.pos.x >= sprite.pos.x - width:
            self.player1.vel.x = 0
            self.player1.pos.x = sprite.pos.x - width

    @staticmethod
    def _sprite_block_from_side(instig, sprite) -> None:
        width = (instig.hitbox.width + sprite.hitbox.width) // 2
        height = (instig.hitbox.height + sprite.hitbox.height) // 2
        if (calc.triangle_collide(instig, sprite) == cst.SOUTH and
                instig.pos.y <= sprite.pos.y + height and (
                instig.vel.y < 0 or sprite.vel.y > 0)):
            instig.vel.y = 0
            instig.pos.y = sprite.pos.y + height

        elif (calc.triangle_collide(instig, sprite) == cst.EAST and
                instig.pos.x <= sprite.pos.x + width and (
                instig.vel.x < 0 or sprite.vel.x > 0)):
            instig.vel.x = 0
            instig.pos.x = sprite.pos.x + width

        elif (calc.triangle_collide(instig, sprite) == cst.NORTH and
                instig.pos.y >= sprite.pos.y - height and (
                instig.vel.y > 0 or sprite.vel.y < 0)):
            instig.vel.y = 0
            instig.pos.y = sprite.pos.y - height

        elif (calc.triangle_collide(instig, sprite) == cst.WEST and
                instig.pos.x >= sprite.pos.x - width and (
                instig.vel.x > 0 or sprite.vel.x < 0)):
            instig.vel.x = 0
            instig.pos.x = sprite.pos.x - width

    # -------------------------------- Room Layout ------------------------------- #
    def _change_room(self) -> None:
        if not self.trans_screen.active:
            width = self.player1.hitbox.width // 2
            height = self.player1.hitbox.height // 2

            if self.player1.pos.y >= self.border_south.pos.y - height:
                self.can_update = False
                self.player1.can_update = False
                self.room.y -= 1
                self.last_dir_entered = cst.SOUTH
                self.trans_screen.active = True
                self.trans_screen.last_trans = time.time()
                calc.kill_groups(groups.all_projs)

            elif self.player1.pos.x >= self.border_east.pos.x - width:
                self.can_update = False
                self.player1.can_update = False
                self.room.x += 1
                self.last_dir_entered = cst.EAST
                self.trans_screen.active = True
                self.trans_screen.last_trans = time.time()
                calc.kill_groups(groups.all_projs)

            elif self.player1.pos.y <= self.border_north.pos.y + height:
                self.can_update = False
                self.player1.can_update = False
                self.room.y += 1
                self.last_dir_entered = cst.NORTH
                self.trans_screen.active = True
                self.trans_screen.last_trans = time.time()
                calc.kill_groups(groups.all_projs)

            elif self.player1.pos.x <= self.border_west.pos.x + width:
                self.can_update = False
                self.player1.can_update = False
                self.room.x -= 1
                self.last_dir_entered = cst.WEST
                self.trans_screen.active = True
                self.trans_screen.last_trans = time.time()
                calc.kill_groups(groups.all_projs)

    def _init_room(self, room_size_x: int, room_size_y: int, can_scroll_x: bool, can_scroll_y: bool) -> None:
        """Initializes a room's properties. This function must be called once for every room iteration.

        :param room_size_x: The width of the room (in pixels).
        :param room_size_y: The height of the room (in pixels).
        :param can_scroll_x: Should the room scroll with the player along the x-axis?
        :param can_scroll_y: Should the room scroll with the player along the y-axis?
        :return: None
        """
        # Placing borders in correct spots in room
        west_coords = vec(-8, room_size_y // 2)
        north_coords = vec(room_size_x // 2, -8)
        south_coords = vec(north_coords.x, north_coords.y + room_size_y + 16)
        east_coords = vec(west_coords.x + room_size_x + 16, room_size_y // 2)

        self.border_south = tiles.RoomBorder(south_coords.x, south_coords.y, room_size_x / 16, 1)
        self.border_east = tiles.RoomBorder(east_coords.x, east_coords.y, 1, room_size_y / 16)
        self.border_north = tiles.RoomBorder(north_coords.x, north_coords.y, room_size_x / 16, 1)
        self.border_west = tiles.RoomBorder(west_coords.x, west_coords.y, 1, room_size_y / 16)

        self.add(self.border_south, self.border_east, self.border_north, self.border_west)

        # Setting player at correct spot in room
        if self.last_dir_entered == cst.SOUTH:
            self.player1.pos.x = self.border_north.pos.x
            self.player1.pos.y = (self.border_north.pos.y + self.border_north.hitbox.height // 2
                                  + self.player1.hitbox.height // 2)

        elif self.last_dir_entered == cst.EAST:
            self.player1.pos.x = (self.border_west.pos.x
                                  + self.border_west.hitbox.width // 2 + self.player1.hitbox.width // 2)
            self.player1.pos.y = self.border_west.pos.y

        elif self.last_dir_entered == cst.NORTH:
            self.player1.pos.x = self.border_south.pos.x
            self.player1.pos.y = (self.border_south.pos.y
                                  - self.border_south.hitbox.height // 2 - self.player1.hitbox.height // 2)

        elif self.last_dir_entered == cst.WEST:
            self.player1.pos.x = (self.border_east.pos.x
                                  - self.border_east.hitbox.width // 2 - self.player1.hitbox.width // 2)
            self.player1.pos.y = self.border_east.pos.y

        player_vel_copy = self.player1.vel.copy()
        self.size = vec((room_size_x, room_size_y))

        scroll_copy_x = copy.copy(self.is_scrolling_x)
        scroll_copy_y = copy.copy(self.is_scrolling_y)
        self.is_scrolling_x = can_scroll_x
        self.is_scrolling_y = can_scroll_y

        # self._get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.is_scrolling_x, self.is_scrolling_y,
        #                                  player_vel_copy, room_vel_copy)
        self.vel = vec(0, 0)

    def _get_room_change_trajectory(self, prev_room_scroll_x: bool, prev_room_scroll_y: bool, new_room_scroll_x: bool,
                                    new_room_scroll_y: bool, player_vel: vec, room_vel: vec) -> None:
        """Transfers the velocity from the room to the player or vice versa when changing rooms

        :param prev_room_scroll_x: Did the previous room scroll along the x-axis?
        :param prev_room_scroll_y: Did the previous room scroll along the y-axis?
        :param new_room_scroll_x: Does the new room scroll along the x-axis?
        :param new_room_scroll_y: Does the new room scroll along the y-axis?
        :param player_vel: The player's velocity
        :return: None
        """
        if prev_room_scroll_x:
            if not new_room_scroll_x:
                self.player1.vel.x = -room_vel.x
        elif not prev_room_scroll_x:
            if new_room_scroll_x:
                self._set_vel(-player_vel.x, 0)

        if prev_room_scroll_y:
            if not new_room_scroll_y:
                self.player1.vel.y = -room_vel.y
        elif not prev_room_scroll_y:
            if new_room_scroll_y:
                self._set_vel(0, -player_vel.y)

    def layout_update(self) -> None:
        """Updates the layout of the room"""
        for sprite in self.sprites():
            sprite.kill()

        for portal in groups.all_portals:
            portal.kill()

        for container in groups.all_containers:
            container.deactivate_sprites()

        try:  # Searching for the room container. If container isn't found, one will be generated
            container = next(c for c in groups.all_containers if c.room == self.room)
            container.activate_sprites()
        except StopIteration:
            new_container = roomcontainers.RoomContainer(self.room.x, self.room.y, self._get_room_layout())
            groups.all_containers.append(new_container)

        this_room = self._room_specs[tuple(self.room)]  # Retrieve room specs
        self._init_room(this_room.width, this_room.height, this_room.scroll.x, this_room.scroll.y)

        # ----- Centering the room when the room is smaller than the window size ----- #
        if self.border_east.pos.x - 16 < cst.WINWIDTH:
            self.pos_offset.x = cst.WINWIDTH // 2 - self.border_north.hitbox.width // 2
            self.border_north.pos.x = cst.WINWIDTH // 2
            self.border_south.pos.x = cst.WINWIDTH // 2
            self.border_east.pos.x = cst.WINWIDTH // 2 + self.border_north.hitbox.width // 2 + 8
            self.border_west.pos.x = cst.WINWIDTH // 2 - self.border_north.hitbox.width // 2 - 8
            self.player1.pos.x += self.pos_offset.x
        else:
            self.pos_offset.x = 0

        if self.border_south.pos.y - 16 < cst.WINHEIGHT:
            self.pos_offset.y = cst.WINHEIGHT // 2 - self.border_east.hitbox.height // 2
            self.border_east.pos.y = cst.WINHEIGHT // 2
            self.border_west.pos.y = cst.WINHEIGHT // 2
            self.border_south.pos.y = cst.WINHEIGHT // 2 + self.border_east.hitbox.height // 2 + 8
            self.border_north.pos.y = cst.WINHEIGHT // 2 - self.border_east.hitbox.height // 2 - 8
            self.player1.pos.y += cst.WINHEIGHT // 2 - self.border_east.hitbox.height // 2
        else:
            self.pos_offset.y = 0

    def _get_room_layout(self) -> list:
        """Returns the layout of the current room.

        Returns:
            list: A list of all the sprites that should be in the room. This includes walls, floors, enemies, and
            puzzle mechanisms.
        """
        if self.room == vec(0, 0):
            return [
                tiles.Wall(0, 0, 4, 41),
                enemies.Turret(300, 300),
                # tiles.CustomWall(cst.WINWIDTH // 2, cst.WINHEIGHT // 2,
                #                  'xx\nxo', 64)
                trinkets.Box(300, 300)
            ]

        elif self.room == vec(0, 1):
            return [
                tiles.Wall(320, 180, 16, 4),
                tiles.Wall(320, 180, 4, 8),
                # trinkets.Box(cst.WINWIDTH // 2, cst.WINHEIGHT // 2),
                # enemies.Ambusher(cst.WINWIDTH // 2, cst.WINHEIGHT // 2)
            ]

        elif self.room == vec(0, 2):
            return [
                tiles.Wall(600, 400, 16, 4),
            ]

        elif self.room == vec(1, 0):
            return [

            ]

        else:
            raise RuntimeError(f'No room layout associated with room {self.room}.')

    @cb.check_update_state
    def update(self):
        self._hard_reset_binds()
        self._change_room()
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'
