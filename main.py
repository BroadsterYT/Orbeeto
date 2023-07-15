import pygame
from pygame.locals import *

pygame.init()

import sys, math, time, copy
import random as rand

from math import sin, cos, radians, degrees, floor, pi

from init import can_update, keyReleased
from calculations import *
from class_bases import *
from constants import *
from groups import *
from spritesheet import *
from ui_actors import *

# Aliases
spriteGroup = pygame.sprite.Group
rad = radians
deg = degrees

clock = pygame.time.Clock()

screenSize = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED)
pygame.display.set_caption('Orbeeto')


def objectAccel(sprite: pygame.sprite.Sprite):
    """Defines the relationship between acceleration, velocity, and position (and time, when called once every frame)

    Args:
        sprite (pygame.sprite.Sprite): The sprite that should follow the acceleration logic
    """    
    sprite.accel.x += sprite.vel.x * FRIC
    sprite.accel.y += sprite.vel.y * FRIC
    sprite.vel += sprite.accel * dt
    sprite.pos += sprite.vel + sprite.ACCELC * sprite.accel


# ============================================================================ #
#                                 Player Class                                 #
# ============================================================================ #
class PlayerBase(ActorBase):
    def __init__(self):
        """The base class for all player objects. It contains parameters and methods to gain better control over player objects."""        
        super().__init__()
        self.room = vec((0, 0))

        self.pos = vec((WIN_WIDTH / 2, WIN_HEIGHT / 2))
        self.ACCELC = 0.52

        #-------------------- Game stats & UI --------------------#
        self.xp = 0
        self.level = 0
        self.max_hp = 50
        self.hp = 50
        self.max_attack = 10
        self.attack = 10
        self.max_defense = 10
        self.defense = 15
        self.bulletVel = 12
        self.gun_cooldown = 0.12
        self.hitTime_charge = 1200
        self.hitTime = 0
        
        self.lastHit = time.time()
        self.last_shot = time.time()

        self.updateMaxStats()

        self.menu = InventoryMenu(self)
        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)

        self.inventory = {}
        for item in MAT.values():
            self.inventory.update({item: 0})

    def changeRoom(self, direction: str) -> None:
        hideCurrentEnemies()

        if direction == SOUTH:
            mainroom.room.y -= 1
            mainroom.layoutUpdate()
            self.pos.y -= WIN_HEIGHT
            groupChangeRooms(SOUTH, all_portals, all_drops)

        elif direction == EAST:
            mainroom.room.x += 1
            mainroom.layoutUpdate()
            self.pos.x -= WIN_WIDTH
            groupChangeRooms(EAST, all_portals, all_drops)

        elif direction == NORTH:
            mainroom.room.y += 1
            mainroom.layoutUpdate()
            self.pos.y += WIN_HEIGHT
            groupChangeRooms(NORTH, all_portals, all_drops)
        
        elif direction == WEST:
            mainroom.room.x -= 1
            mainroom.layoutUpdate()

            self.pos.x += WIN_WIDTH
            groupChangeRooms(WEST, all_portals, all_drops)

        killGroups(all_projs, all_explosions)

    def checkRoomChange(self):
        if self.pos.x <= 0:
            self.changeRoom(WEST)

        if self.pos.x >= WIN_WIDTH:
            self.changeRoom(EAST)

        if self.pos.y <= 0:
            self.changeRoom(NORTH)

        if self.pos.y >= WIN_HEIGHT:
            self.changeRoom(SOUTH)

    def teleport(self, portal_in):
        portalOut = getOtherPortal(portal_in)
        velCopy = self.vel.copy()

        width = portalOut.hitbox.height // 2
        height = portalOut.hitbox.width // 2

        if portal_in.facing == SOUTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = self.vel.rotate(180)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = self.vel.rotate(90)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)

        if portal_in.facing == EAST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, -velCopy.x)
                
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - width
                self.vel = vec(-velCopy.y, velCopy.x)

            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset

        if portal_in.facing == NORTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)

        if portal_in.facing == WEST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(velCopy.y, -velCopy.x)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

    def loadXpReq(self):
        """Returns a list containing the amount of xp needed to reach each level
        
        ### Returns
            - ``list``: A list containing the amount of xp needed to reach each level
        """        
        xpToReach = []
        xpRequired = []

        for a in range(250):
            if a < 125:
                value = math.floor(17.84 * a)
            else:
                value = math.floor(pow(1.061726202, a))
            xpToReach.append(value)
        for b in range(250):
            countup = 0
            total = 0
            while countup <= b:
                total = total + xpToReach[countup]
                countup += 1
            xpRequired.append(total)

        del xpToReach
        return xpRequired

    def updateMaxStats(self):
        """Updates all of the player's max stats."""        
        self.max_hp = floor(50 * pow(1.009290219, self.level))
        self.max_attack = floor(10 * pow(1.019580042, self.level))
        self.max_defense = floor(15 * pow(1.016098331, self.level))

    def updateLevel(self):
        """Updates the current level of the player."""        
        xpRequired = self.loadXpReq()
        for i in range(250):
            if self.xp < xpRequired[i + 1]:
                self.level = i
                break
            if self.xp > xpRequired[249]:
                self.level = 249
                break
        
        self.updateMaxStats()


