import pygame
import os
import time
import copy

from calculations import *
from constants import *
from groups import *
from spritesheet import Spritesheet


class ActorBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all actors in the game."""        
        super().__init__()
        self.visible = True
        self.canUpdate = True
        self.lastFrame = time.time()

        self.pos = vec((0, 0))
        self.posCopy = self.pos.copy()
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cAccel = 0.3

        self.isGrappled = False
    
    # -------------------------------- Visibility -------------------------------- #
    def hide(self) -> None:
        """Makes the sprite invisible. The sprite's ``update()`` method will not be called."""
        self.visible = False
        if hasattr(self, 'healthBar'):
            self.healthBar.hide()
        all_sprites.remove(self)

    def show(self, layerSend) -> None:
        """Makes the sprite visible. The sprite's ``update()`` method will be called.
        
        ### Parameters
            - layer_send (``str``): The layer the sprite should be added to
        """        
        self.visible = True
        if hasattr(self, 'healthBar'):
            self.healthBar.show(LAYER['statbar'])
        all_sprites.add(self, layer = layerSend)

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
            - hitboxWidth (``int``): The width of the hitbox
            - hitboxHeight (``int``): The height of the hitbox
            - setPos (``bool``, optional): Should the rect and hitbox be snapped to the position of the sprite?. Defaults to ``True``.
        """        
        # self.image = self.images[self.index]
        # self.original_image = self.original_images[self.index]
        
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
    def velMovement(self, adjustCenterFirst: bool) -> None:
        """Makes a sprite move according to its velocity (``self.vel``)
        """
        if adjustCenterFirst:
            self.rect.center = self.pos
            self.hitbox.center = self.pos

            self.pos.x += self.vel.x
            self.pos.y += self.vel.y

        else:
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y
            
            self.rect.center = self.pos
            self.hitbox.center = self.pos

    def accelMovement(self) -> None:
        """Makes a sprite move according to its acceleration (``self.accel`` and ``self.cAccel``)
        """
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel
        self.pos += self.vel + self.cAccel * self.accel

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def collideCheck(self, *contactLists: list) -> None:
        """Check if the sprite comes into contact with another sprite from a specific group. 
        If the sprites do collide, then they will perform a hitbox collision.
        
        ### Arguments
            - contactLists (``list``): The sprite group(s) to check for a collision with
        """
        for list in contactLists:
            for sprite in list:
                if sprite.visible:
                    self.blockFromSide(sprite)

    def blockFromSide(self, sprite: pygame.sprite.Sprite) -> None:
        if self.hitbox.colliderect(sprite.hitbox):
            width = (self.hitbox.width + sprite.hitbox.width) // 2
            height = (self.hitbox.height + sprite.hitbox.height) // 2
            
            # If hitting the right side
            if (collideSideCheck(self, sprite) == EAST and
                # self.vel.x < 0 and
                self.pos.x <= sprite.pos.x + width):
                self.vel.x = 0
                self.pos.x = sprite.pos.x + width

            # Hitting bottom side
            if (collideSideCheck(self, sprite) == SOUTH and
                # self.vel.y < 0 and
                self.pos.y <= sprite.pos.y + height):
                self.vel.y = 0
                self.pos.y = sprite.pos.y + height

            # Hitting left side
            if (collideSideCheck(self, sprite) == WEST and
                # self.vel.x > 0 and
                self.pos.x >= sprite.pos.x - width):
                self.vel.x = 0
                self.pos.x = sprite.pos.x - width

            # Hitting top side
            if (collideSideCheck(self, sprite) == NORTH and
                # self.vel.y > 0 and
                self.pos.y >= sprite.pos.y - height):
                self.vel.y = 0
                self.pos.y = sprite.pos.y - height

    def teleport(self, portalIn) -> None:
        """Teleports a sprite from one portal to another
        
        ### Arguments
            - portalIn (``Portal``): The portal the sprite is entering
        """        
        portalOut: ActorBase = getOtherPortal(portalIn)
        width = (portalOut.hitbox.width + self.hitbox.width) // 2
        height = (portalOut.hitbox.height + self.hitbox.height) // 2
        
        # Makes sure that sprites dont repeatedly get thrown back into the portals b/c of room acceleration
        room = self.getRoom()
        velAdjust: vec = room.vel.copy()

        if portalIn.facing == SOUTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portalIn.pos.x)
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x - distOffset
                self.pos.y = portalOut.pos.y + height + abs(velAdjust.y)
                self.vel = self.vel.rotate(180)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width + abs(velAdjust.x)
                self.pos.y = portalOut.pos.y - distOffset
                self.vel = self.vel.rotate(90)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset 
                self.pos.y = portalOut.pos.y - height - abs(velAdjust.y)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width - abs(velAdjust.x)
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = self.vel.rotate(270)

        if portalIn.facing == EAST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portalIn.pos.y)
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x - distOffset
                self.pos.y = portalOut.pos.y + height + abs(velAdjust.y)
                self.vel = self.vel.rotate(270)
                
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width + abs(velAdjust.x)
                self.pos.y = portalOut.pos.y - distOffset
                self.vel = self.vel.rotate(180)

            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height - abs(velAdjust.y)
                self.vel = self.vel.rotate(90)

            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width - abs(velAdjust.x)
                self.pos.y = portalOut.pos.y + distOffset

        if portalIn.facing == NORTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portalIn.pos.x)
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height + abs(velAdjust.y)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width + abs(velAdjust.x)
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = self.vel.rotate(270)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x - distOffset
                self.pos.y = portalOut.pos.y - height - abs(velAdjust.y)
                self.vel = self.vel.rotate(180)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width - abs(velAdjust.x)
                self.pos.y = portalOut.pos.y - distOffset
                self.vel = self.vel.rotate(90)

        if portalIn.facing == WEST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portalIn.pos.y)
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height + abs(velAdjust.y)
                self.vel = self.vel.rotate(90)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width + abs(velAdjust.x)
                self.pos.y = portalOut.pos.y + distOffset
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x - distOffset
                self.pos.y = portalOut.pos.y - height - abs(velAdjust.y)
                self.vel = self.vel.rotate(270)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width - abs(velAdjust.x)
                self.pos.y = portalOut.pos.y - distOffset
                self.vel = self.vel.rotate(180)

# ----------------------------------- Rooms ---------------------------------- #
    def getRoom(self) -> pygame.sprite.AbstractGroup:
        """Returns the room object being used
        
        ### Returns
            - ``pygame.sprite.AbstractGroup``: The room object group
        """        
        return all_rooms[0]

    def changeRoom(self, direction: str):
        if direction == SOUTH:
            self.pos.y -= WINHEIGHT

        elif direction == EAST:
            self.pos.x -= WINWIDTH

        elif direction == NORTH:
            self.pos.y += WINHEIGHT

        elif direction == WEST:
            self.pos.y += WINWIDTH

        else:
            raise ValueError(f'Error: {direction} is not a valid input for changeRooms')


class AbstractBase(pygame.sprite.AbstractGroup):
    def __init__(self):
        """The base class for all standard abstract groups. Contains methods to help manipulate the abstract group."""        
        super().__init__()
        self.canUpdate = True
    
    def add(self, *sprites):
        """Adds one or more sprites to the abstract group.
        
        ### Parameters
            - sprites (``pygame.sprite.Sprite``): The sprite(s) to add to the group
        """         
        for sprite in sprites:
            super().add(sprite)


if __name__ == '__main__':
    os.system('python main.py')