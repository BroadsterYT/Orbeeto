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
vec = pygame.math.Vector2
spriteGroup = pygame.sprite.Group
rad = radians
deg = degrees

clock = pygame.time.Clock()

screenSize = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED)
pygame.display.set_caption('Orbeeto')


def getClosestPlayer(check_sprite: pygame.sprite.Sprite) -> pygame.sprite.Sprite:
    """Checks for the closest player to a given sprite.
    
    ### Parameters
        - check_sprite ``(pygame.sprite.Sprite)``: The entity checking for the closest player
    
    ### Returns
        - ``pygame.sprite.Sprite``: The player closest to ``check_sprite``
    """    
    playerCoords = {}
    for a_player in all_players:
        playerCoords[a_player] = getDistToSprite(check_sprite, a_player)

    try:
        temp = min(playerCoords.values())
        result = [key for key in playerCoords if playerCoords[key] == temp]
        return result[0]
    except:
        return check_sprite


def objectAccel(sprite):
    """Defines the relationship between acceleration, velocity, and position (and time, when called once every frame)
    
    ### Parameters
        - ``sprite`` ``(pygame.sprite.Sprite)``: The sprite that should follow the acceleration logic
    """    
    sprite.accel.x += sprite.vel.x * FRIC
    sprite.accel.y += sprite.vel.y * FRIC
    sprite.vel += sprite.accel * dt
    sprite.pos += sprite.vel + sprite.accel_const * sprite.accel


