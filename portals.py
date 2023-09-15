import pygame
import os

from class_bases import *


class Portal(ActorBase):
    def __init__(self, spawnedFrom: pygame.sprite.Sprite, posX: int, posY: int, facing: str = SOUTH):
        """A portal that can teleport any moving object

        ### Arguments
            - posX (``int``): The x-position where the portal should spawn
            - posY (``int``): The y-position where the portal should spawn
            - facing (``str``, optional): The direction the portal should face. Defaults to ``SOUTH``.
        """        
        super().__init__()
        self.show(LAYER['portal'])
        all_portals.add(self)
        room = self.getRoom(); room.add(self)

        self.pos = vec((posX, posY))
        self.facing = facing

        self.landedOn = spawnedFrom.hit
        self.posOffset = vec(self.pos.x - self.landedOn.pos.x, self.pos.y - self.landedOn.pos.y)

        self.setImages("sprites/portals/portals.png", 64, 64, 1, 1)
        self.setRects(self.pos.x, self.pos.y, 64, 64, 54, 54)

        self.image, self.hitbox = self.__getFace()

    def __getFace(self) -> tuple:
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

    def movement(self):
        # Setting position to offset of where bullet landed
        self.pos = self.landedOn.pos + self.posOffset
        self.centerRects()

    def update(self):
        # self.movement()

        if self.facing == None:
            self.kill()

    def __repr__(self):
        return f'Portal({self.landedOn}, {self.facing}, {self.pos})'


class NewPortal(ActorBase):
    def __init__(self, portalBullet, posX: float, posY: float, facing: str = SOUTH):
        """A portal that can teleport any sprite that is able to fit inside.
        
        ### Arguments
            - portalBullet (``PortalBullet``): The bullet the portal is spawning from
            - posX (``float``): The x-position the portal should be spawned at
            - posY (``float``): The y-position the portal should be spawned at
            - facing (``str``, optional): The direction the portal should be facing. Defaults to ``SOUTH``.
        """        
        super.__init__()
        self.show(LAYER['portal'])
        all_portals.add(self)
        room = self.getRoom(); room.add(self) # Portal needs to belong to the room

        self.landedOn = portalBullet.hit
        self.facing = facing

        self.pos = vec((posX, posY))
        self.posOffset = vec(self.pos.x - self.landedOn.pos.x, self.pos.y - self.landedOn.pos.y)

        self.__initFace()

    def __initFace(self) -> None:
        """Initializes the images and hitbox of the portal. This method must be called in the __init__() method"""        
        def rotateImages(angle: float):
            """Rotates the references images of the portal's spritesheet.
            
            ### Arguments
                - angle (``float``): The angle to rotate the images by
            """            
            for i in range(len(self.origImages)):
                self.origImages[i] = pygame.transform.rotate(self.origImages[i], angle)
                
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.rotate(self.images[i], angle)


        if self.facing == SOUTH:
            self.setImages('sprites/portals/portals.png', 64, 64, 1, 1)
            self.setRects(self.pos.x, self.pos.y, 64, 64, 54, 14)

        elif self.facing == EAST:
            self.setImages('sprites/portals/portals.png', 64, 64, 1, 1)
            rotateImages(90)
            self.setRects(self.pos.x, self.pos.y, 64, 64, 14, 54)

        elif self.facing == NORTH:
            self.setImages('sprites/portals/portals.png', 64, 64, 1, 1)
            rotateImages(180)
            self.setRects(self.pos.x, self.pos.y, 64, 64, 54, 14)

        elif self.facing == WEST:
            self.setImages('sprites/portals/portals.png', 64, 64, 1, 1)
            rotateImages(270)
            self.setRects(self.pos.x, self.pos.y, 64, 64, 14, 54)


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


if __name__ == '__main__':
    os.system('python main.py')