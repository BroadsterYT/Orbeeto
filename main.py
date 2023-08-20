import pygame
from pygame.locals import *

pygame.init()

import sys
import time
import itertools

from math import sin, cos, radians, degrees, floor, pi
from init import *

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
rad = radians
deg = degrees

clock = pygame.time.Clock()

screenSize = (WINWIDTH, WINHEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED, 0, 0, 1)
pygame.display.set_caption('Orbeeto')


# ============================================================================ #
#                                 Player Class                                 #
# ============================================================================ #
class Player(ActorBase):
    def __init__(self):
        """A player sprite that can move and shoot.
        """        
        super().__init__()
        all_players.add(self)
        self.show(LAYER['player'])
        self.room: Room = self.getRoom()

        self.setImages("sprites/orbeeto/orbeeto.png", 64, 64, 5, 5)
        self.setRects(0, 0, 64, 64, 32, 32)

        self.pos = vec((608, WINHEIGHT // 2))
        self.center = vec(608, WINHEIGHT // 2)
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
        """        
        if direction == SOUTH:
            # mainroom.room.y -= 1
            # mainroom.layoutUpdate()
            # # self.pos.y -= WINHEIGHT
            # groupChangeRooms(SOUTH, all_portals, all_drops)
            pass

        elif direction == EAST:
            # mainroom.room.x += 1
            # mainroom.layoutUpdate()
            # # self.pos.x -= WINWIDTH
            # groupChangeRooms(EAST, all_portals, all_drops)
            pass

        elif direction == NORTH:
            # mainroom.room.y += 1
            # mainroom.layoutUpdate()
            # self.pos.y += WINHEIGHT
            # groupChangeRooms(NORTH, all_portals, all_drops)
            pass
        
        elif direction == WEST:
            # mainroom.room.x -= 1
            # mainroom.layoutUpdate()
            # self.pos.x += WINWIDTH
            # groupChangeRooms(WEST, all_portals, all_drops)
            pass

        killGroups(all_projs, all_explosions)

    def checkRoomChange(self):
        """Checks if the player should change rooms
        """        
        if self.pos.x <= 0:
            self.changeRoom(WEST)

        if self.pos.x >= WINWIDTH:
            self.changeRoom(EAST)

        if self.pos.y <= 0:
            self.changeRoom(NORTH)

        if self.pos.y >= WINHEIGHT:
            self.changeRoom(SOUTH)

# --------------------------------- Movement --------------------------------- #
    def movement(self):
        """When called once every frame, it allows the player to recive input from the user and move accordingly
        """        
        if self.canUpdate and self.visible:
            self.accel = self.getAccel()
            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        """Returns the acceleration that the player should undergo given specific conditions
        
        ### Returns
            - ``pygame.math.Vector2``: The acceleration value of the player
        """        
        finalAccel = vec(0, 0)
        if self.room.isScrollingX and self.room.isScrollingY:
            return finalAccel
        
        elif self.room.isScrollingX and not self.room.isScrollingY:
            if isInputHeld[K_w]:
                finalAccel.y -= self.cAccel
            if isInputHeld[K_s]:
                finalAccel.y += self.cAccel
            return finalAccel
        
        elif not self.room.isScrollingX and self.room.isScrollingY:
            if isInputHeld[K_a]:
                finalAccel.x -= self.cAccel
            if isInputHeld[K_d]:
                finalAccel.x += self.cAccel
            return finalAccel
        
        elif not self.room.isScrollingX and not self.room.isScrollingY:
            if isInputHeld[K_a]:
                finalAccel.x -= self.cAccel
            if isInputHeld[K_w]:
                finalAccel.y -= self.cAccel
            if isInputHeld[K_s]:
                finalAccel.y += self.cAccel
            if isInputHeld[K_d]:
                finalAccel.x += self.cAccel
            return finalAccel

    def shoot(self):
        """Shoots bullets
        """
        angle = rad(getAngleToMouse(self))

        velX = self.bulletVel * -sin(angle)
        velY = self.bulletVel * -cos(angle)

        if (isInputHeld[1] and 
            self.bulletType == PROJ_STD and 
            getTimeDiff(self.lastShot) >= self.gunCooldown and
            self.ammo > 0):

            OFFSET = vec((21, 30))
            all_projs.add(
                PlayerStdBullet(self,
                    self.pos.x - (OFFSET.x * cos(angle)) - (OFFSET.y * sin(angle)),
                    self.pos.y + (OFFSET.x * sin(angle)) - (OFFSET.y * cos(angle)),
                    velX, velY,
                ),
                
                PlayerStdBullet(self,
                    self.pos.x + (OFFSET.x * cos(angle)) - (OFFSET.y * sin(angle)),
                    self.pos.y - (OFFSET.x * sin(angle)) - (OFFSET.y * cos(angle)),
                    velX, velY,
                )
            )
            self.ammo -= 1
            self.lastShot = time.time()

        # Firing portals
        if keyReleased[3] % 2 == 0 and self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = False

        elif keyReleased[3] % 2 != 0 and not self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = True

        # Grappling hook
        # if keyReleased[2] % 2 != 0 and self.canGrapple:
        #     if self.grapple != None:
        #         self.grapple.shatter()
        #     self.grapple = GrappleBullet(self, self.pos.x, self.pos.y, velX, velY)
        #     self.canGrapple = False

        # elif keyReleased[2] % 2 == 0 and not self.canGrapple:
        #     if self.grapple != None:
        #         self.grapple.returning = True
        #     self.canGrapple = True

    def update(self):
        if self.canUpdate and self.visible:
            self.collideCheck(all_enemies, all_walls)

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

        pygame.draw.rect(screen, RED, self.hitbox, 3)
        
        if self.hp <= 0:
            self.kill()

# ------------------------------- Magic Methods ------------------------------ #
    def __str__(self):
        return f'Player at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\ncurrent bullet: {self.bulletType}\nxp: {self.xp}\nlevel: {self.level}\n'

    def __repr__(self):
        return f'Player({self.pos}, {self.vel}, {self.accel}, {self.cAccel}, {self.bulletType}, {self.xp}, {self.level})'


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
        
        self.isScrollingX = True
        self.isScrollingY = True

        self.canSwitchX = True
        self.canSwitchY = True

        self.player1: Player = Player()
        self.posCopy = self.player1.pos.copy()
        self.offset = vec(self.player1.pos.x - 608, self.player1.pos.y - WINHEIGHT // 2)
        self.lastRecenter = time.time()
        self.recentering = False

        # --------------------------------- Movement --------------------------------- #
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cAccel = self.player1.cAccel

    def accelMovement(self):
        """Calculates the room's acceleration, velocity, and position
        """        
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel
        self.pos += self.vel + self.player1.cAccel * self.accel

    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player"""        
        if self.canUpdate:
            self.accel = self.getAccel()
            self.accelMovement()

            if not (not self.isScrollingX and not self.isScrollingY):
                self.__spriteCollideCheck(self.player1, all_walls)
                for sprite in all_trinkets:
                    self.__spriteCollideCheck(sprite, all_players, all_walls)

            # ------------------ Teleporting player when room scrolling ------------------ #
            for portal in all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portalIn: Portal = portal
                    portalOut: Portal = getOtherPortal(portalIn)

                    if len(all_portals) == 2:
                        self.__teleportPlayer(portalIn, portalOut)

            self.__recenterPlayer()

            for sprite in self.sprites():
                sprite.movement()

    def __recenterPlayer(self) -> None:
        """Adjusts all sprites in the room so that the player is at the center
        """
        if self.isScrollingX and self.isScrollingY:
            if not self.recentering:
                if self.player1.pos != vec(608, WINHEIGHT // 2):
                    self.posCopy = self.player1.pos.copy()
                    self.offset = vec(self.posCopy.x - 608, self.posCopy.y - WINHEIGHT // 2)
                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.posCopy = sprite.pos.copy()

                    self.lastRecenter = time.time()
                    self.recentering = True

            if self.recentering:
                weight = getTimeDiff(self.lastRecenter)
                if weight <= 0.25:
                    self.player1.pos = cerp(self.posCopy, vec(608, WINHEIGHT // 2), weight * 4)
                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.pos = cerp(sprite.posCopy, sprite.posCopy - self.offset, weight * 4)
                else:
                    self.player1.pos = vec(608, WINHEIGHT // 2)
                    self.recentering = False
        
        elif self.isScrollingX and not self.isScrollingY:
            if not self.recentering:
                if self.player1.pos.x != 608:
                    self.posCopy = self.player1.pos.copy()
                    self.offset = vec(self.posCopy.x - 608, self.posCopy.y - WINHEIGHT // 2)

                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.posCopy = sprite.pos.copy()

                    self.lastRecenter = time.time()
                    self.recentering = True

            if self.recentering:
                weight = getTimeDiff(self.lastRecenter)
                if weight <= 0.25:
                    self.player1.pos.x = cerp(self.posCopy.x, 608, weight * 4)
                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.pos.x = cerp(sprite.posCopy.x, sprite.posCopy.x - self.offset.x, weight * 4)
                else:
                    self.player1.pos.x = 608
                    self.recentering = False

        elif not self.isScrollingX and self.isScrollingY:
            if not self.recentering:
                if self.player1.pos.y != WINHEIGHT // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offset = vec(self.posCopy.x - 608, self.posCopy.y - WINHEIGHT // 2)
                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.posCopy = sprite.pos.copy()

                    self.lastRecenter = time.time()
                    self.recentering = True

            if self.recentering:
                weight = getTimeDiff(self.lastRecenter)
                if weight <= 0.25:
                    self.player1.pos.y = cerp(self.posCopy.y, WINHEIGHT // 2, weight * 4)
                    for group in (self.sprites(), all_trinkets):
                        for sprite in group:
                            sprite.pos.y = cerp(sprite.posCopy.y, sprite.posCopy.y - self.offset.y, weight * 4)
                else:
                    self.player1.pos.y = WINHEIGHT // 2
                    self.recentering = False

        elif not self.isScrollingX and not self.isScrollingY:
            pass

    def __teleportPlayer(self, portalIn: Portal, portalOut: Portal):
        """Teleports the player when the room is scrolling.
        
        ### Arguments
            - portalIn (``Portal``): The portal the player is entering
            - portalOut (``Portal``): The portal the player is exiting
        """
        width = (portalOut.hitbox.width + self.player1.hitbox.width) // 2
        height = (portalOut.hitbox.height + self.player1.hitbox.height) // 2

        if self.isScrollingX and self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel = self.vel.rotate(180)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel = self.vel.rotate(90)

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y + distOffset
                    self.vel = self.vel.rotate(270)

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel = self.vel.rotate(270)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel = self.vel.rotate(180)

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.vel = self.vel.rotate(90)

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
                    self.vel = self.vel.rotate(270)

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.vel = self.vel.rotate(180)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel = self.vel.rotate(90)

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel = self.vel.rotate(90)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y + distOffset

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.vel = self.vel.rotate(270)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel = self.vel.rotate(180)

        elif self.isScrollingX and not self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.player1.vel = self.player1.vel.rotate(180)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel.x = self.player1.vel.y
                    self.player1.vel.y = self.player1.vel.x

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y + distOffset
                    self.vel.x = -self.player1.vel.y
                    self.player1.vel.y = -self.player1.vel.x

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.player1.vel.y = self.vel.x

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel.x = -self.vel.x

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.player1.vel.y = -self.vel.x

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
                    self.vel.x = -self.player1.vel.y
                    self.player1.vel.y = -self.player1.vel.x

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.player1.vel = self.player1.vel.rotate(180)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel.x = self.player1.vel.y
                    self.player1.vel.y = self.player1.vel.x

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.player1.vel = -self.vel.rotate(90)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y + distOffset

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.player1.vel = -self.vel.rotate(270)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.vel = self.vel.rotate(180)

        elif not self.isScrollingX and self.isScrollingY:
            if portalIn.facing == SOUTH:
                distOffset = copy.copy(self.player1.pos.x) - copy.copy(portalIn.pos.x)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel = self.vel.rotate(180)

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel.x = self.vel.y
                    self.vel.y = self.player1.vel.x

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y + distOffset
                    self.player1.vel.x = -self.vel.y
                    self.vel.y = -self.player1.vel.x

            if portalIn.facing == EAST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel.y = self.player1.vel.x

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel = self.player1.vel.rotate(180)
                    self.vel.y = -self.vel.y

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.player1.vel.x = -self.player1.vel.x
                    self.vel.y = self.player1.vel.x

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
                    self.player1.vel.x = -self.vel.y
                    self.vel.y = 0

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.vel = self.vel.rotate(180)

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel.x = self.vel.y
                    self.vel.y = 0

            if portalIn.facing == WEST:
                distOffset = copy.copy(self.player1.pos.y) - copy.copy(portalIn.pos.y)
                if portalOut.facing == SOUTH:
                    self.player1.pos.x = portalOut.pos.x + distOffset
                    self.player1.pos.y = portalOut.pos.y + height
                    self.vel.y = self.player1.vel.x

                if portalOut.facing == EAST:
                    self.player1.pos.x = portalOut.pos.x + width
                    self.player1.pos.y = portalOut.pos.y + distOffset

                if portalOut.facing == NORTH:
                    self.player1.pos.x = portalOut.pos.x - distOffset
                    self.player1.pos.y = portalOut.pos.y - height
                    self.vel.y = self.player1.vel.x

                if portalOut.facing == WEST:
                    self.player1.pos.x = portalOut.pos.x - width
                    self.player1.pos.y = portalOut.pos.y - distOffset
                    self.player1.vel.x = -self.player1.vel.x
                    self.vel.y = -self.vel.y

        elif not self.isScrollingX and not self.isScrollingY:
            pass

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

            if collideSideCheck(instig, sprite) == SOUTH and (instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self.vel.y = 0
                if not self.isScrollingX and self.isScrollingY:
                    instig.pos.y = sprite.pos.y + height

            if collideSideCheck(instig, sprite) == EAST and (instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self.vel.x = 0
                if self.isScrollingX and not self.isScrollingY:
                    instig.pos.x = sprite.pos.x + width

            if collideSideCheck(instig, sprite) == NORTH and (instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self.vel.y = 0
                if not self.isScrollingX and self.isScrollingY:
                    instig.pos.y = sprite.pos.y - height

            if collideSideCheck(instig, sprite) == WEST and (instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self.vel.x = 0
                if self.isScrollingX and not self.isScrollingY:
                    instig.pos.x = sprite.pos.x - width

    def __spriteBlockFromSide(self, instig: ActorBase, sprite: ActorBase):
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if collideSideCheck(instig, sprite) == SOUTH and (instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if collideSideCheck(instig, sprite) == EAST and (instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if collideSideCheck(instig, sprite) == NORTH and (instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if collideSideCheck(instig, sprite) == WEST and (instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    def __setRoomBorders(self):
        self.borderSouth = RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.borderNorth = RoomBorder(0, 0, self.size.x // 16, 1)

        self.add(self.borderSouth, self.borderNorth)

    def getAccel(self) -> pygame.math.Vector2:
        finalAccel = vec(0, 0)
        if self.isScrollingX and self.isScrollingY:
            finalAccel = vec(0, 0)
            if isInputHeld[K_a]:
                finalAccel.x += self.player1.cAccel
            if isInputHeld[K_w]:
                finalAccel.y += self.player1.cAccel
            if isInputHeld[K_s]:
                finalAccel.y -= self.player1.cAccel
            if isInputHeld[K_d]:
                finalAccel.x -= self.player1.cAccel
            return finalAccel
        
        elif self.isScrollingX and not self.isScrollingY:
            finalAccel = vec(0, 0)
            if isInputHeld[K_a]:
                finalAccel.x += self.player1.cAccel
            if isInputHeld[K_d]:
                finalAccel.x -= self.player1.cAccel
            return finalAccel
        
        elif not self.isScrollingX and self.isScrollingY:
            finalAccel = vec(0, 0)
            if isInputHeld[K_w]:
                finalAccel.y += self.player1.cAccel
            if isInputHeld[K_s]:
                finalAccel.y -= self.player1.cAccel
            return finalAccel
        
        elif not self.isScrollingX and not self.isScrollingY:
            finalAccel = vec(0, 0)
            return finalAccel

    def layoutUpdate(self) -> None:
        """Updates the layout of the room
        """        
        for sprite in self.sprites():
            sprite.kill()

        container: EntityContainer
        for container in all_containers:
            container.hideEnemies()
        
        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            self.isScrollingX = True
            self.isScrollingY = True
            
            self.__setRoomBorders()
            self.add(
                Wall(0, 0, 8, 8),
                Wall(0, 37, 40, 8),
                Wall(72, 0, 8, 8),
                Wall(72, 37, 8, 8),
            )
            
            try:
                container: EntityContainer = next(c for c in all_containers if c.room == self.room)
                container.showEnemies()

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        # Box(0, 500, 500)
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

    def hideEnemies(self):
        """Hides all of the enemies in the container"""
        for sprite in self.sprites():
            sprite.hide()

    def showEnemies(self):
        for sprite in self.sprites():
            sprite.show(LAYER['enemy'])


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
        self.images = self.spritesheet.get_images(64, 64, 61)
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
        self.images = self.spritesheet.get_images(64, 64, 61)
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
    def __init__(self, owner: Player, posX: float, posY: float, item_held: str):
        """A menu slot that shows the collected amount of a specific item
        
        ### Arguments
            - owner (``player``): The owner of the inventory to whom the menu slot belongs to
            - posX (``float``): The x-position to spawn at
            - posY (``float``): The y-position to spawn at
            - item_held (``str``): The item the menu slot will hold. Items are chosen from ``MATERIALS`` dictionary.
            - num_frames (``int``): The number of animation frames the item has
            - frame_offset (``int``): Where the first frame of the animation begins. (0 = first image of sprite sheet)
        """
        super().__init__()
        all_slots.add(self)
        self.owner = owner

        self.pos = vec((posX, posY))
        self.start_pos = vec((posX, posY))
        self.holding = item_held
        self.count = 0

        self.menusheet = Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.itemsheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.menu_imgs = self.menusheet.get_images(64, 64, 1)
        
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
            return self.itemsheet.get_images(32, 32, 1, 0)
        elif self.holding == MAT[1]:
            return self.itemsheet.get_images(32, 32, 1, 1)
        else:
            return self.itemsheet.get_images(32, 32, 1, 0)

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
mainroom.layoutUpdate()


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