class Player(PlayerBase):
    def __init__(self):
        """A player sprite that can move and shoot."""        
        super().__init__()
        all_players.add(self)
        self.show(LAYER['player_layer'])

        self.setImages("sprites/orbeeto/orbeeto.png", 64, 64, 5, 5)
        self.setRects(0, 0, 64, 64, 32, 32)

        self.bulletType = PROJ_STD
        
        self.canPortal = False
        self.canGrapple = True

        self.grapple = None

    def movement(self):
        """When called once every frame, it allows the player to recive input from the user and move accordingly"""        
        self.accel = vec(0, 0)
        if self.visible:
            if self.grapple == None:
                if isInputHeld[K_a]:
                    self.accel.x = -self.ACCELC * dt
                if isInputHeld[K_d]:
                    self.accel.x = self.ACCELC * dt
                if isInputHeld[K_s]:
                    self.accel.y = self.ACCELC * dt
                if isInputHeld[K_w]:
                    self.accel.y = -self.ACCELC * dt

            elif self.grapple != None:
                if isInputHeld[K_a]:
                    self.accel.x = -self.ACCELC * dt
                if isInputHeld[K_d]:
                    self.accel.x = self.ACCELC * dt
                if isInputHeld[K_s]:
                    self.accel.y = self.ACCELC * dt
                if isInputHeld[K_w]:
                    self.accel.y = -self.ACCELC * dt
                
                if self.grapple.returning and self.grapple.grappledTo in all_walls:
                    self.accel = vec((self.ACCELC * 3) * -sin(getAngleToSprite(self, self.grapple)) * dt, (self.ACCELC * 3) * -cos(getAngleToSprite(self, self.grapple)) * dt)

            self.accelMovement(dt)

    def shoot(self):
        """Shoots a bullet"""
        angle_to_mouse = rad(getAngleToMouse(self))

        velX = self.bulletVel * -sin(angle_to_mouse)
        velY = self.bulletVel * -cos(angle_to_mouse)

        if isInputHeld[1] and self.bulletType == PROJ_STD and getTimeDiff(self.last_shot) >= self.gun_cooldown:
            OFFSET = vec((21, 30))
            all_projs.add(
                PlayerStdBullet(self,
                    self.pos.x - (OFFSET.x * cos(angle_to_mouse)) - (OFFSET.y * sin(angle_to_mouse)),
                    self.pos.y + (OFFSET.x * sin(angle_to_mouse)) - (OFFSET.y * cos(angle_to_mouse)),
                    velX, velY
                ),
                
                PlayerStdBullet(self,
                    self.pos.x + (OFFSET.x * cos(angle_to_mouse)) - (OFFSET.y * sin(angle_to_mouse)),
                    self.pos.y - (OFFSET.x * sin(angle_to_mouse)) - (OFFSET.y * cos(angle_to_mouse)),
                    velX, velY
                )
            )
            self.last_shot = time.time()

        # Firing portals
        if keyReleased[3] % 2 == 0 and self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = False

        elif keyReleased[3] % 2 != 0 and not self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.canPortal = True

        # Grappling hook
        if keyReleased[2] % 2 != 0 and self.canGrapple:
            if self.grapple != None:
                self.grapple.shatter()
            self.grapple = GrappleBullet(self, self.pos.x, self.pos.y, velX, velY)
            self.canGrapple = False

        elif keyReleased[2] % 2 == 0 and not self.canGrapple:
            if self.grapple != None:
                self.grapple.returning = True
            self.canGrapple = True

    def update(self):
        if can_update and self.visible:
            collideCheck(self, all_enemies, all_movable, all_walls)

            self.movement()
            self.shoot()
            self.checkRoomChange()

            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if isInputHeld[1]:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                else: # Idle animation
                    self.index = 0
                
                self.lastFrame = time.time()
            self.rotateImage(getAngleToMouse(self))

            for portal in all_portals:
                if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                    self.teleport(portal)

            # Dodge charge up
            if self.hitTime < self.hitTime_charge:
                self.hitTime += 1

        self.menu.update()
        
        if self.hp <= 0:
            self.kill()