# ============================================================================ #
#                                 Player Class                                 #
# ============================================================================ #
class PlayerBase(ActorBase):
    def __init__(self):
        """The base class for all player objects. It contains parameters and methods to gain better control over player objects."""        
        super().__init__()
        self.room = vec((0, 0))

        self.pos = vec((WIN_WIDTH / 2, WIN_HEIGHT / 2))
        self.accel_const = 0.52

        self.room = vec((0, 0))

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

        self.menu = InventoryMenu()
        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)

        self.inventory = {}
        for item in MAT.values():
            self.inventory.update({item: 0})

    def changeRoom(self, direction: str) -> None:
        hideCurrentEnemies()

        if direction == DOWN:
            room.room.y -= 1
            room.layoutUpdate()
            self.pos.y -= WIN_HEIGHT
            groupChangeRooms(all_portals, DOWN)

        elif direction == RIGHT:
            room.room.x += 1
            room.layoutUpdate()
            self.pos.x -= WIN_WIDTH
            groupChangeRooms(all_portals, RIGHT)

        elif direction == UP:
            room.room.y += 1
            room.layoutUpdate()
            self.pos.y += WIN_HEIGHT
            groupChangeRooms(all_portals, UP)
        
        elif direction == LEFT:
            room.room.x -= 1
            room.layoutUpdate()

            self.pos.x += WIN_WIDTH
            groupChangeRooms(all_portals, LEFT)

        killGroups(all_projs, all_explosions)

    def checkRoomChange(self):
        if self.pos.x <= 0:
            self.changeRoom(LEFT)

        if self.pos.x >= WIN_WIDTH:
            self.changeRoom(RIGHT)

        if player1.pos.y <= 0:
            self.changeRoom(UP)

        if player1.pos.y >= WIN_HEIGHT:
            self.changeRoom(DOWN)

    def teleport(self, portal_in):
        for portal in all_portals:
            if portal != portal_in:
                portalOut = portal

        velCopy = self.vel.copy()

        width = portalOut.hitbox.height // 2
        height = portalOut.hitbox.width // 2

        if portal_in.facing == DOWN:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
            
            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)

        if portal_in.facing == RIGHT:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, -velCopy.x)
                
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - width
                self.vel = vec(-velCopy.y, velCopy.x)

            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset

        if portal_in.facing == UP:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)

        if portal_in.facing == LEFT:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(velCopy.y, -velCopy.x)
            
            if portalOut.facing == LEFT:
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
        self.show(LAYERS['player_layer'])

        self.setImages("sprites/orbeeto/orbeeto.png", 64, 64, 5, 0, 0)
        self.setRects(0, 0, 64, 64, -32, -32)

        self.bulletType = PROJ_P_STD
        self.can_fire_portal = False

    def movement(self):
        """When called once every frame, it allows the player to recive input from the user and move accordingly"""        
        self.accel = vec(0, 0)
        if self.visible:
            if isInputHeld[K_a] == True:
                self.accel.x = -self.accel_const * dt
            if isInputHeld[K_d] == True:
                self.accel.x = self.accel_const * dt
            if isInputHeld[K_s] == True:
                self.accel.y = self.accel_const * dt
            if isInputHeld[K_w] == True:
                self.accel.y = -self.accel_const * dt

            self.rect.center = self.pos
            self.hitbox.center = self.pos
            objectAccel(self)

    def shoot(self):
        """Shoots a bullet"""
        angle_to_mouse = rad(getAngleToMouse(self))

        velX = self.bulletVel * -sin(angle_to_mouse)
        velY = self.bulletVel * -cos(angle_to_mouse)

        if isInputHeld[1] and self.bulletType == PROJ_P_STD and time.time() - self.last_shot >= self.gun_cooldown:
            offset = vec((21, 30))
            all_projs.add(
                PlayerStdBullet(self,
                    self.pos.x - (offset.x * cos(angle_to_mouse)) - (offset.y * sin(angle_to_mouse)),
                    self.pos.y + (offset.x * sin(angle_to_mouse)) - (offset.y * cos(angle_to_mouse)),
                    velX, velY
                ),
                
                PlayerStdBullet(self,
                    self.pos.x + (offset.x * cos(angle_to_mouse)) - (offset.y * sin(angle_to_mouse)),
                    self.pos.y - (offset.x * sin(angle_to_mouse)) - (offset.y * cos(angle_to_mouse)),
                    velX, velY
                )
            )
            self.last_shot = time.time()

        # Firing portals
        if keyReleased[3] % 2 == 0 and self.can_fire_portal:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.can_fire_portal = False

        elif keyReleased[3] % 2 != 0 and not self.can_fire_portal:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75))
            self.can_fire_portal = True

    def update(self):
        if can_update and self.visible:
            collideCheck(self, all_enemies, all_movable, all_walls)

            self.movement()
            self.shoot()
            self.checkRoomChange()

            for portal in all_portals:
                if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                    self.teleport(portal)

            # Animation
            if time.time() - self.lastFrame > ANIMTIME:
                if isInputHeld[1]:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                else: # Idle animation
                    self.index = 0
                
                self.lastFrame = time.time()

            # Animation rotation
            self.rotateImage(getAngleToMouse(self))

            # Dodge charge up
            if self.hitTime < self.hitTime_charge:
                self.hitTime += 1
        
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

    def collisionDetect(self):
        collideCheck(self, all_players, all_walls)

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
        
        ### Parameters
            - posX (``_type_``): _description_
            - posY (``_type_``): _description_
        """         
        super().__init__()
        self.show(LAYERS['enemy_layer'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WIN_WIDTH - 64), rand.randint(64, WIN_HEIGHT - 64))

        self.setImages("sprites/enemies/standard_grunt.png", 64, 64, 5, 0, 0)
        self.setRects(0, 0, 64, 64, -32, -32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 15, 10, 10, 25, 0.4)

    def movement(self, canShoot: bool):
        if self.hp > 0:
            if time.time() - self.lastRelocate > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, WIN_WIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, WIN_HEIGHT - self.image.get_height() - 64)
                self.lastRelocate = time.time()

            if self.pos.x != (self.rand_pos.x) or self.pos.y != (self.rand_pos.y):
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.accel_const
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.accel_const
                else:
                    self.accel.x = 0

                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.accel_const
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.accel_const
                else:
                    self.accel.y = 0
            
            if canShoot:
                self.shoot(getClosestPlayer(self), 6, rand.uniform(0.4, 0.9))

            self.rect.center = self.pos
            self.hitbox.center = self.pos
            objectAccel(self)

    def shoot(self, target, vel, shoot_time):
        global anim_timer
        if time.time() - self.lastShot > shoot_time:
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
            self.collisionDetect()
            self.movement(True)
            
            # Animation
            if time.time() - self.lastFrame > ANIMTIME:
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
        self.show(LAYERS['enemy_layer'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WIN_WIDTH - 64), rand.randint(64, WIN_HEIGHT - 64))

        self.setImages("sprites/enemies/octogrunt.png", 64, 64, 1, 0, 0)
        self.setRects(0, 0, 64, 64, -32, -32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 44, 10, 10, 45, 0.4)

    def movement(self, canShoot):
        if can_update and self.visible:
            if time.time() - self.lastRelocate > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(0, WIN_WIDTH)
                self.rand_pos.y = rand.randint(0, WIN_HEIGHT)
                self.lastRelocate = time.time()

            if self.pos.x != self.rand_pos.x or self.pos.y != self.rand_pos.y:
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.accel_const
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.accel_const
                else:
                    self.accel.x = 0

                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.accel_const
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.accel_const
                else:
                    self.accel.y = 0
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 3, 1)

            self.rect.center = self.pos
            self.hitbox.center = self.pos
            objectAccel(self)

    def shoot(self, target, vel, shoot_time):
        if time.time() - self.lastShot > shoot_time:
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
            self.collisionDetect()
            self.movement(True)

            # Animation
            if time.time() - self.lastFrame > ANIMTIME:
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
        self.show(LAYERS['movable_layer'])
        all_movable.add(self)

        self.spritesheet = Spritesheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 1)
        self.index = 0

        self.pos = vec((posX, posY))
        self.accel_const = 0.4

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect

        self.rect.center = self.pos

    def movement(self):
        self.accel = vec(0, 0)
        if self.visible:
            if self.hitbox.colliderect(player1.rect):
                if collideSideCheck(self, player1) == DOWN:
                    self.accel.y = -self.accel_const * dt
                if collideSideCheck(self, player1) == RIGHT:
                    self.accel.x = -self.accel_const * dt
                if collideSideCheck(self, player1) == UP:
                    self.accel.y = self.accel_const * dt
                if collideSideCheck(self, player1) == LEFT:
                    self.accel.x = self.accel_const * dt

            self.rect.center = self.pos
            self.hitbox.center = self.pos

            objectAccel(self)

    def update(self):
        pass


class DropBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.accel_const = 0.8


class ItemDrop(DropBase):
    def __init__(self, dropped_from, item_name):
        """An item or material dropped by an enemey that is able to be collected
        
        ### Parameters
            - dropped_from (``pygame.sprite.Sprite``): The enemy that the item was dropped from
            - item_name (``str``): The item to drop
            - item_frame_start (``int``): The index of the first frame to display from the item drop spritesheet (0 = the first image).
            - image_count (``int``): The number of frames to use
        """        
        super().__init__()
        self.show(LAYERS['drops_layer'])
        all_drops.add(self)
        self.droppedFrom = dropped_from
        self.mat = item_name

        self.start_time = time.time()
        self.pos = vec(self.droppedFrom.pos.x, self.droppedFrom.pos.y)
        self.randAccel = getRandComponents(self.accel_const)
        
        self.spritesheet = Spritesheet("sprites/textures/item_drops.png")
        self.index = 0

        if self.mat == MAT[0]:
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 1, 0)
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 1, 0)
        elif self.mat == MAT[1]:
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 1, 1)
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 1, 1)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        self.accel = vec(0, 0)
        if self.visible:
            time_since_start = time.time() - self.start_time
            if time_since_start <= 0.1:
                self.accel.x = self.randAccel.x
                self.accel.y = self.randAccel.y
            
            if time_since_start <= 10:
                self.original_image = self.original_images[self.index]
                self.image = pygame.transform.rotate(self.original_image, int(degrees(sin(self.period_mult * pi * time_since_start) * (1 / time_since_start))))
                self.rect = self.image.get_rect(center = self.rect.center)
            
            objectAccel(self)
        
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        collideCheck(self, all_walls)

        self.movement()

        if self.hitbox.colliderect(player1):
            player1.inventory[self.mat] += 1
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

        if portal_in.facing == DOWN:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
            
            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)

        if portal_in.facing == RIGHT:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, -velCopy.x)
                
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - width
                self.vel = vec(-velCopy.y, velCopy.x)

            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset

        if portal_in.facing == UP:
            distOffset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            
            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(-velCopy.x, -velCopy.y)
            
            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.y, velCopy.x)

        if portal_in.facing == LEFT:
            distOffset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)

            if portalOut.facing == DOWN:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y + height
                self.vel = vec(velCopy.y, velCopy.x)
            
            if portalOut.facing == RIGHT:
                self.pos.x = portalOut.pos.x + width
                self.pos.y = portalOut.pos.y + distOffset
            
            if portalOut.facing == UP:
                self.pos.x = portalOut.pos.x + distOffset
                self.pos.y = portalOut.pos.y - height
                self.vel = vec(velCopy.y, -velCopy.x)
            
            if portalOut.facing == LEFT:
                self.pos.x = portalOut.pos.x - width
                self.pos.y = portalOut.pos.y + distOffset
                self.vel = vec(-velCopy.x, -velCopy.y)

    def projCollide(self, spriteGroup, canHurt):
        """Destroys a given projectile upon a collision and renders an explosion

        ### Parameters
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
        self.show(LAYERS['proj_layer'])
        
        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.hitbox_adjust = vec(0, 0)
        self.damage = PROJS[PROJ_P_PORTAL]

        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(-24, -24, 8, 8)
        self.hitbox = self.rect.inflate(self.hitbox_adjust.x, self.hitbox_adjust.y)

        # Rotate sprite to trajectory
        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

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
                    side = portalSideCheck(colliding_entity, self)
                    if side == DOWN:
                        all_portals.add(Portal(self.pos.x, colliding_entity.pos.y + (colliding_entity.image.get_height() / 2), side))
                        portalCountCheck()
                    if side == UP:
                        all_portals.add(Portal(self.pos.x, colliding_entity.pos.y - (colliding_entity.image.get_height() / 2), side))
                        portalCountCheck()
                    if side == RIGHT:
                        all_portals.add(Portal(self.pos.x, self.pos.y, side))
                        portalCountCheck()
                    if side == LEFT:
                        all_portals.add(Portal(self.pos.x, self.pos.y, side))
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
        self.images = self.spritesheet.get_images(0, 0, 32, 32, 5, 4)
        self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 5, 4)
        self.hitbox_adjust = vec(0, 0)
        if anim_timer % 5 == 0:
            self.index += 1
            if self.index > 4:
                self.index = 0
        
        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.bindProj()


