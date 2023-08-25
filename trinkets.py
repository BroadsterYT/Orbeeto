import pygame
import os

from class_bases import *
from tiles import TileBase


class Box(ActorBase):
    def __init__(self, idValue, posX, posY):
        super().__init__()
        self.show(LAYER['trinket'])
        all_movable.add(self)
        all_trinkets.add(self)

        self.idValue = idValue

        self.pos = vec((posX, posY))

        room = self.getRoom()
        self.cAccel = 0.8
        
        self.setImages("sprites/textures/box.png", 64, 64, 5, 1, 0, 0)
        self.setRects(0, 0, 64, 64, 64, 64, True)

    def movement(self):
        if self.canUpdate:
            self.collideCheck(all_walls)

            self.accel = self.getAccel()
            self.accelMovement()
    
    def getAccel(self) -> pygame.math.Vector2:
        room = self.getRoom()
        finalAccel = vec(0, 0)

        finalAccel += room.getAccel()

        for a_player in all_players:
            if self.hitbox.colliderect(a_player.hitbox):
                if collideSideCheck(self, a_player) == SOUTH:
                    finalAccel.y += self.cAccel
                if collideSideCheck(self, a_player) == EAST:
                    finalAccel.x += self.cAccel
                if collideSideCheck(self, a_player) == NORTH:
                    finalAccel.y -= self.cAccel
                if collideSideCheck(self, a_player) == WEST:
                    finalAccel.x -= self.cAccel
        
        return finalAccel

    def update(self):
        self.movement()

        # Teleporting
        for portal in all_portals:
            if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                self.teleport(portal)


class Button(ActorBase):
    def __init__(self, idValue: int, blockPosX: int, blockPosY: int):
        """A button that can be activated and deactivated
        
        ### Arguments
            - idValue (``int``): _description_
            - blockPosX (``int``): _description_
            - blockPosY (``int``): _description_
        """        
        super().__init__()
        self.show(LAYER['trinket'])
        all_trinkets.add(self)

        self.activated = False

        self.idValue = idValue
        self.pos = vec((blockPosX * 16, blockPosY * 16))

        self.setImages('sprites/trinkets/button.png', 64, 64, 2, 2)
        self.setRects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def __activeCheck(self) -> bool:
        isActive = False
        for box in all_movable:
            if not self.hitbox.colliderect(box.hitbox):
                return isActive
            else:
                isActive = True
                return isActive
    
    def getState(self):
        return self.__activeCheck()

    def movement(self):
        self.accel = vec(0, 0)
        if self.canUpdate and self.visible:
            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        finalAccel = vec(0, 0)
        return finalAccel

    def update(self):
        if self.__activeCheck():
            self.index = 1
        elif not self.__activeCheck():
            self.index = 0
        
        self.renderImages()

    def __repr__(self):
        return f'Button({self.idValue}, {self.pos}, {self.__activeCheck()})'


class LockedWall(TileBase):
    def __init__(self, idValue: int, sBlockPosX: int, sBlockPosY: int, eBlockPosX: int, eBlockPosY: int, blockWidth: int, blockHeight: int):
        """A wall that will move when activated by a switch or button
        
        ### Arguments
            - idValue (``int``): The ID value of the wall. A button with the same ID value must be present in the same room!
            - sBlockPosX (``int``): The x position where the wall should be placed in "tiles" (0 being the left edge and 80 being the right)
            - sBlockPosY (``int``): The y position where the wall should be placed in "tiles" (0 being the top edge and 45 being the bottom)
            - eBlockPosX (``int``): The x position where the wall should relocate after being activated (0 being the left edge and 80 being the right)
            - eBlockPosY (``int``): The y position where the wall should relocate after being activated (0 being the top edge and 45 being the bottom)
            - blockWidth (``int``): The width of the wall in "tiles"
            - blockHeight (``int``): The height of the wall in "tiles"
        """        
        super().__init__(sBlockPosX, sBlockPosY, blockWidth, blockHeight)
        self.show(LAYER['wall'])
        all_walls.add(self)
        all_trinkets.add(self)
        self.idValue = idValue

        self.switch: Button = self.__findSwitch()
        self.lastSwitchState = self.switch.getState()
        self.hasActivated = False
        self.lastChange = time.time()
        
        self.pos = getTopLeftCoords(self.width, self.height, sBlockPosX * self.tileSize, sBlockPosY * self.tileSize)
        self.startPos = getTopLeftCoords(self.width, self.height, sBlockPosX * self.tileSize, sBlockPosY * self.tileSize)
        self.endPos = getTopLeftCoords(self.width, self.height, eBlockPosX * self.tileSize, eBlockPosY * self.tileSize)

        self.spritesheet = Spritesheet('sprites/tiles/wall.png', 1)
        self.textures = self.spritesheet.get_images(16, 16, 1)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, BLACK)

        self.setRects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def __findSwitch(self) -> pygame.sprite.Sprite:
        try:
            switchMatch = next(s for s in all_trinkets if s.idValue == self.idValue)
            return switchMatch
        except StopIteration:
            raise CustomError(f'Error: No switch with idValue of {self.idValue} found')

    def __activate(self):
        currentSwitchState = self.switch.getState()
        if currentSwitchState != self.lastSwitchState:
            # Button state has changed, update lastChange and reset position
            self.lastChange = time.time()
            self.lastSwitchState = currentSwitchState

        weight = getTimeDiff(self.lastChange) / 3
        if not self.switch.getState() and self.hasActivated:
            self.pos = cerp(self.pos, self.startPos, weight)
        elif self.switch.getState():
            self.hasActivated = True
            self.pos = cerp(self.pos, self.endPos, weight)

    def update(self):
        self.__activate()
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def __repr__(self):
        return f'LockedWall({self.idValue}, {self.pos}, {self.switch})'
    

if __name__ == '__main__':
    os.system('python main.py')