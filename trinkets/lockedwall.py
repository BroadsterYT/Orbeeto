import time

from pygame.math import Vector2 as vec

import calc
import classbases as cb
import constants as cst
import groups
import tiles


class LockedWall(tiles.Wall):
    """A locked wall that can be opened by triggering it via a switch with an identical ID value."""
    def __init__(self, start_pos_x, start_pos_y, end_pos_x, end_pos_y, id_value: int,
                 block_width: int, block_height: int):
        super().__init__(start_pos_x, start_pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.add_to_gamestate()
        groups.all_trinkets.add(self)
        self.id_value = id_value

        self.activator = self._get_activator()
        self.last_state = False
        self.last_state_change = time.time()
        self.speed_mult = 4

        self.switch_diff = calc.get_time_diff(self.last_state_change)

        self.pos = self.place_top_left(start_pos_x, start_pos_y)
        self.start_pos = self.place_top_left(start_pos_x, start_pos_y)
        self.end_pos = self.place_top_left(end_pos_x, end_pos_y)

        self._set_room_points()

        self._is_moving = False

    def _get_activator(self):
        """Finds the switch/trigger/activator sprite with the same ID value.

        Returns:
            The trinket that activates the locked wall
        """
        try:
            activator = next(t for t in groups.all_trinkets if t.id_value == self.id_value)
            return activator
        except StopIteration:
            raise IndexError

    def _set_room_points(self):
        room = cb.get_room()
        self.start_room_pos = vec((self.start_pos.x + room.pos.x, self.start_pos.y + room.pos.y))
        self.end_room_pos = vec((self.end_pos.x + room.pos.x, self.end_pos.y + room.pos.y))

    def movement(self):
        if self.in_gamestate:
            self._set_room_points()
            self.set_room_pos()

            # Controls movement of wall when activator is activated/deactivated
            if self.activator.get_state():
                if not self._is_moving and self.activator.get_state() is not self.last_state:
                    self.last_state = self.activator.get_state()
                    self.last_state_change = time.time()
                    self._is_moving = True

                elif self._is_moving:
                    self.pos.x = calc.cerp(self.pos.x, self.end_room_pos.x, self.switch_diff / self.speed_mult)
                    self.pos.y = calc.cerp(self.pos.y, self.end_room_pos.y, self.switch_diff / self.speed_mult)
                    if self.switch_diff >= self.speed_mult:
                        self._is_moving = False

            else:
                if not self._is_moving and self.activator.get_state() is not self.last_state:
                    self.last_state = self.activator.get_state()
                    self.last_state_change = time.time()
                    self._is_moving = True

                elif self._is_moving:
                    self.pos.x = calc.cerp(self.pos.x, self.start_room_pos.x, self.switch_diff / self.speed_mult)
                    self.pos.y = calc.cerp(self.pos.y, self.start_room_pos.y, self.switch_diff / self.speed_mult)
                    if self.switch_diff >= self.speed_mult:
                        self._is_moving = False

            self.accel = self.get_accel()
            self.accel_movement()

    def update(self):
        self.switch_diff = calc.get_time_diff(self.last_state_change)

    def __repr__(self):
        return f'LockedWall({self.id_value}, {self.pos}, {self.start_room_pos})'

    def __str__(self):
        return (f'ID value: {self.id_value}, pos: {self.pos}, Start pos: {self.start_room_pos}, '
                f'End pos: {self.end_room_pos}')
    