class PlayerStdBullet(PlayerBulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        """A projectile object that moves at a constant velocity

        Parameters:
        ----------
            shotFrom (pygame.sprite.Sprite): The entity the projectile is being shot from

            posX (float): The x-position that the projectile should be spawned at

            posY (float): The y-position that the projectile should be spawned at

            velX (float): The x-axis component of the projectile's velocity

            velY (float): The y-axis component of the projectile's velocity

            bulletType (str): The type of projectile that should be spawned
        """           
        super().__init__()
        self.show(LAYERS['proj_layer'])

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.damage = PROJS[PROJ_P_STD]

        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(-24, -24, 8, 8)
        self.hitbox = self.rect.inflate(-2, -2)

        # Rotate sprite to trajectory
        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.original_image = self.original_images[self.index]

        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.bindProj()


class EnemyStdBullet(EnemyBulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYERS['proj_layer'])

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.damage = PROJS[PROJ_P_STD]

        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(-24, -24, 8, 8)
        self.hitbox = self.rect.inflate(-2, -2)

        # Rotate sprite to trajectory
        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.original_image = self.original_images[self.index]

        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.bindProj()


# ============================================================================ #
#                                 Portal Class                                 #
# ============================================================================ #
class Portal(PortalBase):
    def __init__(self, posX, posY, facing=DOWN):
        """A portal object that can teleport players, enemies, and projectiles

        Parameters:
        ----------
            posX (float): The x-position where the portal will spawn

            posY (float): The y-position where the portal will spawn

            facing (str, optional): The direction of an entity's velocity after being expelled. Defaults to DOWN.
        """        
        super().__init__()
        all_sprites.add(self, layer = LAYERS['portal_layer'])
        
        self.pos = vec((posX, posY))
        self.facing = facing

        self.spritesheet = Spritesheet("sprites/portals/portals.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 1)
        self.index = 0
        
        self.image = self.images[self.index]
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 32, 32)
        
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.center = self.pos

        self.hitbox = self.rect.inflate(-10, -10)

        if self.facing == DOWN:
            self.hitbox = self.rect.inflate(0, -40)
        if self.facing == RIGHT:
            self.image = pygame.transform.rotate(self.image, 90)
            self.hitbox = self.rect.inflate(-40, 0)
        if self.facing == UP:
            self.image = pygame.transform.rotate(self.image, 180)
            self.hitbox = self.rect.inflate(0, -40)
        if self.facing == LEFT:
            self.image = pygame.transform.rotate(self.image, 270)
            self.hitbox = self.rect.inflate(-40, 0)
        if self.facing == None:
            self.kill()

    def update(self):
        if self.facing == None:
            self.kill()
        
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)


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


