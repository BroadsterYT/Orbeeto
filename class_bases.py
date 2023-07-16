import pygame
import time

from calculations import *
from constants import *
from groups import *
from spritesheet import Spritesheet


class ActorBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all actors in the game."""        
        super().__init__()
        self.visible = True
        self.lastFrame = time.time()

        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.ACCELC = 0.3

        self.isGrappled = False
    
    # -------------------------------- Visibility -------------------------------- #
    def hide(self):
        """Makes the sprite invisible. The sprite's ``update()`` method will not be called."""
        self.visible = False
        all_sprites.remove(self)

    def show(self, layer_send):
        """Makes the sprite visible. The sprite's ``update()`` method will be called.
        
        ### Parameters
            - layer_send (``str``): The layer the sprite should be added to
        """        
        self.visible = True
        all_sprites.add(self, layer = layer_send)
    
    # ----------------------------- Images and Rects ----------------------------- #
    def setImages(self, imageFile: str, frameWidth: int, frameHeight: int, spritesPerRow: int, imageCount: int, imageOffset: int = 0, index: int = 0):
        """Initializes the sprite's spritesheet, images, and animations. Should be used in the object's ``__init__()`` method.
        
        ### Parameters
            - imageFile (``str``): The path of the spritesheet image
            - frameWidth (``int``): The width of each individual frame
            - frameHeight (``int``): The height of each individual frame
            - spritesPerRow (``int``): The number of sprites within each row of the sprite sheet
            - imageCount (``int``): The number of images in the sprite's animation
            - imageOffset (``int``, optional): The index of the frame to begin the snip from. Defaults to ``0``.
            - index (``int``, optional): The index of the sprite's animation to start from. Defaults to ``0`` (the first image).
        """        
        self.spritesheet = Spritesheet(imageFile, spritesPerRow)
        self.images = self.spritesheet.get_images(frameWidth, frameHeight, imageCount, imageOffset)
        self.original_images = self.spritesheet.get_images(frameWidth, frameHeight, imageCount, imageOffset)
        self.index = index

        self.renderImages()

    def renderImages(self):
        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

    def setRects(self, rectPosX: int, rectPosY: int, rectWidth: int, rectHeight: int, hitboxWidth: int, hitboxHeight: int, setPos: bool = True):
        """Defines the rect and hitbox of a sprite
        
        ### Parameters
            - rectPosX (``int``): The x-axis position to spawn the rect and hitbox
            - rectPosY (``int``): The y-axis position to spawn the rect and hitbox
            - rectWidth (``int``): The width of the rect
            - rectHeight (``int``): The height of the rect
            - hitboxInfWidth (``int``, optional): The change in width of the hitbox with respect to the rect. Defaults to ``0`` (rect and hitbox have same width).
            - hitboxInfHeight (``int``, optional): The change in height of the hitbox with respect to the rect. Defaults to ``0`` (rect and hitbox have same height).
            - setPos (``bool``, optional): Should the rect and hitbox be snapped to the position of the sprite?. Defaults to ``True``.
        """        
        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(rectPosX, rectPosY, rectWidth, rectHeight)
        self.hitbox = pygame.Rect(rectPosX, rectPosY, hitboxWidth, hitboxHeight)

        if setPos:
            self.rect.center = self.pos
            self.hitbox.center = self.pos

    def rotateImage(self, angle: float):
        """Rotates the sprite's image by a specific angle
        
        ### Parameters
            - angle (``float``): The angle to rotate the sprite's image by
        """        
        self.original_image = self.original_images[self.index]
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center = self.rect.center)
    
    # ---------------------------------- Physics --------------------------------- #
    def accelMovement(self, deltaTime: float):
        """Makes a sprite move according to its acceleration (``self.accel`` and ``self.ACCELC``)
        
        ``self.accel`` MUST BE (0, 0) BEFORE THIS FUCNTION IS CALLED
        
        ### Arguments
            - deltaTime (``float``): The difference in time between frame updates
        """
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel * deltaTime
        self.pos += self.vel + self.ACCELC * self.accel

    def velMovement(self, deltaTime: float):
        """Makes a sprite move according to its velocity (``self.vel``)
        
        ### Arguments
            - deltaTime (``float``): The difference in time between frame updates
        """
        self.rect.center = self.pos
        self.hitbox.center = self.pos 
        
        self.pos.x += self.vel.x * deltaTime
        self.pos.y += self.vel.y * deltaTime

    def changeRoomRight(self):
        self.pos.x -= WIN_WIDTH

    def changeRoomLeft(self):
        self.pos.x += WIN_WIDTH

    def changeRoomUp(self):
        self.pos.y += WIN_HEIGHT

    def changeRoomDown(self):
        self.pos.y -= WIN_HEIGHT


class AbstractBase(pygame.sprite.AbstractGroup):
    def __init__(self):
        """The base class for all standard abstract groups. Contains methods to help manipulate the abstract group."""        
        super().__init__()
    
    def add(self, *sprites):
        """Adds one or more sprites to the abstract group.
        
        ### Parameters
            - sprites (``pygame.sprite.Sprite``): The sprite(s) to add to the group
        """         
        for sprite in sprites:
            super().add(sprite)


class EnvirBase(ActorBase):
    def __init__(self):
        super().__init__()

    def tileTexture(self, blockWidth: int, blockHeight: int, texture: pygame.Surface, colorkey: tuple) -> pygame.Surface:
        """Tiles a texture across an image
        
        ### Arguments
            - blockWidth (``int``): The width of the final image in "blocks"
            - blockHeight (``int``): The height of the final image in "blocks"
            - texture (``pygame.Surface``): The texture that should be repeated across the final image
            - colorkey (``tuple``): The color to set as the colorkey on the final image
        
        ### Returns
            - ``pygame.Surface``: The final image with the repeated texture
        """        
        finalImage = pygame.Surface(vec(blockWidth * 16, blockHeight * 16))

        imageWidth, imageHeight = finalImage.get_size()
        textureWidth, textureHeight = texture.get_size()

        for x in range(0, imageWidth, textureWidth):
            for y in range(0, imageHeight, textureHeight):
                tile_rect = pygame.Rect(x, y, textureWidth, textureHeight)
                finalImage.blit(texture, tile_rect)

        finalImage.set_colorkey(colorkey)
        return finalImage


class PortalBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.visible = True


class DropBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.ACCELC = 0.8