# ============================================================================ #
#                                 Enemy Classes                                #
# ============================================================================ #
class EnemyBase(ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It contains parameters and methods to gain better control over enemy objects."""    
        super().__init__()
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.isGrappled = False

        self.is_shooting = False

        #-------------------- In-game Stats --------------------#
        self.max_hp = None
        self.hp = None
        self.max_attack = None
        self.attack = None
        self.max_defense = None
        self.defense = None
        self.xp_worth = None

        self.healthBar = HealthBar(self)

    def awardXp(self):
        for a_player in all_players:
            a_player.xp += self.xp_worth
            a_player.updateLevel()
            a_player.updateMaxStats()

    def dropItems(self, table_index):
        drops = LTDROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)
        
        for item in drops[row][column]:
            ItemDrop(self, item)


class StandardGrunt(EnemyBase):
    def __init__(self, posX: int, posY: int):
        """A simple enemy that moves to random locations and shoots at players.
        
        ### Arguments
            - posX (``int``): The x-position to spawn at
            - posY (``int``): The y-position to spawn at
        """         
        super().__init__()
        self.show(LAYER['enemy_layer'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WIN_WIDTH - 64), rand.randint(64, WIN_HEIGHT - 64))

        self.setImages("sprites/enemies/standard_grunt.png", 64, 64, 5, 5, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 15, 10, 10, 25, 0.4)

    def movement(self, canShoot: bool):
        if self.hp > 0:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, WIN_WIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, WIN_HEIGHT - self.image.get_height() - 64)
                self.lastRelocate = time.time()

            if self.pos.x != (self.rand_pos.x) or self.pos.y != (self.rand_pos.y):
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.ACCELC
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.ACCELC
                else:
                    self.accel.x = 0

                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.ACCELC
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.ACCELC
                else:
                    self.accel.y = 0
            
            if canShoot:
                self.shoot(getClosestPlayer(self), 6, rand.uniform(0.4, 0.9))

            self.accelMovement(dt)

    def shoot(self, target, vel, shoot_time):
        if getTimeDiff(self.lastShot) > shoot_time:
            self.is_shooting = True
            try:
                angle_to_target = getAngleToSprite(self, target)
            except:
                angle_to_target = 0

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            all_projs.add(EnemyStdBullet(self, self.pos.x - (21 * cos(rad(angle_to_target))) - (30 * sin(rad(angle_to_target))), self.pos.y + (21 * sin(rad(angle_to_target))) - (30 * cos(rad(angle_to_target))), vel_x, vel_y))
            self.lastShot = time.time()

    def update(self):
        if can_update and self.visible and self.hp > 0:
            collideCheck(self, all_players, all_walls)
            self.movement(True)
            
            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.is_shooting == True:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                        self.is_shooting = False
                self.lastFrame = time.time()
            self.rotateImage(getAngleToSprite(self, getClosestPlayer(self)))

        if self.hp <= 0:
            self.dropItems(0)
            self.awardXp()
            self.kill()


class OctoGrunt(EnemyBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show(LAYER['enemy_layer'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WIN_WIDTH - 64), rand.randint(64, WIN_HEIGHT - 64))

        self.setImages("sprites/enemies/octogrunt.png", 64, 64, 1, 1, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 44, 10, 10, 45, 0.4)

    def movement(self, canShoot):
        if can_update and self.visible:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(0, WIN_WIDTH)
                self.rand_pos.y = rand.randint(0, WIN_HEIGHT)
                self.lastRelocate = time.time()

            if self.pos.x != self.rand_pos.x or self.pos.y != self.rand_pos.y:
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.ACCELC
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.ACCELC
                else:
                    self.accel.x = 0

                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.ACCELC
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.ACCELC
                else:
                    self.accel.y = 0
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 3, 1)

            self.accelMovement(dt)

    def shoot(self, target, vel, shoot_time):
        if getTimeDiff(self.lastShot) > shoot_time:
            self.is_shooting = True
            angle_to_target = getAngleToSprite(self, target)

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            OFFSET = 21

            all_projs.add(
                EnemyStdBullet(self, self.pos.x - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel_x, vel_y),
                EnemyStdBullet(self, self.pos.x + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))), -vel_x, -vel_y),

                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90))),
                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 90)), -vel * -cos(rad(angle_to_target + 90))),

                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 45)), vel * -cos(rad(angle_to_target + 45))),
                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 45)), -vel * -cos(rad(angle_to_target + 45))),

                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target - 45)), vel * -cos(rad(angle_to_target - 45))),
                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target - 45)), -vel * -cos(rad(angle_to_target - 45))),
            )

            self.lastShot = time.time()

    def update(self):
        if can_update and self.visible and self.hp > 0:
            collideCheck(self, all_players, all_walls)
            self.movement(True)

            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.is_shooting:
                    self.index += 0
                    if self.index > 4:
                        self.index = 0
                    self.is_shooting = False
                self.lastFrame = time.time()

            self.image = self.images[self.index]
            self.original_image = self.original_images[self.index]

            # Animation rotation
            self.image = pygame.transform.rotate(self.original_image, int(getAngleToSprite(self, getClosestPlayer(self))))
            self.rect = self.image.get_rect(center = self.pos)

        if self.hp <= 0:
            self.dropItems(1)
            self.awardXp()
            self.kill()


# ============================================================================ #
#                             Interactible Classes                             #
# ============================================================================ #
class Box(ActorBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show(LAYER['movable_layer'])
        all_movable.add(self)

        self.pos = vec((posX, posY))
        self.ACCELC = 0.4
        
        self.setImages("sprites/orbeeto/orbeeto.png", 64, 64, 5, 1, 0, 0)
        self.setRects(0, 0, 64, 64, 64, 64, True)

    def movement(self):
        self.accel = vec(0, 0)
        if can_update and self.visible:
            for a_player in all_players:
                if self.hitbox.colliderect(a_player.rect):
                    if collideSideCheck(self, a_player) == SOUTH:
                        self.accel.y = -self.ACCELC * dt
                    if collideSideCheck(self, a_player) == EAST:
                        self.accel.x = -self.ACCELC * dt
                    if collideSideCheck(self, a_player) == NORTH:
                        self.accel.y = self.ACCELC * dt
                    if collideSideCheck(self, a_player) == WEST:
                        self.accel.x = self.ACCELC * dt

            self.accelMovement(dt)

    def update(self):
        self.movement()


class ItemDrop(DropBase):
    def __init__(self, dropped_from, item_name):
        """An item or material dropped by an enemey that is able to be collected
        
        ### Arguments
            - dropped_from (``pygame.sprite.Sprite``): The enemy that the item was dropped from
            - item_name (``str``): The item to drop
            - item_frame_start (``int``): The index of the first frame to display from the item drop spritesheet (0 = the first image).
            - image_count (``int``): The number of frames to use
        """        
        super().__init__()
        self.show(LAYER['drops_layer'])
        all_drops.add(self)
        self.droppedFrom = dropped_from
        self.mat = item_name

        self.start_time = time.time()
        self.pos = vec(self.droppedFrom.pos.x, self.droppedFrom.pos.y)
        self.randAccel = getRandComponents(self.ACCELC)
        
        self.spritesheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.index = 0

        if self.mat == MAT[0]:
            self.original_images = self.spritesheet.get_images(32, 32, 1, 0)
            self.images = self.spritesheet.get_images(32, 32, 1, 0)
        elif self.mat == MAT[1]:
            self.original_images = self.spritesheet.get_images(32, 32, 1, 1)
            self.images = self.spritesheet.get_images(32, 32, 1, 1)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        self.accel = vec(0, 0)
        if self.visible:
            time_since_start = getTimeDiff(self.start_time)
            if time_since_start <= 0.1:
                self.accel.x = self.randAccel.x
                self.accel.y = self.randAccel.y
            
            if time_since_start <= 10:
                self.original_image = self.original_images[self.index]
                self.image = pygame.transform.rotate(self.original_image, int(degrees(sin(self.period_mult * pi * time_since_start) * (1 / time_since_start))))
                self.rect = self.image.get_rect(center = self.rect.center)
            
            # objectAccel(self)
            self.accelMovement(dt)
        
        # self.rect.center = self.pos
        # self.hitbox.center = self.pos

    def update(self):
        collideCheck(self, all_walls)

        self.movement()

        for a_player in all_players:
            if self.hitbox.colliderect(a_player):
                a_player.inventory[self.mat] += 1
                a_player.menu.updateMenuSlots()
                self.kill()


# ============================================================================ #
#                            Projectile Class Bases                            #
# ============================================================================ #
class BulletBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.ricCount = 1

    def land(self):
        self.ricCount -= 1

        if self.ricCount <= 0:
            all_explosions.add(ProjExplode(self))
            self.kill()
        else:
            # Cause the bullet to ricochet
            pass

    def teleport(self, portal_in):
        for portal in all_portals:
            if portal != portal_in:
                portalOut = portal

        velCopy = self.vel.copy()

        width = portalOut.hitbox.height // 4
        height = portalOut.hitbox.width // 4

        if portal_in.facing == SOUTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)

        if portal_in.facing == EAST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, -velCopy.x)
                
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - width
                self.vel = vec(-velCopy.y, velCopy.x)

            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset

        if portal_in.facing == NORTH:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)

        if portal_in.facing == WEST:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

            if portalOut.facing == SOUTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == EAST:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
            
            if portalOut.facing == NORTH:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(velCopy.y, -velCopy.x)
            
            if portalOut.facing == WEST:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

    def projCollide(self, spriteGroup, canHurt):
        """Destroys a given projectile upon a collision and renders an explosion

        ### Arguments
            - entityGroup (``pygame.sprite.Group``): The group of the entity the projectile is colliding with
            - proj (``pygame.sprite.Sprite``): The projectile involved in the collision
            - canHurt (``bool``): Should the projectile calculate damage upon impact?
        """    
        for colliding_entity in spriteGroup:
            if not self.hitbox.colliderect(colliding_entity.hitbox):
                continue
            
            if not colliding_entity.visible:
                continue

            if canHurt:
                damage = calculateDamage(self.shotFrom, colliding_entity, self)
                if spriteGroup == all_enemies:
                    if rand.randint(1, 20) == 1:
                        colliding_entity.hp -= damage * 3
                        if damage > 0:
                            all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, 3 * damage))
                    else:
                        colliding_entity.hp -= damage
                        if damage > 0:
                            all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, damage))
                    self.land()

                elif spriteGroup != all_enemies:
                    colliding_entity.hp -= damage
                    if damage > 0:
                        all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, damage))
                    if hasattr(colliding_entity, 'hitTime'):
                        colliding_entity.hitTime = 0
                        colliding_entity.lastHit = time.time()
                    self.land()

            elif not canHurt:
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                        return
                    
                    elif len(all_portals) < 2:
                        self.land()
                        return

                else:
                    self.land()


class PlayerBulletBase(BulletBase):
    def __init__(self):
        super().__init__()

    def bindProj(self):
        if can_update:
            if (
                self.pos.x < WIN_WIDTH and 
                self.pos.x > 0 and
                self.pos.y < WIN_HEIGHT and 
                self.pos.y > 0
            ):
                self.movement()
            else:
                self.kill()

            self.projCollide(all_enemies, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)


class EnemyBulletBase(BulletBase):
    def __init__(self):
        super().__init__()

    def bindProj(self):
        if can_update:
            if (
                self.pos.x < WIN_WIDTH and 
                self.pos.x > 0 and
                self.pos.y < WIN_HEIGHT and 
                self.pos.y > 0
            ):
                self.movement()
            else:
                self.kill()

            self.projCollide(all_players, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)


# ============================================================================ #
#                              Projectile Classes                              #
# ============================================================================ #
class PortalBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY): 
        super().__init__()
        self.show(LAYER['proj_layer'])
        
        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.hitbox_adjust = vec(0, 0)
        self.damage = PROJ_DMG[PROJ_PORTAL]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 5, 4)
        self.setRects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def projCollide(self, spriteGroup, canHurt):
        for colliding_entity in spriteGroup:
            if not self.hitbox.colliderect(colliding_entity.hitbox):
                continue
            
            if not colliding_entity.visible:
                continue

            if canHurt:
                if spriteGroup == all_enemies:
                    if rand.randint(1, 20) == 1:
                        colliding_entity.hp -= (calculateDamage(self.shotFrom, colliding_entity, self)) * 3
                        all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, 3 * calculateDamage(self.shotFrom, colliding_entity, self)))
                    else:
                        colliding_entity.hp -= calculateDamage(self.shotFrom, colliding_entity, self)
                        all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(self.shotFrom, colliding_entity, self)))
                    self.land()

                elif spriteGroup != all_enemies:
                    colliding_entity.hp -= calculateDamage(self.shotFrom, colliding_entity, self)
                    all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(self.shotFrom, colliding_entity, self)))
                    if hasattr(colliding_entity, 'hitTime'):
                        colliding_entity.hitTime = 0
                        colliding_entity.lastHit = time.time()
                    self.land()

            elif not canHurt:
                # If the projectile hits a portal
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                        return
                    
                    elif len(all_portals) < 2:
                        self.land()
                        return

                elif spriteGroup == all_walls:
                    side = wallSideCheck(colliding_entity, self)
                    if side == SOUTH:
                        all_portals.add(Portal(self.pos.x, colliding_entity.pos.y + (colliding_entity.image.get_height() // 2), side))
                        portalCountCheck()
                    if side == NORTH:
                        all_portals.add(Portal(self.pos.x, colliding_entity.pos.y - (colliding_entity.image.get_height() // 2), side))
                        portalCountCheck()
                    if side == EAST:
                        all_portals.add(Portal(colliding_entity.pos.x + (colliding_entity.image.get_width() // 2), self.pos.y, side))
                        portalCountCheck()
                    if side == WEST:
                        all_portals.add(Portal(colliding_entity.pos.x - (colliding_entity.image.get_width() // 2), self.pos.y, side))
                        portalCountCheck()
                    self.land()
                
                else:
                    self.land()

    def bindProj(self):
        if (
            self.pos.x < WIN_WIDTH and 
            self.pos.x > 0 and
            self.pos.y < WIN_HEIGHT and 
            self.pos.y > 0
        ):
            self.movement()
        else:
            self.kill()

        self.projCollide(all_enemies, True)
        self.projCollide(all_walls, False)
        self.projCollide(all_portals, False)

    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        if getTimeDiff(self.lastFrame) > ANIMTIME:
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.lastFrame = time.time()
        
        self.rotateImage(int(getVecAngle(self.vel.x, self.vel.y)))
        self.bindProj()


class GrappleBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYER['grapple'])
        all_projs.add(self)

        self.shotFrom: Player = shotFrom
        self.damage = PROJ_DMG[PROJ_GRAPPLE]

        self.isHooked = False
        self.grappledTo: pygame.sprite.Sprite = None
        
        self.returning = False
        self.hasExitedPortal = False

        self.chain1: Beam = Beam(self.shotFrom, self)
        self.chain2: Beam = None

        self.canTp = True
        self.tpPoints = []

        self.enterPoint: InvisObj = None; self.enterPointFace = None
        self.exitPoint: InvisObj = None; self.exitPointFace = None

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.accel = vec(0, 0)
        self.ACCELC = 0.7

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 2, 9)
        self.setRects(0, 0, 32, 32, 16, 16)
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def land(self, grappledTo):
        self.isHooked = True
        self.grappledTo = grappledTo
        if self.grappledTo != None:
            self.grappledTo.isGrappled = True

    def shatter(self):
        """Destroys the grappling hook"""   
        self.shotFrom.grapple = None
        self.returning = False

        self.chain1.kill()
        if isinstance(self.chain2, Beam):
            self.chain2.kill()

        if isinstance(self.enterPoint, InvisObj):
            self.enterPoint.kill()
        if isinstance(self.exitPoint, InvisObj):
            self.exitPoint.kill()

        self.kill()

    def projCollide(self, spriteGroup, canHurt):
        for colliding_entity in spriteGroup:
            if not self.hitbox.colliderect(colliding_entity.hitbox):
                continue
            
            if not colliding_entity.visible:
                continue

            if canHurt:
                if spriteGroup == all_enemies:
                    if rand.randint(1, 20) == 1:
                        colliding_entity.hp -= (calculateDamage(self.shotFrom, colliding_entity, self)) * 3
                        all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, 3 * calculateDamage(self.shotFrom, colliding_entity, self)))
                    else:
                        colliding_entity.hp -= calculateDamage(self.shotFrom, colliding_entity, self)
                        all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(self.shotFrom, colliding_entity, self)))
                    self.land(colliding_entity)

                elif spriteGroup != all_enemies:
                    colliding_entity.hp -= calculateDamage(self.shotFrom, colliding_entity, self)
                    all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(self.shotFrom, colliding_entity, self)))
                    if hasattr(colliding_entity, 'hitTime'):
                        colliding_entity.hitTime = 0
                        colliding_entity.lastHit = time.time()
                    self.land(colliding_entity)

            elif not canHurt:
                if spriteGroup == all_portals:
                    if len(all_portals) == 2 and self.canTp:
                        self.tpPoints.append(copy.copy(self.pos))
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.canTp = False
                                self.tpPoints.append(copy.copy(self.pos))
                                
                                # Creating invisible objects at teleport points so grapple can return through portals
                                otherPortal: Portal = getOtherPortal(portal)
                                self.enterPointFace = portal.facing
                                self.exitPointFace = otherPortal.facing

                                ret1Pos: pygame.math.Vector2 = copy.copy(self.tpPoints[0])
                                ret2Pos: pygame.math.Vector2 = copy.copy(self.tpPoints[1])
                                self.enterPoint = InvisObj(ret1Pos.x, ret1Pos.y, 8, 8)
                                self.exitPoint = InvisObj(ret2Pos.x, ret2Pos.y, 8, 8)
                                
                                # Correcting chains
                                self.chain1.kill()
                                self.chain1: Beam = Beam(self.shotFrom, self.enterPoint)
                                self.chain2: Beam = Beam(self.exitPoint, self)
                        return
                    
                elif not self.canTp and spriteGroup == all_portals:
                    pass

                else:
                    self.land(colliding_entity)

    def bindProj(self):
        if can_update:
            self.movement()
            if (
                self.pos.x > WIN_WIDTH or 
                self.pos.x < 0 or
                self.pos.y > WIN_HEIGHT or 
                self.pos.y < 0
            ):
                self.land(None)

            if not self.isHooked:
                self.projCollide(all_enemies, True)
                self.projCollide(all_walls, False)
                self.projCollide(all_drops, False)
                self.projCollide(all_portals, False)

    def sendBack(self):
        """Sends the grappling hook back to the player"""
        if len(self.tpPoints) == 0:  
            angle = getAngleToSprite(self, self.shotFrom)
            self.accel.x = self.ACCELC * -sin(rad(angle))
            self.accel.y = self.ACCELC * -cos(rad(angle))

            if self.hitbox.colliderect(self.shotFrom.rect):
                self.shatter()

        if len(self.tpPoints) > 0:
            if not self.hasExitedPortal:
                angle = getAngleToSprite(self, self.exitPoint)
                self.accel.x = self.ACCELC * -sin(rad(angle))
                self.accel.y = self.ACCELC * -cos(rad(angle))

                if self.hitbox.colliderect(self.exitPoint.hitbox):
                    self.pos = self.enterPoint.pos
                    self.vel = getTpVel(self.exitPointFace, self.enterPointFace, self)
                    self.hasExitedPortal = True
                    self.chain2.kill()
            
            elif self.hasExitedPortal:
                angle = getAngleToSprite(self, self.shotFrom)
                self.accel.x = self.ACCELC * -sin(rad(angle))
                self.accel.y = self.ACCELC * -cos(rad(angle))
                if self.hitbox.colliderect(self.shotFrom.rect):
                    self.shatter()

        objectAccel(self)

    def movement(self):
        if not self.returning:
            if not self.isHooked:
                self.pos.x += self.vel.x * dt
                self.pos.y += self.vel.y * dt

            else:
                if self.grappledTo != None and self.grappledTo not in all_walls:
                    self.pos.x = self.grappledTo.pos.x
                    self.pos.y = self.grappledTo.pos.y
                
                elif self.grappledTo != None and self.grappledTo in all_walls:
                    side = wallSideCheck(self.grappledTo, self)
                    if side == SOUTH:
                        self.pos.x = self.pos.x
                        self.pos.y = self.grappledTo.pos.y + (self.grappledTo.rect.height // 2)
                    if side == NORTH:
                        self.pos.x = self.pos.x
                        self.pos.y = self.grappledTo.pos.y - (self.grappledTo.rect.height // 2)
                    if side == EAST:
                        self.pos.x = self.grappledTo.pos.x + (self.grappledTo.rect.width // 2)
                        self.pos.y = self.pos.y
                    if side == WEST:
                        self.pos.x = self.grappledTo.pos.x - (self.grappledTo.rect.width // 2)
                        self.pos.y = self.pos.y
                
                else:
                    self.pos = self.pos

        if self.returning:
            if self.grappledTo == None:
                self.sendBack()
            
            # Grapple will move if attached to an enemy or item
            if self.grappledTo != None and self.grappledTo not in all_walls:
                self.sendBack()
                self.grappledTo.pos.x = self.pos.x
                self.grappledTo.pos.y = self.pos.y

            if self.grappledTo != None and self.grappledTo in all_walls:
                if self.shotFrom.hitbox.colliderect(self.hitbox):
                    self.shatter()
                for wall in all_walls:
                    if self.shotFrom.hitbox.colliderect(wall.hitbox):
                        self.shatter()

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        if not self.isHooked and not self.returning:
            self.index = 0
            self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
        else:
            self.index = 1
            self.rotateImage(getAngleToSprite(self, self.shotFrom) + 180)
        
        self.bindProj()


class PlayerStdBullet(PlayerBulletBase):
    def __init__(self, shotFrom: Player, posX: int, posY: int, velX: int, velY: int):
        """A projectile fired by a player that moves at a constant velocity

        ### Arguments
            - shotFrom (``Player``): The player that the bullet was shot from
            - posX (``int``): The x-position where the bullet should be spawned
            - posY (``int``): The y-position where the bullet should be spawned
            - velX (``int``): The x-axis component of the bullet's velocity
            - velY (``int``): The y-axis component of the bullet's velocity
        """        
        super().__init__()
        self.show(LAYER['proj_layer'])
        self.damage = PROJ_DMG[PROJ_STD]

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(-24, -24, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
        self.bindProj()


class EnemyStdBullet(EnemyBulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYER['proj_layer'])

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.damage = PROJ_DMG[PROJ_STD]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(-24, -24, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
        self.bindProj()


# ============================================================================ #
#                                 Portal Class                                 #
# ============================================================================ #
class Portal(PortalBase):
    def __init__(self, posX: int, posY: int, facing: str = SOUTH):
        """A portal that can teleport any moving object

        ### Arguments
            - posX (``int``): The x-position where the portal should spawn
            - posY (``int``): The y-position where the portal should spawn
            - facing (``str``, optional): The direction the portal should face. Defaults to ``SOUTH``.
        """        
        super().__init__()
        all_sprites.add(self, layer = LAYER['portal_layer'])
        
        self.pos = vec((posX, posY))
        self.facing = facing

        self.setImages("sprites/portals/portals.png", 64, 64, 1, 1)
        self.setRects(self.pos.x, self.pos.y, 64, 64, 54, 54)

        self.image, self.hitbox = self.getFace()

    def getFace(self) -> tuple:
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

    def update(self):
        if self.facing == None:
            self.kill()
        
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        pygame.draw.rect(screen, RED, self.hitbox, 3)


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


# ============================================================================ #
#                            Bullet Explosion Class                            #
# ============================================================================ #
class ProjExplode(ActorBase):
    def __init__(self, proj: BulletBase):
        """An explosion that is displayed on-screen when a projectile hits something
        
        ### Arguments
            - proj (``BulletBase``): The projectile that is exploding
        """            
        super().__init__()
        self.show(LAYER['explosion_layer'])
        self.proj = proj
        
        self.spritesheet = Spritesheet("sprites/bullets/bullets.png", 8)
        self.index = 1

        if isinstance(proj, PlayerStdBullet) or isinstance(proj, EnemyStdBullet):
            self.images = self.spritesheet.get_images(32, 32, 4)
            self.original_images = self.spritesheet.get_images(32, 32, 4)

        elif isinstance(proj, PortalBullet):
            self.images = self.spritesheet.get_images(32, 32, 4)
            self.original_images = self.spritesheet.get_images(32, 32, 4)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        self.rect = self.proj.rect
        self.randRotation = rand.randint(1, 360)

        self.pos = self.proj.pos

    def update(self):
        global anim_timer
        if isinstance(self.proj, PlayerStdBullet) or isinstance(self.proj, EnemyStdBullet):
            if anim_timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1

        elif isinstance(self.proj, PortalBullet):
            if anim_timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1
        
        # Give explosion its random rotation
        self.image = pygame.transform.rotate(self.original_image, self.randRotation)
        self.rect = self.image.get_rect(center = self.rect.center)


# ============================================================================ #
#                             Wall & Floor Classes                             #
# ============================================================================ #
class Wall(EnvirBase):
    def __init__(self, blockPosX: float, blockPosY: float, blockWidth: float, blockHeight: float):
        super().__init__()
        self.show(LAYER['wall_layer'])
        all_walls.add(self) 

        self.blockWidth, self.blockHeight = blockWidth, blockHeight
        self.pos = getTopLeftCoordinates(blockWidth * 16, blockHeight * 16, blockPosX * 16, blockPosY * 16)

        self.texture = pygame.image.load("sprites/textures/wall.png").convert()
        self.image: pygame.Surface = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, None)

        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox.center = self.pos


class Floor(EnvirBase):
    def __init__(self, blockPosX: float, blockPosY: float, blockWidth: float, blockHeight: float):
        super().__init__()
        self.show(LAYER['floor'])
        all_floors.add(self)
        self.blockWidth, self.blockHeight = blockWidth, blockHeight
        self.pos = getTopLeftCoordinates(blockWidth * 32, blockHeight * 32, blockPosX * 32, blockPosY * 32)

        self.spritesheet = Spritesheet("sprites/textures/floor.png", 4)
        self.textures = self.spritesheet.get_images(64, 64, 4)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, BLACK)

        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()
        self.rect.center = self.pos
        self.hitbox.center = self.pos
    
    def update(self):
        if self.visible and getTimeDiff(self.lastFrame) >= 0.25:
            self.index += 1
            if self.index > 3:
                self.index = 0
            self.texture = self.textures[self.index]
            self.image = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, BLACK)
            self.lastFrame = time.time()


# ============================================================================ #
#                                Visual Classes                                #
# ============================================================================ #
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
        # pygame.draw.rect(screen, RED, self.rect, 3)


# ============================================================================ #
#                                  Room Class                                  #
# ============================================================================ #
class Room(AbstractBase):
    def __init__(self, roomX, roomY):
        """The room where all the current action is taking place

        ### Arguments:
            roomX (int): The room's x-axis location in the grid of the room layout
            roomY (int): The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        all_rooms.append(self)
        self.room = vec((roomX, roomY))

        self.player1: Player = Player()

    def layoutUpdate(self):
        """Updates the layout of the room."""        
        for sprite in self.sprites():
            sprite.kill()
        
        #---------- Room Layouts ----------#
        if self.room == vec(0, 0):
            self.add(
                Wall(0, 0, 4, 4)
            )

            # Search for an enemy container for this room
            try:
                container = next(c for c in all_containers if c.room == self.room)
                showEnemies(container)

            except StopIteration:
                all_containers.append(
                    EnemyContainer(
                        self.room.x, self.room.y,
                    )
                )

        elif self.room == vec(1, 0):
            self.add(
                Wall(0, 0, 40, 4),
                Wall(0, 18.5, 40, 4),
            )

            # Search for an enemy container for this room
            try:
                container = next(c for c in all_containers if c.room == self.room)
                showEnemies(container)

            except StopIteration:
                all_containers.append(
                    EnemyContainer(
                        self.room.x, self.room.y,
                        StandardGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2),
                        StandardGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2),
                    )
                )

        elif self.room == vec(0, 1):
            self.add(
                Wall(0, 0, 4, 22.5),
                Wall(36, 0, 4, 22.5),
                Wall(8, 4, 4, 4),
                Wall(28, 4, 4, 4),
            )

            # Search for an enemy container for this room
            try:
                container = next(c for c in all_containers if c.room == self.room)
                showEnemies(container)

            except StopIteration:
                all_containers.append(
                    EnemyContainer(
                        self.room.x, self.room.y,
                        StandardGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2),
                        StandardGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2),
                    )
                )


