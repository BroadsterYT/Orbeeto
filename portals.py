import pygame

from class_bases import *


class PortalBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.visible = True


class Portal(PortalBase):
    def __init__(self, posX: int, posY: int, facing: str = SOUTH):
        """A portal that can teleport any moving object

        ### Arguments
            - posX (``int``): The x-position where the portal should spawn
            - posY (``int``): The y-position where the portal should spawn
            - facing (``str``, optional): The direction the portal should face. Defaults to ``SOUTH``.
        """        
        super().__init__()
        all_sprites.add(self, layer = LAYER['portal_layer'])
        
        self.pos = vec((posX, posY))
        self.facing = facing

        self.setImages("sprites/portals/portals.png", 64, 64, 1, 1)
        self.setRects(self.pos.x, self.pos.y, 64, 64, 54, 54)

        self.image, self.hitbox = self.getFace()

    def getFace(self) -> tuple:
        if self.facing == SOUTH:
            return self.image, self.rect.inflate(0, -40)
        if self.facing == EAST:
            return pygame.transform.rotate(self.image, 90), self.rect.inflate(-40, 0)
        if self.facing == NORTH:
            return pygame.transform.rotate(self.image, 180), self.rect.inflate(0, -40)
        if self.facing == WEST:
            return pygame.transform.rotate(self.image, 270), self.rect.inflate(-40, 0)
        if self.facing == None:
            self.kill()

    def update(self):
        if self.facing == None:
            self.kill()
        
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def __repr__(self):
        return f'Portal({self.facing}, {self.pos})'


def portalCountCheck():
    """If there are more than two portals present during gameplay, the oldest one will be deleted to make room for another one."""    
    if len(all_portals) > 2:
        portalTemp = all_portals.sprites()
        if len(portalTemp) > 0:
            oldest_portal = portalTemp[0]
            oldest_portal.kill()
            all_portals.remove(oldest_portal)
            if len(portalTemp) > 1:
                all_portals.add(portalTemp[1:])