def portalSideCheck(wall, portal):
    """Checks for which side of a wall a portal hit and assigns it that value
    
    ### Parameters
        - ``wall`` ``(pygame.sprite.Sprite)``: The wall being hit
        - ``portal`` ``(pygame.sprite.Sprite)``: The portal being fired
    
    ### Returns
        - ``str``: The direction the portal should face
    """    
    if wall.pos.x - 0.45 * wall.image.get_width() <= portal.pos.x <= wall.pos.x + 0.45 * wall.image.get_width():
        if portal.pos.y < wall.pos.y:
            return UP
        elif portal.pos.y > wall.pos.y:
            return DOWN
        
    elif wall.pos.y - 0.45 * wall.image.get_height() <= portal.pos.y <= wall.pos.y + 0.45 * wall.image.get_height():
        if portal.pos.x < wall.pos.x:
            return LEFT
        elif portal.pos.x > wall.pos.x:
            return RIGHT
        
    else:
        return None


# ============================================================================ #
#                            Bullet Explosion Class                            #
# ============================================================================ #
class ProjExplode(ActorBase):
    def __init__(self, proj):
        """An explosion/shattering that is displayed on-screen when a projectile hits something

        Parameters:
        --------
            proj (pygame.sprite.Sprite): The projectile that is exploding
        """
        super().__init__()
        self.show(LAYERS['explosion_layer'])

        self.proj = proj
        
        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.index = 1

        if isinstance(proj, PlayerStdBullet) or isinstance(proj, EnemyStdBullet):
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)

        elif isinstance(proj, PortalBullet):
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)

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
    def __init__(self, topleftX_mult: float, topleftY_mult: float, widthMult: float, heightMult: float):
        super().__init__()
        all_sprites.add(self, layer = LAYERS['wall_layer'])
        all_walls.add(self)

        self.visible = True

        self.image = pygame.Surface((32 * widthMult, 32 * heightMult))
        self.texture = pygame.image.load("sprites/textures/wall.png")
        self.tileTexture(None)

        self.pos = getTopLeftCoordinates(self, topleftX_mult * 32, topleftY_mult * 32)
        self.rect.center = self.pos


