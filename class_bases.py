import pygame, time

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

    def tileTexture(self, colorkey: tuple):
        image_width, image_height = self.image.get_size()
        tile_width, tile_height = self.texture.get_size()

        for x in range(0, image_width, tile_width):
            for y in range(0, image_height, tile_height):
                tile_rect = pygame.Rect(x, y, tile_width, tile_height)
                self.image.blit(self.texture, tile_rect)

        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.hitbox = self.rect


class PortalBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.visible = True
    
    def changeRoomRight(self):
        self.pos.x -= WIN_WIDTH

    def changeRoomLeft(self):
        self.pos.x += WIN_WIDTH

    def changeRoomUp(self):
        self.pos.y += WIN_HEIGHT

    def changeRoomDown(self):
        self.pos.y -= WIN_HEIGHT


class StatBarBase(ActorBase):
    def __init__(self):
        super().__init__()