class EnemyContainer(AbstractBase):
    def __init__(self, roomX: int, roomY: int, *sprites: EnemyBase):
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
        if self.room == mainroom.room:
            for sprite in self.sprites():
                sprite.hide()
                if hasattr(sprite, 'healthBar'):
                    sprite.healthBar.hide()

    def showEnemies(self):
        """Shows all of the enemies within the container"""      
        for sprite in self.sprites():
            sprite.show(LAYER['enemy_layer'])
            if hasattr(sprite, 'healthBar'):
                sprite.healthBar.show(LAYER['statBar_layer'])


def hideCurrentEnemies():
    """Hides all of the enemy sprites in the current room"""
    for container in all_containers:
        if container.room == mainroom.room:
            for sprite in container.sprites():
                sprite.hide()
                if hasattr(sprite, 'healthBar'):
                    sprite.healthBar.hide()


def showEnemies(container):
    """Shows all the enemies within an enemy container
    
    ### Arguments
        - container (``pygame.sprite.AbstractGroup``): The enemy container to unhide
    """    
    for sprite in container.sprites():
        sprite.show(LAYER['enemy_layer'])
        if hasattr(sprite, 'healthBar'):
            sprite.healthBar.show(LAYER['statBar_layer'])


# ============================================================================ #
#                                  UI Classes                                  #
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

        self.rightArrow = RightMenuArrow(WIN_WIDTH - 64, WIN_HEIGHT / 2)
        self.leftArrow = LeftMenuArrow(64, WIN_HEIGHT / 2)
        
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
            all_sprites.add(sprite, layer = LAYER['ui_layer_1'])

    def cycleMenu(self):
        if (not self.cyclingLeft and 
            not self.cyclingRight and
            not can_update):
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
                    sprite.pos.x = cosInterp(sprite.start_pos.x, sprite.start_pos.x - WIN_WIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cyclingLeft = False

        # Cycling right
        if not self.cyclingLeft and self.cyclingRight:
            weight = getTimeDiff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = cosInterp(sprite.start_pos.x, sprite.start_pos.x + WIN_WIDTH, weight)
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
        global can_update
        if keyReleased[K_e] % 2 != 0 and keyReleased[K_e] > 0:
            self.show()
            self.rightArrow.show(LAYER['ui_layer_1'])
            self.leftArrow.show(LAYER['ui_layer_1'])
            can_update = False

        elif keyReleased[K_e] % 2 == 0 and keyReleased[K_e] > 0:
            self.hide()
            self.rightArrow.hide()
            self.leftArrow.hide()
            can_update = True
            
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
#                                 Font Classes                                 #
# ============================================================================ #
class DamageChar(ActorBase):
    def __init__(self, posX: float, posY: float, damage: int):
        """A number that pops up after a player or enemy is hit that indicates how much damage that entity has taken
        
        ### Arguments
            - posX (``float``): _description_
            - posY (``float``): _description_
            - damage (``int``): _description_
        """        
        super().__init__()
        global anim_timer
        self.show(LAYER['text_layer'])
        all_font_chars.add(self)
        self.start_time = time.time()

        self.pos = vec((posX, posY))
        self.vel = vec(0, -2)

        self.image = textToImage(str(damage), "sprites/ui/font.png", 9, 14, 36)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos

    def update(self):
        self.movement()

        if getTimeDiff(self.start_time) > 0.75:
            self.kill()


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
def redrawGameWindow():
    """Draws all entities every frame"""
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
# Load rooms
mainroom = Room(0, 0)
mainroom.layoutUpdate()

# Time control
anim_timer = 0
last_time = time.time()


def checkKeyRelease(isMouse, *inputs):
    """Checks if any input(s) has been released. If one has, then its count in ''keyReleased'' will be updated to match.
    
    ### Arguments
        - isMouse (``bool``): Are the inputs mouse buttons?
        - inputs (``str``, multiple): The input(s) to check
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
    dt = getTimeDiff(last_time) * 60
    last_time = time.time()
    
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
            1: pygame.mouse.get_pressed()[0],
            2: pygame.mouse.get_pressed()[1],
            3: pygame.mouse.get_pressed()[2],

            K_a: keyPressed[K_a],
            K_w: keyPressed[K_w],
            K_s: keyPressed[K_s],
            K_d: keyPressed[K_d],
            K_x: keyPressed[K_x],
            K_e: keyPressed[K_e]
        }

        checkKeyRelease(False, K_e, K_x)
        checkKeyRelease(True, 1, 2, 3)

    screen.fill((255, 250, 255))

    #------------------------------ Game operation ------------------------------#
    # Regenerate health for testing purposes
    for a_player in all_players:
        if anim_timer % 5 == 0 and a_player.hp < a_player.max_hp and isInputHeld[K_x]:
            a_player.hp += 1

    #------------------------------ Redraw window ------------------------------#
    redrawGameWindow()
    clock.tick_busy_loop(FPS)