class Floor(EnvirBase):
    def __init__(self, topleftX_mult: float, topleftY_mult: float, widthMult: float, heightMult: float):
        super().__init__()
        self.show(LAYERS['floor'])
        all_floors.add(self)

        self.sizeMult = vec(widthMult, heightMult)

        self.spritesheet = Spritesheet("sprites/textures/floor.png")
        self.textures = self.spritesheet.get_images(0, 0, 64, 64, 4)
        self.index = 0

        self.image = pygame.Surface((32 * widthMult, 32 * heightMult))
        self.texture = self.textures[self.index]
        self.tileTexture((0, 0, 0))

        self.pos = getTopLeftCoordinates(self, topleftX_mult * 32, topleftY_mult * 32)
        self.rect.center = self.pos
    
    def update(self):
        if self.visible and time.time() - self.lastFrame >= 0.25:
            self.index += 1
            if self.index > 3:
                self.index = 0
            self.texture = self.textures[self.index]
            self.tileTexture((0, 0, 0))
            self.lastFrame = time.time()


# ============================================================================ #
#                                  Room Class                                  #
# ============================================================================ #
class Room(AbstractBase):
    def __init__(self, roomX, roomY):
        """The room where all the current action is taking place

        Parameters:
            roomX (int): The room's x-axis location in the grid of the room layout
            roomY (int): The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        
        all_rooms.append(self)
        self.room = vec((roomX, roomY))

    def layoutUpdate(self):
        """Updates the layout of the room."""        
        for sprite in self.sprites():
            sprite.kill()
        
        #---------- Room Layouts ----------#
        if self.room == vec(0, 0):
            self.add(
                Wall(0, 0, 4, 4),
                Wall(36, 0, 4, 4),
                Wall(0, 18.5, 4, 4),
                Wall(36, 18.5, 4, 4),
                Floor(0, 0, 10, 22.5),
            )

            # Search for an enemy container for this room
            try:
                container = next(c for c in all_containers if c.room == self.room)
                showEnemies(container)

            except StopIteration:
                all_containers.append(
                    EntityContainer(
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
                    EntityContainer(
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
                    EntityContainer(
                        self.room.x, self.room.y,
                        OctoGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2),
                        OctoGrunt(WIN_WIDTH / 2, WIN_HEIGHT / 2)
                    )
                )


class EntityContainer(AbstractBase):
    def __init__(self, roomX, roomY, *sprites):
        """A container for enemies. Contains data about all enemies in a room.

        Parameters:
        -------
            roomX (int): The room's x-axis location in the grid of the room layout

            roomY (int): The room's y-axis location in the grid of the room layout

            sprites (pygame.sprite.Sprite): The sprite(s) to add to the container
        """        
        super().__init__()
        self.room = vec((roomX, roomY))

        for sprite in sprites:
            self.add(sprite)


def hideCurrentEnemies():
    """Hides all of the enemy sprites in the current room"""
    for container in all_containers:
        if container.room == room.room:
            for sprite in container.sprites():
                if hasattr(sprite, "healthBar"):
                    sprite.healthBar.hide()
                sprite.hide()


def showEnemies(container):
    """Shows all the enemies within an enemy container
    
    ### Parameters
        - container (``pygame.sprite.AbstractGroup``): The enemy container to unhide
    """    
    for sprite in container.sprites():
        sprite.show(LAYERS['enemy_layer'])
        if hasattr(sprite, "healthBar"):
            sprite.healthBar.show(LAYERS['statBar_layer'])


# ============================================================================ #
#                                  UI Classes                                  #
# ============================================================================ #
class InventoryMenu(AbstractBase):
    def __init__(self):
        """A menu used to view collected items and utilize them for various purposes
        
        ### Parameters
            - owner ``(pygame.sprite.Sprite)``: The player whom the inventory belongs to
        """        
        super().__init__()
        self.is_cyclingLeft = False
        self.is_cyclingRight = False
        
        self.wipeTime = 1

        self.window = 0
        
        self.last_cycle = time.time()

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
            all_sprites.add(sprite, layer = LAYERS['ui_layer_1'])

    def cycleMenu(self):
        if not self.is_cyclingLeft and not self.is_cyclingRight:
            if isInputHeld[1] and self.leftArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window -= 1
                self.last_cycle = time.time()
                self.is_cyclingLeft = True

        if self.is_cyclingLeft and not self.is_cyclingRight:
            t_lapsed = time.time() - self.last_cycle
            if t_lapsed <= self.wipeTime:
                for sprite in self.sprites():
                    sprite.pos.x = sprite.start_pos.x - (-(WIN_WIDTH / 2) * cos((1 / self.wipeTime) * pi * t_lapsed) + (WIN_WIDTH / 2))
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                    sprite.pos.x = sprite.start_pos.x + (WIN_WIDTH * self.window)
                self.is_cyclingLeft = False
        
        if not self.is_cyclingRight and not self.is_cyclingLeft:
            if isInputHeld[1] and self.rightArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window += 1
                self.last_cycle = time.time()
                self.is_cyclingRight = True

        if self.is_cyclingRight and not self.is_cyclingLeft:
            t_lapsed = time.time() - self.last_cycle
            if t_lapsed <= self.wipeTime:
                for sprite in self.sprites():
                    sprite.pos.x = sprite.start_pos.x + (-(WIN_WIDTH / 2) * cos((1 / self.wipeTime) * pi * t_lapsed) + (WIN_WIDTH / 2))
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                    sprite.pos.x = sprite.start_pos.x + (WIN_WIDTH * self.window)
                self.is_cyclingRight = False

    def buildMenuSlots(self):
        space = vec(0, 0)
        space_cushion = vec(82, 82)
        menu_slots = []
        slot_count = 0
        offset = 0
        for y in range(5):
            for x in range(5):
                menu_slots.append(MenuSlot(64 + space.x, 64 + space.y, MAT[slot_count], 1, offset))
                space.x += space_cushion.x
                offset += 1
                slot_count += 1
            space.y += space_cushion.y
            space.x = 0
        return menu_slots

    def update(self):
        global can_update
        if keyReleased[K_e] % 2 != 0 and keyReleased[K_e] > 0:
            self.show()
            self.rightArrow.show(LAYERS['ui_layer_1'])
            self.leftArrow.show(LAYERS['ui_layer_1'])
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
        
        ### Parameters
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """        
        super().__init__()
        self.pos = vec((posX, posY))
        self.return_pos = vec((posX, posY))
        
        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 61)
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
        
        ### Parameters
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((posX, posY))
        self.return_pos = vec((posX, posY))
        
        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 61)
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


