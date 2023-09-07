import pygame
from pygame.locals import *

pygame.init()

import sys
import time
import copy

from math import sin, cos, floor

from init import anim_timer, keyReleased

from bullets import *
from enemies import *
from itemdrops import *
from spritesheet import *
from statbars import *
from text import *
from tiles import *
from trinkets import *

# Aliases
spriteGroup = pygame.sprite.Group

clock = pygame.time.Clock()

screenSize = (WINWIDTH, WINHEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED, 0, 0, 1)
pygame.display.set_caption('Orbeeto')


# ============================================================================ #
#                                 Player Class                                 #
# ============================================================================ #
class Player(ActorBase):
    def __init__(self):
        """A player sprite that can move and shoot."""        
        super().__init__()
        all_players.add(self)
        self.show(LAYER['player'])
        
        self.room: Room = self.getRoom()

        self.setImages("sprites/orbeeto/orbeeto.png", 64, 64, 5, 5)
        self.setRects(0, 0, 64, 64, 32, 32)

        self.pos = vec((WINWIDTH // 2, WINHEIGHT // 2 - 10))
        self.cAccel = 0.58

        # -------------------------------- Game Stats -------------------------------- #
        self.__setStats()

        # --------------------------------- Stat Bars -------------------------------- #
        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)
        self.ammoBar = AmmoBar(self)

        self.menu = InventoryMenu(self)
        
        self.inventory = {}
        for item in MAT.values():
            self.inventory.update({item: 0})

        self.bulletType = PROJ_STD
        self.canPortal = False
        self.canGrapple = True
        self.grapple = None

# ----------------------------------- Stats ---------------------------------- #
    def __setStats(self) -> None:
        """Initializes the starting stats of the player sprite
        """        
        self.xp: int = 0
        self.level: int = 0
        self.maxLevel: int = 249
        
        self.maxHp: int = 50
        self.hp: int = self.maxHp
        self.maxAtk: int = 10
        self.atk: int = self.maxAtk
        self.maxDef: int = 10
        self.defense: int = self.maxDef

        self.maxAmmo: int = 40
        self.ammo: int = self.maxAmmo
        self.bulletVel: float = 12.0
        self.gunCooldown: float = 0.12
        self.lastShot: float = time.time()

        self.grappleSpeed: float = 2.0
        
        self.hitTimeCharge = 1200
        self.hitTime = 0
        self.lastHit = time.time()

        self.updateLevel()

    def updateMaxStats(self):
        """Updates all of the player's max stats."""        
        self.maxHp = floor(eerp(50, 650, self.level / self.maxLevel))
        self.maxAtk = floor(eerp(10, 1250, self.level / self.maxLevel))
        self.maxDef = floor(eerp(15, 800, self.level / self.maxLevel))
        self.maxAmmo = floor(eerp(40, 1200, self.level / self.maxLevel))

        self.grappleSpeed = floor(eerp(2.0, 4.0, self.level / self.maxLevel))

        self.atk = self.maxAtk
        self.defense = self.maxDef

    def updateLevel(self):
        if self.xp > 582803:
            self.xp = 582803

        self.level = floor((256 * self.xp) / (self.xp + 16384))
        self.updateMaxStats()

# ------------------------------- Room Changing ------------------------------ #
    def changeRoom(self, direction: str) -> None:
        """Changes the player's current room
        
        ### Arguments
            - direction (``str``): The direction of the new room the player is traveling to
        
        ### Raises
            - ``ValueError``: Raised if the direction is not `NORTH`, `SOUTH`, `EAST`, or `WEST`
        """         
        if direction == SOUTH:
            self.room.room.y -= 1
            self.room.lastEntranceDir = SOUTH
            self.room.layoutUpdate()

        elif direction == EAST:
            self.room.room.x += 1
            self.room.lastEntranceDir = EAST
            self.room.layoutUpdate()

        elif direction == NORTH:
            self.room.room.y += 1
            self.room.lastEntranceDir = NORTH
            self.room.layoutUpdate()
        
        elif direction == WEST:
            self.room.room.x -= 1
            self.room.lastEntranceDir = WEST
            self.room.layoutUpdate()

        else:
            raise ValueError(f'Error: {direction} is not a valid room-changing direction.')

        killGroups(all_projs)

    def checkRoomChange(self) -> None:
        """Checks if the player should change rooms"""
        if self.hitbox.colliderect(self.room.borderSouth.hitbox):
            self.changeRoom(SOUTH)
        
        if self.hitbox.colliderect(self.room.borderEast.hitbox):
            self.changeRoom(EAST)

        if self.hitbox.colliderect(self.room.borderNorth.hitbox):
            self.changeRoom(NORTH)

        if self.hitbox.colliderect(self.room.borderWest.hitbox):
            self.changeRoom(WEST)

# --------------------------------- Movement --------------------------------- #
    def movement(self):
        """When called once every frame, it allows the player to recive input from the user and move accordingly"""        
        if self.canUpdate and self.visible:
            if not self.room.isScrollingX and not self.room.isScrollingY:
                self.collideCheck(all_walls)

            self.accel = self.getAccel()
            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        """Returns the acceleration that the player should undergo given specific conditions
        
        ### Returns
            - ``pygame.math.Vector2``: The acceleration value of the player
        """        
        finalAccel = vec(0, 0)
        if not self.room.isScrollingX:
            finalAccel.x += self.__getXAxisOutput()

        if not self.room.isScrollingY:
            finalAccel.y += self.__getYAxisOutput()

        return finalAccel
    
    def __getXAxisOutput(self) -> float:
        output: float = 0.0
        if isInputHeld[K_a]:
            output -= self.cAccel
        if isInputHeld[K_d]:
            output += self.cAccel

        if self.isSwinging():
            angle = getAngleToSprite(self, self.grapple)
            output += self.grappleSpeed * -sin(rad(angle))

        return output

    def __getYAxisOutput(self) -> float:
        output: float = 0.0
        if isInputHeld[K_w]:
            output -= self.cAccel
        if isInputHeld[K_s]:
            output += self.cAccel

        if self.isSwinging():
            angle = getAngleToSprite(self, self.grapple)
            output += self.grappleSpeed * -cos(rad(angle))
        
        return output

    def isSwinging(self) -> bool:
        """Determines if the player should be accelerating towards the grappling hook.
        
        ### Returns
            - ``bool``: Whether or not the player is swinging
        """
        output = False
        if self.grapple == None:
            return output
        elif not self.grapple.returning:
            return output
        elif self.grapple.grappledTo not in all_walls:
            return output
        else:
            output = True
            return output

    def shoot(self):
        """Shoots bullets"""
        angle = rad(getAngleToMouse(self))
        velX = self.bulletVel * -sin(angle)
        velY = self.bulletVel * -cos(angle)

        OFFSET = vec((21, 30))

        if (isInputHeld[1] and
            self.ammo > 0 and
            getTimeDiff(self.lastShot) >= self.gunCooldown):
            if self.bulletType == PROJ_STD:
                all_projs.add(
                    PlayerStdBullet(self,
                        self.pos.x - (OFFSET.x * cos(angle)) - (OFFSET.y * sin(angle)),
                        self.pos.y + (OFFSET.x * sin(angle)) - (OFFSET.y * cos(angle)),
                        velX, velY, 1
                    ),
                    
                    PlayerStdBullet(self,
                        self.pos.x + (OFFSET.x * cos(angle)) - (OFFSET.y * sin(angle)),
                        self.pos.y - (OFFSET.x * sin(angle)) - (OFFSET.y * cos(angle)),
                        velX, velY, 1
                    )
                )

            else:
                raise ValueError(f'Error: {self.bulletType} is not a valid bullet type.')
            
            self.ammo -= 1
            self.lastShot = time.time()

        # ------------------------------ Firing Portals ------------------------------ #
        if keyReleased[3] % 2 == 0 and self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = False

        elif keyReleased[3] % 2 != 0 and not self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = True

        # --------------------------- Firing Grappling Hook -------------------------- #
        if keyReleased[2] % 2 != 0 and self.canGrapple:
            if self.grapple != None:
                self.grapple.shatter()
            self.grapple = NewGrappleBullet(self, self.pos.x, self.pos.y, velX, velY)
            self.canGrapple = False

        if keyReleased[2] % 2 == 0 and not self.canGrapple:
            self.grapple.returning = True
            self.canGrapple = True

    def update(self):
        if self.canUpdate and self.visible:
            self.movement()
            self.shoot()
            self.checkRoomChange()

            # Animation
            if getTimeDiff(self.lastFrame) > 0.05:
                if isInputHeld[1]:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                else: # Idle animation
                    self.index = 0
                
                self.lastFrame = time.time()
            self.rotateImage(getAngleToMouse(self))

            # Teleporting
            if not self.room.isScrollingX and not self.room.isScrollingY:
                for portal in all_portals:
                    if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                        self.teleport(portal)

            # Dodge charge up
            if self.hitTime < self.hitTimeCharge:
                self.hitTime += 1

        self.menu.update()
        
        if self.hp <= 0:
            self.kill()

# ------------------------------- Magic Methods ------------------------------ #
    def __str__(self):
        return f'Player at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\ncurrent bullet: {self.bulletType}\nxp: {self.xp}\nlevel: {self.level}\n'

    def __repr__(self):
        return f'Player({self.pos}, {self.vel}, {self.accel}, {self.bulletType}, {self.xp}, {self.level})'


# ============================================================================ #
#                                  Room Class                                  #
# ============================================================================ #
class Room(AbstractBase):
    def __init__(self, roomX: int, roomY: int):
        """The room where all the current action is taking place

        ### Arguments:
            roomX (``int``): The room's x-axis location in the grid of the room layout
            roomY (``int``): The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        all_rooms.append(self)
        self.room = vec((roomX, roomY))
        self.size = vec((1280, 720))

        # self.roomOffset = vec(0, 0)
        
        self.lastEntranceDir = None
        self.isChangingRooms = False

        self.player1: Player = Player()
        self.posCopy = self.player1.pos.copy()
        self.offset = vec(self.player1.pos.x - 608, self.player1.pos.y - WINHEIGHT // 2)

        self.borderSouth = RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.borderEast = RoomBorder(WINWIDTH // 16, 0, 1, self.size.y // 16)
        self.borderNorth = RoomBorder(0, -1, self.size.x // 16, 1)
        self.borderWest = RoomBorder(-1, 0, 1, self.size.y // 16)
        # self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

        self.isScrollingX = True
        self.isScrollingY = True

        self.canSwitchX = True
        self.canSwitchY = True

        self.recenteringX = False
        self.recenteringY = False
        self.lastRecenterX = time.time()
        self.lastRecenterY = time.time()
        self.offsetX = self.player1.pos.x - 608
        self.offsetY = self.player1.pos.y - WINHEIGHT // 2

        # --------------------------------- Movement --------------------------------- #
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cAccel = self.player1.cAccel

        self.layoutUpdate()

    # ------------------------------- Room Movement ------------------------------ #
    def accelMovement(self) -> None:
        """Calculates the room's acceleration, velocity, and position"""        
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel
        self.pos = vec(self.borderWest.pos.x + self.borderWest.hitbox.width // 2, self.borderNorth.pos.y + self.borderNorth.height // 2)

    def getAccel(self) -> pygame.math.Vector2:
        finalAccel = vec(0, 0)
        if self.isScrollingX:
            finalAccel.x += self.__getXAxisOutput()
        
        if self.isScrollingY:
            finalAccel.y += self.__getYAxisOutput()

        return finalAccel

    def __getXAxisOutput(self) -> float:
        """Determines the amount of acceleration the room's x-axis component should have
        
        ### Returns
            - ``float``: The room's acceleration's x-axis component
        """        
        output: float = 0.0
        if isInputHeld[K_a]:
            output += self.player1.cAccel
        if isInputHeld[K_d]:
            output -= self.player1.cAccel

        if self.player1.isSwinging():
            angle = getAngleToSprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * sin(rad(angle))
        
        return output

    def __getYAxisOutput(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have
        
        ### Returns
            - ``float``: The room's acceleration's y-axis component
        """        
        output: float = 0.0
        if isInputHeld[K_w]:
            output += self.player1.cAccel
        if isInputHeld[K_s]:
            output -= self.player1.cAccel

        if self.player1.isSwinging():
            angle = getAngleToSprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * cos(rad(angle))

        return output
    
    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player"""   
        if self.canUpdate:
            self.accel = self.getAccel()
            self.accelMovement()

            if not (not self.isScrollingX and not self.isScrollingY):
                self.__spriteCollideCheck(self.player1, all_walls)

            if self.isScrollingX and self.isScrollingY:
                for sprite in all_movable:
                    self.__spriteCollideCheck(sprite, all_walls)

            # ------------------ Teleporting player when room scrolling ------------------ #
            for portal in all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portalIn: Portal = portal
                    portalOut: Portal = getOtherPortal(portalIn)

                    if len(all_portals) == 2:
                        self.__teleportPlayer(portalIn, portalOut)

            self.__recenterPlayerX()
            self.__recenterPlayerY()

            for sprite in self.__getSpritesToRecenter():
                sprite.movement()

    def __recenterPlayerX(self) -> None:
        if self.isScrollingX:
            if not self.recenteringX:
                if self.player1.pos.x != WINWIDTH // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetX = self.posCopy.x - WINWIDTH // 2
                    for sprite in self.__getSpritesToRecenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterX = time.time()
                    self.recenteringX = True
  
            if self.recenteringX:
                weight = getTimeDiff(self.lastRecenterX)
                if weight <= 0.25:
                    self.player1.pos.x = cerp(self.posCopy.x, WINWIDTH // 2, weight * 4)
                    for sprite in self.__getSpritesToRecenter():
                        sprite.pos.x = cerp(sprite.posCopy.x, sprite.posCopy.x - self.offsetX, weight * 4)
                else:
                    self.player1.pos.x = WINWIDTH // 2
                    self.recenteringX = False

    def __recenterPlayerY(self) -> None:
        if self.isScrollingY:
            if not self.recenteringY:
                if self.player1.pos.y != WINHEIGHT // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetY = self.posCopy.y - WINHEIGHT // 2
                    for sprite in self.__getSpritesToRecenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterY = time.time()
                    self.recenteringY = True

            if self.recenteringY:
                weight = getTimeDiff(self.lastRecenterY)
                if weight <= 0.25:
                    self.player1.pos.y = cerp(self.posCopy.y, WINHEIGHT // 2, weight * 4)
                    for sprite in self.__getSpritesToRecenter():
                        sprite.pos.y = cerp(sprite.posCopy.y, sprite.posCopy.y - self.offsetY, weight * 4)
                else:
                    self.player1.pos.y = WINHEIGHT // 2
                    self.recenteringY = False

    def __getSpritesToRecenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is recentered.
        
        ### Returns
            - ``list``: A list containing all sprites that should be relocated when the player is recentered
        """        
        outputList = []
        for sprite in self.sprites():
            outputList.append(sprite)

        for container in all_containers:
            if container.room == self.room:
                for sprite in container:
                    outputList.append(sprite)

        return outputList

    # -------------------------------- Teleporting ------------------------------- #
    def __teleportPlayer(self, portalIn: Portal, portalOut: Portal):
        """Teleports the player when the room is scrolling.
        
        ### Arguments
            - portalIn (``Portal``): The portal the player is entering
            - portalOut (``Portal``): The portal the player is exiting
        """
        width = (portalOut.hitbox.width + self.player1.hitbox.width) // 2
        height = (portalOut.hitbox.height + self.player1.hitbox.height) // 2


        def alignPlayer(tpOffset: float, direction: str) -> None:
            if direction == SOUTH:
                self.player1.pos.x = portalOut.pos.x - tpOffset
                self.player1.pos.y = portalOut.pos.y + height

            elif direction == EAST:
                self.player1.pos.x = portalOut.pos.x + width
                self.player1.pos.y = portalOut.pos.y - tpOffset
                
            elif direction == NORTH:
                self.player1.pos.x = portalOut.pos.x + tpOffset
                self.player1.pos.y = portalOut.pos.y - height

            elif direction == WEST:
                self.player1.pos.x = portalOut.pos.x - width
                self.player1.pos.y = portalOut.pos.y + tpOffset


        if self.isScrollingX and self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.__spritesRotateTrajectory(90)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.__spritesRotateTrajectory(270)

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.__spritesRotateTrajectory(270)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.__spritesRotateTrajectory(90)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)

            if portalIn.facing == NORTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.__spritesRotateTrajectory(270)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.__spritesRotateTrajectory(90)

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.__spritesRotateTrajectory(90)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.__spritesRotateTrajectory(270)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.__spritesRotateTrajectory(180)

        elif self.isScrollingX and not self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.player1.vel = self.player1.vel.rotate(180)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.__translateTrajectory(True, True, False)
                    self.player1.vel.y = 0

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.__translateTrajectory(True, True, True)
                    self.player1.vel.y = 0

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.player1.vel.y = self.vel.x

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.vel.x = -self.vel.x
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.__translateTrajectory(False, False, True)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)

            if portalIn.facing == NORTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)
                    self.__translateTrajectory(True, True, True)
                    self.player1.vel.y = 0

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.player1.vel = self.player1.vel.rotate(180)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.vel.x = self.player1.vel.y
                    self.player1.vel.y = self.player1.vel.x

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    alignPlayer(distOffset, SOUTH)
                    self.player1.vel = -self.vel.rotate(90)

                if portalOut.facing == EAST:
                    alignPlayer(distOffset, EAST)

                if portalOut.facing == NORTH:
                    alignPlayer(distOffset, NORTH)
                    self.player1.vel = -self.vel.rotate(270)

                if portalOut.facing == WEST:
                    alignPlayer(distOffset, WEST)
                    self.vel = self.vel.rotate(180)

        elif not self.isScrollingX and self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.__translateTrajectory(False, True, False)
                    self.player1.vel.y = 0

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y + distOffset
                    self.__translateTrajectory(False, True, True)
                    self.player1.vel.y = 0

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.__translateTrajectory(True, False, False)
                    self.player1.vel.x = 0

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel = self.player1.vel.rotate(180)
                    self.vel.y = -self.vel.y

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.__translateTrajectory(True, False, True)
                    self.player1.vel.x = 0

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y + distOffset

            if portalIn.facing == NORTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y + height

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y + distOffset
                    self.__translateTrajectory(False, True, True)
                    self.vel.y = 0

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.__spritesRotateTrajectory(180)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    # self.player1.vel.x = self.vel.y
                    # self.vel.y = 0
                    self.__translateTrajectory(False, True, False)

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.__translateTrajectory(True, False, True)
                    self.player1.vel.x = 0

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y + distOffset

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.__translateTrajectory(True, False, False)
                    self.player1.vel.x = 0

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel = self.player1.vel.rotate(180)
                    self.vel.y = -self.vel.y

    def __spritesRotateTrajectory(self, angle: float) -> None:
        """Rotates the velocities and accelerations of all the sprites within the room's sprites
        
        ### Arguments
            - angle (``float``): The angle to rotate the vectors by

        """
        self.accel = self.accel.rotate(angle)
        self.vel = self.vel.rotate(angle)
        
        for sprite in self.__getSpritesToRecenter():
            sprite.accel = sprite.accel.rotate(angle)
            sprite.vel = sprite.vel.rotate(angle)

    def __translateTrajectory(self, isPlayerToRoom: bool, isXToY: bool, isOutputNegative: bool = False) -> None:
        """Translates the velocity of the room's sprites to the player, or vice versa.
        
        ### Arguments
            - isPlayerToRoom (``bool``): Should velocity be translated from the player to the room (`True`), or from the room to the player (`False`)?
            - isXToY (``bool``): Should velocity be translated from the x-component to the y-component (`True`), or from the y-component to the x-component (`False`)?
            - isOutputNegative (``bool``): Should the translation be negative (`True`), or remain positive (`False`)?
        """        
        if isPlayerToRoom:
            if isXToY:
                if isOutputNegative:
                    for sprite in self.__getSpritesToRecenter():
                        sprite.vel.x = -self.player1.vel.y

                elif not isOutputNegative:
                    for sprite in self.__getSpritesToRecenter():
                        sprite.vel.x = self.player1.vel.y

            elif not isXToY:
                if isOutputNegative:
                    for sprite in self.__getSpritesToRecenter():
                        sprite.vel.y = -self.player1.vel.x

                elif not isOutputNegative:
                    for sprite in self.__getSpritesToRecenter():
                        sprite.vel.y = self.player1.vel.x

        elif not isPlayerToRoom:
            if isXToY:
                if isOutputNegative:
                    self.player1.vel.x = -self.vel.y

                elif not isOutputNegative:
                    self.player1.vel.x = self.vel.y

            elif not isXToY:
                if isOutputNegative:
                    self.player1.vel.y = -self.vel.x

                elif not isOutputNegative:
                    self.player1.vel.y = self.vel.x

    # ----------------------------- Sprite Collisions ---------------------------- #
    def __spriteCollideCheck(self, instig: ActorBase, *contactList: AbstractBase):
        """Collide check for when the room is scrolling
        
        ### Arguments
            - instig (``ActorBase``): The sprite instigating the collision
            - contactList (``AbstractBase``): The sprite group(s) to check for a collision with
        """
        for list in contactList:
            for sprite in list:
                if sprite.visible and isinstance(instig, Player):
                    self.__playerBlockFromSide(instig, sprite)
                elif sprite.visible:
                    self.__spriteBlockFromSide(instig, sprite)

    def __playerBlockFromSide(self, instig: Player, sprite: ActorBase):
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if triangleCollide(instig, sprite) == SOUTH and (instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self.accel.y = 0
                self.vel.y = 0
                # if not self.isScrollingX and self.isScrollingY:
                instig.pos.y = sprite.pos.y + height

            if triangleCollide(instig, sprite) == EAST and (instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self.accel.x = 0
                self.vel.x = 0
                # if self.isScrollingX and not self.isScrollingY:
                instig.pos.x = sprite.pos.x + width

            if triangleCollide(instig, sprite) == NORTH and (instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self.accel.y = 0
                self.vel.y = 0
                # if not self.isScrollingX and self.isScrollingY:
                instig.pos.y = sprite.pos.y - height

            if triangleCollide(instig, sprite) == WEST and (instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self.accel.x = 0
                self.vel.x = 0
                # if self.isScrollingX and not self.isScrollingY:
                instig.pos.x = sprite.pos.x - width

    def __spriteBlockFromSide(self, instig: ActorBase, sprite: ActorBase):
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if collideSideCheck(instig, sprite) == SOUTH and instig.pos.y <= sprite.pos.y + height and (instig.vel.y < 0 or sprite.vel.y > 0):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if collideSideCheck(instig, sprite) == EAST and instig.pos.x <= sprite.pos.x + width and (instig.vel.x < 0 or sprite.vel.x > 0):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if collideSideCheck(instig, sprite) == NORTH and instig.pos.y >= sprite.pos.y - height and (instig.vel.y > 0 or sprite.vel.y < 0):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if collideSideCheck(instig, sprite) == WEST and instig.pos.x >= sprite.pos.x - width and (instig.vel.x > 0 or sprite.vel.x < 0):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    # -------------------------------- Room Layout ------------------------------- # 
    def __setRoomBorders(self, roomWidth: int, roomHeight: int):
        self.borderSouth = RoomBorder(0, roomHeight // 16, roomWidth // 16, 1)
        self.borderEast = RoomBorder(roomWidth // 16, 0, 1, roomHeight // 16)
        self.borderNorth = RoomBorder(0, -1, roomWidth // 16, 1)
        self.borderWest = RoomBorder(-1, 0, 1, roomHeight // 16)
        
        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

    def __initRoom(self, roomSizeX: int, roomSizeY: int, canScrollX: bool, canScrollY: bool) -> None:
        """Initializes what a room's properties will be. This function must be called once for every `self.room` iteration.
        
        ### Arguments
            - roomSizeX (``int``): The width of the room (in pixels).
            - roomSizeY (``int``): The height of the room (in pixels).
            - canScrollX (``bool``): Should the room scroll with the player along the x-axis?
            - canScrollY (``bool``): Should the room scroll with the player along the y-axis?
        """        
        playerVelCopy = self.player1.vel.copy()
        self.player1.vel = vec(0, 0)
        self.size = vec((roomSizeX, roomSizeY))

        scrollCopyX = copy.copy(self.isScrollingX)
        scrollCopyY = copy.copy(self.isScrollingY)

        self.isScrollingX = canScrollX
        self.isScrollingY = canScrollY

        self.__setRoomBorders(roomSizeX, roomSizeY)

        if self.lastEntranceDir == SOUTH:
            self.player1.pos.x = self.borderNorth.pos.x
            self.player1.pos.y = self.borderNorth.pos.y + self.borderNorth.hitbox.height // 2 + self.player1.hitbox.height // 2
            self.__getRoomChangeTrajectory(scrollCopyX, scrollCopyY, self.isScrollingX, self.isScrollingY, playerVelCopy)
        
        elif self.lastEntranceDir == EAST:
            self.player1.pos.x = self.borderWest.pos.x + self.borderWest.hitbox.width // 2 + self.player1.hitbox.width // 2
            self.player1.pos.y = self.borderWest.pos.y
            self.__getRoomChangeTrajectory(scrollCopyX, scrollCopyY, self.isScrollingX, self.isScrollingY, playerVelCopy)
        
        elif self.lastEntranceDir == NORTH:
            self.player1.pos.x = self.borderSouth.pos.x
            self.player1.pos.y = self.borderSouth.pos.y - self.borderSouth.hitbox.height // 2 - self.player1.hitbox.height // 2
            self.__getRoomChangeTrajectory(scrollCopyX, scrollCopyY, self.isScrollingX, self.isScrollingY, playerVelCopy)
        
        elif self.lastEntranceDir == WEST:
            self.player1.pos.x = self.borderEast.pos.x - self.borderEast.hitbox.width // 2 - self.player1.hitbox.width // 2
            self.player1.pos.y = self.borderEast.pos.y
            self.__getRoomChangeTrajectory(scrollCopyX, scrollCopyY, self.isScrollingX, self.isScrollingY, playerVelCopy)

        else:
            print('no value')

    def __getRoomChangeTrajectory(self, prevRoomScrollX: bool, prevRoomScrollY: bool, newRoomScrollX: bool, newRoomScrollY: bool, playerVel: pygame.math.Vector2) -> None:
        if prevRoomScrollX:
            if not newRoomScrollX:
                self.player1.vel.x = -self.vel.x
        
        elif not prevRoomScrollX:
            if newRoomScrollX:
                self.vel.x = -playerVel.x
                print(self.vel)

        if prevRoomScrollY:
            if not newRoomScrollY:
                self.player1.vel.y = -self.vel.y

        elif not prevRoomScrollY:
            if newRoomScrollY:
                self.vel.y = -playerVel.y

    def layoutUpdate(self) -> None:
        """Updates the layout of the room"""   
        for sprite in self.sprites():
            sprite.kill()

        container: EntityContainer
        for container in all_containers:
            container.hideSprites()
        
        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            self.__initRoom(WINWIDTH, WINHEIGHT, True, True)

            self.add(
                Wall(0, 0, 8, 8),
                Wall(0, 37, 8, 8),
                Wall(72, 0, 8, 8),
                Wall(72, 37, 8, 8),
                Button(1, 14, 38),
            )
            
            try:
                container: EntityContainer = next(c for c in all_containers if c.room == self.room)
                container.showSprites()

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        Box(0, WINWIDTH // 2, WINHEIGHT // 2)
                    )
                )

        if self.room == vec(0, 1):
            self.__initRoom(WINWIDTH, WINHEIGHT, False, True)
            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 20, 8, 8)
            )
            
            try:
                container: EntityContainer = next(c for c in all_containers if c.room == self.room)
                container.showSprites()

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

        if self.room == vec(-1, 0):
            self.__initRoom(WINWIDTH, WINHEIGHT, False, False)

            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 8, 8, 8)
            )
            
            try:
                container: EntityContainer = next(c for c in all_containers if c.room == self.room)
                container.showSprites()

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

        if self.room == vec(1, 0):
            self.__initRoom(WINWIDTH, WINHEIGHT, False, False)

            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 8, 8, 8)
            )
            
            try:
                container: EntityContainer = next(c for c in all_containers if c.room == self.room)
                container.showSprites()

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

    def update(self):
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'


class EntityContainer(AbstractBase):
    def __init__(self, roomX: int, roomY: int, *sprites):
        """A container for enemies. Contains data about all enemies in a room.

        ### Arguments
            roomX (``int``): The container's x-location in the room grid
            roomY (``int``): The container's y-location in the room grid
            sprites (``EnemyBase``): The sprite(s) that should be added to the container
        """        
        super().__init__()
        self.room = vec((roomX, roomY))

        for sprite in sprites:
            self.add(sprite)

    def hideSprites(self):
        """Hides all of the enemies in the container"""
        for sprite in self.sprites():
            sprite.hide()

    def showSprites(self):
        for sprite in self.sprites():
            sprite.show(LAYER['enemy'])
            sprite.accel = vec(0, 0)
            sprite.vel = vec(0, 0)
            sprite.pos = sprite.roomPos


# ============================================================================ #
#                                 Menu Classes                                 #
# ============================================================================ #
class InventoryMenu(AbstractBase):
    def __init__(self, owner: Player):
        """A menu used to view collected items and utilize them for various purposes
        
        ### Arguments
            - owner ``(pygame.sprite.Sprite)``: The player whom the inventory belongs to
        """        
        super().__init__()
        self.cyclingLeft = False
        self.cyclingRight = False

        self.owner = owner
        
        self.wipeTime = 1
        self.window = 0
        
        self.lastCycle = time.time()

        self.rightArrow = RightMenuArrow(WINWIDTH - 64, WINHEIGHT / 2)
        self.leftArrow = LeftMenuArrow(64, WINHEIGHT / 2)
        
        self.add(
            self.buildMenuSlots()
        )

    def hide(self):
        """Makes all of the elements of the inventory menu invisible (closes the inventory menu)"""        
        for sprite in self.sprites():
            all_sprites.remove(sprite)

    def show(self):
        """Makes all of the elements of the inventory menu visible"""        
        for sprite in self.sprites():
            all_sprites.add(sprite, layer = LAYER['ui_1'])

    def cycleMenu(self):
        if (not self.cyclingLeft and 
            not self.cyclingRight and
            not self.canUpdate):
            if isInputHeld[1] and self.leftArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window -= 1
                self.lastCycle = time.time()
                self.cyclingLeft = True

            if isInputHeld[1] and self.rightArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window += 1
                self.lastCycle = time.time()
                self.cyclingRight = True

        # Cycling left
        if self.cyclingLeft and not self.cyclingRight:
            weight = getTimeDiff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = cerp(sprite.start_pos.x, sprite.start_pos.x - WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cyclingLeft = False

        # Cycling right
        if not self.cyclingLeft and self.cyclingRight:
            weight = getTimeDiff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = cerp(sprite.start_pos.x, sprite.start_pos.x + WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cyclingRight = False

    def buildMenuSlots(self):
        space = vec(0, 0)
        space_cushion = vec(82, 82)
        menu_slots = []
        slot_count = 0
        offset = 0
        for y in range(5):
            for x in range(5):
                menu_slots.append(MenuSlot(self.owner, 64 + space.x, 64 + space.y, None))
                space.x += space_cushion.x
                offset += 1
                slot_count += 1
            space.y += space_cushion.y
            space.x = 0
        return menu_slots

    def updateMenuSlots(self):
        for material in self.owner.inventory:
            if self.owner.inventory[material] > 0: # Every material in the owner's inventory
                for slot in self.sprites():
                    if slot.holding == material:
                        break
                    if slot.holding is None:
                        slot.holding = material
                        break
            for slot in self.sprites():
                slot.createSlotImages()

    def update(self):
        if keyReleased[K_e] % 2 != 0 and keyReleased[K_e] > 0:
            self.show()
            self.rightArrow.show(LAYER['ui_1'])
            self.leftArrow.show(LAYER['ui_1'])
            
            self.canUpdate = False
            for sprite in all_sprites:
                sprite.canUpdate = False

        elif keyReleased[K_e] % 2 == 0 and keyReleased[K_e] > 0:
            self.hide()
            self.rightArrow.hide()
            self.leftArrow.hide()
            
            self.canUpdate = True
            for sprite in all_sprites:
                sprite.canUpdate = True
            
        self.cycleMenu()


class RightMenuArrow(ActorBase):
    def __init__(self, posX, posY):
        """A UI element that allows players to cycle through menu screens to the right.
        
        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """        
        super().__init__()
        self.pos = vec((posX, posY))
        self.return_pos = vec((posX, posY))
        
        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.getImages(64, 64, 61)
        self.index = 1

        self.image = pygame.transform.scale(self.images[self.index], (64, 64))
        
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(posX - 32, posY - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it"""        
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        global anim_timer
        if anim_timer % 1 == 0:
            if self.index > 60:
                self.index = 1
            
            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            self.index += 1

        self.hover()


class LeftMenuArrow(ActorBase):
    def __init__(self, posX, posY):
        """A UI element that allows players to cycle through menu screens to the left.
        
        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((posX, posY))
        self.return_pos = vec((posX, posY))
        
        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.getImages(64, 64, 61)
        self.index = 1

        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(posX - 32, posY - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it"""        
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        global anim_timer
        if anim_timer % 1 == 0:
            if self.index > 60:
                self.index = 1
            
            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)
            self.index += 1

        self.hover()


class MenuSlot(ActorBase):
    def __init__(self, owner: Player, posX: float, posY: float, itemHeld: str):
        """A menu slot that shows the collected amount of a specific item
        
        ### Arguments
            - owner (``player``): The owner of the inventory to whom the menu slot belongs to
            - posX (``float``): The x-position to spawn at
            - posY (``float``): The y-position to spawn at
            - itemHeld (``str``): The item the menu slot will hold. Items are chosen from ``MATERIALS`` dictionary.
        """
        super().__init__()
        all_slots.add(self)
        self.owner = owner

        self.pos = vec((posX, posY))
        self.start_pos = vec((posX, posY))
        self.holding = itemHeld
        self.count = 0

        self.menusheet = Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.itemsheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.menu_imgs = self.menusheet.getImages(64, 64, 1)
        
        self.index = 0

        self.menu_img = self.menu_imgs[0]

        self.images = self.createSlotImages()
        self.image: pygame.Surface = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def hover(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            s_time = time.time()
            scale = abs(sin(s_time)) / 2
            self.image = pygame.transform.scale_by(self.images[self.index], 1 + scale)
            self.rect = self.image.get_rect(center = self.rect.center)

        else:
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center = self.rect.center)

    def getItemImages(self) -> list:
        if self.holding == MAT[0]:
            return self.itemsheet.getImages(32, 32, 1, 0)
        elif self.holding == MAT[1]:
            return self.itemsheet.getImages(32, 32, 1, 1)
        else:
            return self.itemsheet.getImages(32, 32, 1, 0)

    def createSlotImages(self):
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that item on top
        
        ### Returns
            - list: A list of the created images
        """        
        self.item_imgs = self.getItemImages()
        finalImages = []
        if self.holding != None:
            for frame in self.item_imgs:
                new_img = combineImages(self.menu_img, frame)

                # Adding the count of the item to its images
                countSurface = textToImage(str(self.count), 'sprites/ui/font.png', 9, 14, 36)
                new_img.set_colorkey((0, 0, 0))
                center_x = (new_img.get_width() - frame.get_width()) // 2
                center_y = (new_img.get_height() - frame.get_height()) // 2
                new_img.blit(swapColor(swapColor(countSurface, (44, 44, 44), (156, 156, 156)), (0, 0, 1), (255, 255, 255)), vec(center_x, center_y))
                finalImages.append(new_img)

        else:
            finalImages.append(self.menu_img)


        return finalImages

    def update(self):
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        
        if self.holding != None:
            self.count = self.owner.inventory[self.holding]
        
        self.images = self.createSlotImages()
        self.hover()


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
def redrawGameWindow():
    """Draws all sprites every frame
    """
    mainroom.update()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
# Load room
mainroom = Room(0, 0)

def checkKeyRelease(isMouse, *inputs):
    """Checks if any input(s) has been released. If one has, then its count in ''keyReleased'' will be updated to match.
    
    ### Arguments
        - isMouse (``bool``): Are the inputs mouse buttons?
        - inputs (``str``): The input(s) to check
    """
    if isMouse == False:
        for key in inputs:
            if event.type == pygame.KEYUP and event.key == key:
                if key in isInputHeld and key in keyReleased:
                    keyReleased[key] += 1
    else:
        for button in inputs:
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                if button in isInputHeld and button in keyReleased:
                    keyReleased[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
running = True
while running:
    anim_timer += 1

    for a_player in all_players:
        if a_player.hp <= 0:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()

        if event.type == QUIT or keyPressed[K_ESCAPE]:
            sys.exit()

        isInputHeld = {
            1: pygame.mouse.get_pressed(5)[0],
            2: pygame.mouse.get_pressed(5)[1],
            3: pygame.mouse.get_pressed(5)[2],

            K_a: keyPressed[K_a],
            K_w: keyPressed[K_w],
            K_s: keyPressed[K_s],
            K_d: keyPressed[K_d],
            K_x: keyPressed[K_x],
            K_e: keyPressed[K_e]
        }

        checkKeyRelease(False, K_e, K_x)
        checkKeyRelease(True, 1, 2, 3)

        if event.type == pygame.MOUSEWHEEL:
            # Player ammo refill
            if mainroom.player1.ammo < mainroom.player1.maxAmmo:
                mainroom.player1.ammo += 1

    screen.fill((255, 250, 255))

    # ------------------------------ Game Operation ------------------------------ #
    # Regenerate health for testing purposes
    for a_player in all_players:
        if anim_timer % 5 == 0 and a_player.hp < a_player.maxHp and isInputHeld[K_x]:
            a_player.hp += 1

    # ------------------------------- Redraw Window ------------------------------ #
    redrawGameWindow()
    clock.tick_busy_loop(FPS)