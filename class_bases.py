import pygame, time

from calculations import *
from constants import *
from groups import *

vec = pygame.math.Vector2

class ActorBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all actors in the game."""        
        super().__init__()
        self.visible = True
        self.lastFrame = time.time()

        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.accel_const = 0.3
    
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