class MenuSlot(pygame.sprite.Sprite):
    def __init__(self, posX, posY, item_held, num_frames, frame_offset):
        """A menu slot that shows the collected amount of a specific item
        
        ### Parameters
            - posX (``float``): The x-position to spawn at
            - posY (``float``): The y-position to spawn at
            - item_held (``str``): The item the menu slot will hold. Items are chosen from ``MATERIALS`` dictionary.
            - num_frames (``int``): The number of animation frames the item has
            - frame_offset (``int``): Where the first frame of the animation begins. (0 = first image of sprite sheet)
        """
        super().__init__()
        all_slots.add(self)
        self.pos = vec((posX, posY))
        self.start_pos = vec((posX, posY))
        self.holding = item_held
        self.count = 0

        self.menusheet = Spritesheet("sprites/ui/menu_item_slot.png")
        self.itemsheet = Spritesheet("sprites/textures/item_drops.png")
        self.menu_imgs = self.menusheet.get_images(0, 0, 64, 64, 1)
        self.item_imgs = self.itemsheet.get_images(0, 0, 32, 32, num_frames, frame_offset)
        self.index = 0

        self.menu_img = self.menu_imgs[0]

        self.images = self.createSlotImages()
        self.image = self.images[self.index]

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

    def createSlotImages(self):
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that item on top
        
        ### Returns
            - ``list``: A list of the created images
        """        
        final_images = []
        for frame in self.item_imgs:
            # Combining menu image and item images
            new_img = pygame.Surface(vec(max(self.menu_img.get_width(), frame.get_width()), max(self.menu_img.get_height(), frame.get_height())))
            new_img.blit(self.menu_img, vec(0, 0))
            center_x = (new_img.get_width() - frame.get_width()) // 2
            center_y = (new_img.get_height() - frame.get_height()) // 2
            new_img.blit(frame, vec(center_x, center_y))

            # Adding the count of the item to its images
            char_sheet = Spritesheet("sprites/ui/font.png")
            chars = char_sheet.get_images(0, 0, 9, 14, 36)
            width, height = 9, 14
            
            charList = []
            for char in str(self.count):
                charList.append(chars[int(char) + 26])
            
            count_surface = pygame.Surface([width * len(charList), height]).convert()

            len_count = 0
            for surface in charList:
                count_surface.blit(surface, (width * len_count, 0), (0, 0, 9, 14))
                len_count += 1

            count_surface.set_colorkey((0, 0, 0))
            new_img.set_colorkey((0, 0, 0))
            new_img.blit(swapColor(swapColor(count_surface, (44, 44, 44), (156, 156, 156)), (0, 0, 1), (255, 255, 255)), vec(center_x, center_y))
            final_images.append(new_img)

        return final_images

    def update(self):
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        self.count = player1.inventory[self.holding]
        self.images = self.createSlotImages()
        self.hover()


# ============================================================================ #
#                                 Font Classes                                 #
# ============================================================================ #
class DamageChar(pygame.sprite.Sprite):
    def __init__(self, posX, posY, damage):
        """A number that pops up after a player or enemy is hit that indicates how much damage that entity has taken
        
        Parameters
        ----------
            posX (_type_): _description_
        
            posY (_type_): _description_
        
            damage (_type_): _description_
        
        """        
        super().__init__()
        global anim_timer
        all_sprites.add(self, layer = LAYERS['text_layer'])
        all_font_chars.add(self)
        
        self.spritesheet = Spritesheet("sprites/ui/font.png")
        self.images = self.spritesheet.get_images(0, 0, 9, 14, 36)

        self.pos = vec((posX, posY))
        self.vel = vec(0, -2)

        self.start_time = time.time()

        width = 9
        height = 14
        
        dmg_charList = []
        for char in str(damage):
            dmg_charList.append(self.images[int(char) + 26])
        
        new_surface = pygame.Surface([width * len(dmg_charList), height]).convert()

        count = 0
        for surface in dmg_charList:
            new_surface.blit(surface, (width * count, 0), (0, 0, 9, 14))
            count += 1
        
        self.rect = pygame.Rect(0, 0, 9, 14)

        self.image = new_surface
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.center = self.pos

    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos

    def update(self):
        global anim_timer
        if time.time() - self.start_time > 0.75:
            self.kill()


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
def redrawGameWindow():
    """Draws all entities every frame"""

    all_sprites.update()

    if can_update:
        # Updating movable objects
        for object in all_movable:
            object.movement()

        # Updating all item drops
        for item in all_drops:
            collideCheck(item, all_walls)

        # Updating all font characters
        for char in all_font_chars:
            char.movement()

    # Updating inventory
    player1.menu.update()

    all_sprites.draw(screen)
    pygame.display.update()


#------------------------------ Initialing parameters ------------------------------#
player1 = Player()

# Load rooms
room = Room(0, 0)
room.layoutUpdate()

# Time control
anim_timer = 0
last_time = time.time()

def checkKeyRelease(isMouse, *inputs):
    """Checks if any input(s) has been released. If one has, then its count in ''keyReleased'' will be updated to match.
    
    ### Parameters
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

#------------------------------ Main loop ------------------------------#
running = True
while running:
    dt = (time.time() - last_time) * 60
    last_time = time.time()
    
    anim_timer += 1

    if player1.hp <= 0:
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
        if anim_timer % 5 == 0 and a_player.hp < a_player.max_hp and isInputHeld[2]:
            a_player.hp += 1

    #------------------------------ Redraw window ------------------------------#
    redrawGameWindow()
    clock.tick_busy_loop(FPS)