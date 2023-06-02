import pygame

from Calculations import *
from Constants import *
from Groups import *

vec = pygame.math.Vector2

class ActorBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all actors in the game."""        
        super().__init__()
        self.visible = True

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
            - ``layer_send`` ``(int)``: The layer the sprite should be added to
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

class EnemyBase(ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It contains parameters and methods to gain better control over enemy objects.
        """    
        super().__init__()
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.is_shooting = False

        #-------------------- In-game Stats --------------------#
        self.max_hp = None
        self.hp = None
        self.max_attack = None
        self.attack = None
        self.max_defense = None
        self.defense = None
        self.xp_worth = None

class PortalBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.visible = True
    
    def changeRoomRight(self):
        self.pos.x -= WINDOW_WIDTH

    def changeRoomLeft(self):
        self.pos.x += WINDOW_WIDTH

    def changeRoomUp(self):
        self.pos.y += WINDOW_HEIGHT

    def changeRoomDown(self):
        self.pos.y -= WINDOW_HEIGHT

class StatBarBase(ActorBase):
    def __init__(self):
        super().__init__()