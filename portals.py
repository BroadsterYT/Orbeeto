from class_bases import *
from groups import *


class Portal(ActorBase):
    def __init__(self, spawned_from, pos_x: int, pos_y: int, facing: str = SOUTH):
        """A portal that can teleport any moving object

        ### Arguments
            - posX (``int``): The x-position where the portal should spawn
            - posY (``int``): The y-position where the portal should spawn
            - facing (``str``, optional): The direction the portal should face. Defaults to ``SOUTH``.
        """        
        super().__init__()
        self.show(LAYER['portal'])
        all_portals.add(self)
        room = get_room(); room.add(self)

        self.pos = vec((pos_x, pos_y))
        self.facing = facing

        self.landedOn = spawned_from.hit
        self.posOffset = vec(self.pos.x - self.landedOn.pos.x, self.pos.y - self.landedOn.pos.y)

        self.set_images("sprites/portals/portals.png", 64, 64, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        self.__get_face()

        if self.facing is None:
            raise ValueError(f'ERROR: {self.facing} is not a valid facing direction')

    def __get_face(self) -> None:
        direction_angles = {SOUTH: 0, EAST: 90, NORTH: 180, WEST: 270}
        self.rotate_image(direction_angles[self.facing])
        if self.facing == SOUTH:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        if self.facing == EAST:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 20, 54)

        if self.facing == NORTH:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 54, 20)

        if self.facing == WEST:
            self.set_rects(self.pos.x, self.pos.y, 64, 64, 20, 54)

    def movement(self):
        # Setting position to offset of where bullet landed
        self.pos = self.landedOn.pos + self.posOffset
        self.center_rects()

    def update(self):
        self.__get_face()

    def __repr__(self):
        return f'Portal({self.landedOn}, {self.facing}, {self.pos})'


def portal_count_check():
    """If more than two portals are present during gameplay, the oldest one will be deleted to make another one.
    """
    if len(all_portals) > 2:
        portal_temp = all_portals.sprites()
        if len(portal_temp) > 0:
            oldest_portal = portal_temp[0]
            oldest_portal.kill()
            all_portals.remove(oldest_portal)
            if len(portal_temp) > 1:
                all_portals.add(portal_temp[1:])
