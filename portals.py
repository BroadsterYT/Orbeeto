import time
import os

from pygame.math import Vector2 as vec

import calc
import classbases as cb
import constants as cst
import groups


class Portal(cb.ActorBase):
    def __init__(self, spawned_from, pos_x: int | float, pos_y: int | float, facing: str = cst.SOUTH):
        """A portal that can teleport objects

        :param spawned_from: The bullet the portal is spawning from
        :param pos_x: The x-position where the portal should spawn
        :param pos_y: The y-position where the portal should spawn
        :param facing: The direction the portal should face. Default is cst.SOUTH.
        """
        super().__init__(cst.LAYER['portal'])
        self.add_to_gamestate()
        groups.all_portals.add(self)

        room = cb.get_room()
        match_container = [c for c in groups.all_containers if c.room == room.room][0]
        match_container.add(self)

        self.pos = vec((pos_x, pos_y))
        self.facing = facing

        self.landedOn = spawned_from.hit
        self.pos_offset = vec(self.pos.x - self.landedOn.pos.x, self.pos.y - self.landedOn.pos.y)

        self.direction_angles = {cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270}

        self.set_images(os.path.join(os.getcwd(), 'sprites/portals/portals.png'), 64, 64, 8, 16)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        self._get_face()

    def _get_face(self) -> None:
        self.rotate_image(self.direction_angles[self.facing])
        if self.facing == cst.SOUTH:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        if self.facing == cst.EAST:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 20, 54)

        if self.facing == cst.NORTH:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        if self.facing == cst.WEST:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 20, 54)

    def movement(self):
        # Setting position to offset of where bullet landed
        self.pos = self.landedOn.pos + self.pos_offset
        self.center_rects()

    def update(self):
        self._animate()
        self.rotate_image(self.direction_angles[self.facing])

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 0.1:
            self.index += 1
            if self.index > 15:
                self.index = 0

            self.last_frame = time.time()

    def __repr__(self):
        return f'Portal({self.pos}, {self.landedOn}, {self.facing})'


def portal_count_check():
    """If more than two portals are present during gameplay, the oldest one will be deleted to make another one."""
    if len(groups.all_portals) > 2:
        portal_temp = groups.all_portals.sprites()
        if len(portal_temp) > 0:
            oldest_portal = portal_temp[0]
            oldest_portal.kill()
            groups.all_portals.remove(oldest_portal)
            if len(portal_temp) > 1:
                groups.all_portals.add(portal_temp[1:])
