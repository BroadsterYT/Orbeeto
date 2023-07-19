import pygame

from class_bases import *


class InvisObj(ActorBase):
    def __init__(self, posX: int, posY: int, width: int, height: int):
        super().__init__()
        self.show(LAYER['floor'])
        all_invisible.add(self)

        self.pos = vec((posX, posY))
        
        self.image = pygame.Surface(vec(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        pass


class Beam(ActorBase):
    def __init__(self, fromSprite: pygame.sprite.Sprite, toSprite: pygame.sprite.Sprite):
        super().__init__()
        self.show(LAYER['floor'])

        self.fromSprite, self.toSprite = fromSprite, toSprite
        self.index = 0
        
        self.length = getDistToCoords(self.fromSprite.pos, self.toSprite.pos)
        self.angle = getAngleToSprite(self.fromSprite, self.toSprite)
        self.image = pygame.Surface(vec(1, 1))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def buildSetup(self, startPos: pygame.math.Vector2, endPos: pygame.math.Vector2):
        self.length = getDistToCoords(startPos, endPos)
        self.angle = getAngleToSprite(self.fromSprite, self.toSprite)

        opp = (self.length / 2) * cos(rad(self.angle + 90))
        adj = (self.length / 2) * sin(rad(self.angle + 90))

        self.pos = vec(self.fromSprite.pos.x + opp, self.fromSprite.pos.y - adj)

    def buildImage(self, frameOffset: int) -> pygame.Surface:
        """Builds the image of the beam 
        
        ### Arguments
            - frameOffset (``int``): The frame from "beams.png" to build the beam from
        
        ### Returns
            - ``pygame.Surface``: The image of the beam
        """        
        self.spritesheet = Spritesheet("sprites/textures/beams.png", 1)
        baseImages = self.spritesheet.get_images(12, 12, 1, frameOffset)
        baseImage: pygame.Surface = baseImages[self.index]

        finalImage = pygame.Surface(vec(baseImage.get_width(), int(self.length)))

        offset = 0
        for i in range(int(self.length / baseImage.get_height())):
            finalImage.blit(baseImage, vec(0, offset))
            offset += baseImage.get_height()

        finalImage.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(finalImage, self.angle)

    def update(self):
        self.buildSetup(self.fromSprite.pos, self.toSprite.pos)
        self.buildImage(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
