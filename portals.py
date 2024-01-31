import pygame

import classbases as cb
import constants as cst

import groups

# Aliases
vec = pygame.math.Vector2


class Portal(cb.ActorBase):  # TODO: Update docstring
    def __init__(self, spawned_from, pos_x: int | float, pos_y: int | float, facing: str = cst.SOUTH):
        """A portal that can teleport any moving object

        ### Arguments
            - posX (``int``): The x-position where the portal should spawn
            - posY (``int``): The y-position where the portal should spawn
            - facing (``str``, optional): The direction the portal should face. Defaults to ``cst.SOUTH``.
        """        
        super().__init__()
        self.layer = cst.LAYER['portal']
        self.show(self.layer)
        groups.all_portals.add(self)

        room = cb.get_room()
        room.add(self)

        self.pos = vec((pos_x, pos_y))
        self.facing = facing

        self.landedOn = spawned_from.hit
        self.posOffset = vec(self.pos.x - self.landedOn.pos.x, self.pos.y - self.landedOn.pos.y)

        self.set_images("sprites/portals/portals.png", 64, 64, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        self._get_face()

        if self.facing is None:
            raise ValueError(f'ERROR: {self.facing} is not a valid facing direction')

    def _get_face(self) -> None:
        direction_angles = {cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270}
        self.rotate_image(direction_angles[self.facing])
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
        self.pos = self.landedOn.pos + self.posOffset
        self.center_rects()

    def update(self):
        pass

    def __repr__(self):
        return f'Portal({self.landedOn}, {self.facing}, {self.pos})'


def get_other_portal(portal_in):
    """Returns the other portal present in the all_portals list.

    Args:
        portal_in: The portal that is known

    Returns:
        Portal: The other portal in the all_portals list
    """
    for portal in groups.all_portals:
        if portal != portal_in:
            return portal


def portal_count_check():
    """If more than two portals are present during gameplay, the oldest one will be deleted to make another one.
    """
    if len(groups.all_portals) > 2:
        portal_temp = groups.all_portals.sprites()
        if len(portal_temp) > 0:
            oldest_portal = portal_temp[0]
            oldest_portal.kill()
            groups.all_portals.remove(oldest_portal)
            if len(portal_temp) > 1:
                groups.all_portals.add(portal_temp[1:])
