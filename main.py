import pygame, pygame.font
from pygame.locals import *

pygame.init()

import sys, math, time
import random as rand

from math import sin, cos, radians, degrees, floor, pi

from Init import can_update, keyReleased
from Calculations import *
from ClassBases import *
from Constants import *
from Groups import *
from Spritesheet import *
from UI_Actors import *

# Aliases
vec = pygame.math.Vector2
spriteGroup = pygame.sprite.Group
rad = radians
deg = degrees

clock = pygame.time.Clock()

screenSize = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED)
pygame.display.set_caption('Orbeeto')

def getClosestPlayer(check_sprite):
    """Checks for the closest player to a given sprite.
    
    ### Parameters
        - ``check_sprite`` ``(pygame.sprite.Sprite)``: The entity checking for the closest player
    
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

def awardXp(killed_enemy):
    """Rewards players with xp after killing an enemy.
    
    ### Parameters
        - ``killed_enemy`` ``(pygame.sprite.Sprite)``: The enemy that has been killed
    """    
    for a_player in all_players:
        a_player.xp += killed_enemy.xp_worth

def tpLocation(tp_sprite, portal_in):
    """Teleports a sprite between two portals.
    
    ### Parameters
        - ``tp_sprite`` ``(pygame.sprite.Sprite)``: The sprite being teleported between portals
        - ``portal_in`` ``(pygame.sprite.Sprite)``: The portal that ``tp_sprite`` is entering
    """    
    for portal in all_portals:
        if portal != portal_in:
            other_portal = portal
            
    if other_portal.facing == DOWN:
        tp_sprite.pos.x = other_portal.pos.x
        tp_sprite.pos.y = other_portal.pos.y + other_portal.hitbox.height + tp_sprite.hitbox.height * 0.5
        tp_sprite.vel = vec(0, 0)

    elif other_portal.facing == RIGHT:
        tp_sprite.pos.x = other_portal.pos.x + other_portal.hitbox.width + tp_sprite.hitbox.width * 0.5
        tp_sprite.pos.y = other_portal.pos.y
        tp_sprite.vel = vec(0, 0)

    elif other_portal.facing == UP:
        tp_sprite.pos.x = other_portal.pos.x
        tp_sprite.pos.y = other_portal.pos.y - other_portal.hitbox.height - tp_sprite.hitbox.height * 0.5
        tp_sprite.vel = vec(0, 0)

    elif other_portal.facing == LEFT:
        tp_sprite.pos.x = other_portal.pos.x - other_portal.hitbox.width - tp_sprite.hitbox.width * 0.5
        tp_sprite.pos.y = other_portal.pos.y
        tp_sprite.vel = vec(0, 0)

def projFromPortalCen(proj, portal_in):
    """Calculates the distance a projectile is from a portal's center upon entering it. This allows the projectile to spawn at the correct position relative to the exit portal.
    
    ### Parameters
        - ``proj`` ``(pygame.sprite.Sprite)``: The projectile entering the portal
        - ``portal_in`` ``(pygame.sprite.Sprite)``: The portal the projectile is entering
    
    ### Returns
        - ``float``: The distance (along the x or y-axis) that the projectile is from the center of ``portal_in``
    """    
    if portal_in.facing == DOWN or portal_in.facing == UP:
        return proj.pos.x - portal_in.pos.x
    if portal_in.facing == RIGHT or portal_in.facing == LEFT:
        return proj.pos.y - portal_in.pos.y

def teleportProj(proj, portal_in):
    """Teleports a projectile between two portals
    
    ### Parameters
        - ``proj`` ``(pygame.sprite.Sprite)``: The projectile being teleported
        - ``portal_in`` ``(pygame.sprite.Sprite)``: The portal the projectile is entering
    """    
    for portal in all_portals:
        if portal != portal_in:
            portalOut = portal

    projGroup = players_projs

    if portal_in.facing == DOWN:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y + 8, proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + projFromPortalCen(proj, portal_in), -proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y - 8, proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + projFromPortalCen(proj, portal_in), proj.vel.y, proj.vel.x, proj.type))

    if portal_in.facing == RIGHT:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y + 8, proj.vel.y, -proj.vel.x, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + projFromPortalCen(proj, portal_in), -proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y - 8, -proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + projFromPortalCen(proj, portal_in), proj.vel.x, proj.vel.y, proj.type))

    if portal_in.facing == UP:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y + 8, proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + projFromPortalCen(proj, portal_in), proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y - 8, -proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + projFromPortalCen(proj, portal_in), -proj.vel.y, proj.vel.x, proj.type))

    if portal_in.facing == LEFT:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y + 8, proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + projFromPortalCen(proj, portal_in), proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + projFromPortalCen(proj, portal_in), portalOut.pos.y - 8, proj.vel.y, -proj.vel.x, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + projFromPortalCen(proj, portal_in), proj.vel.x, proj.vel.y, proj.type))

def groupChangeRooms(spriteGroup, direction):
    """Changes the room of all sprites within a group. This is achieved by adding or subtracting the window's width or height from the sprites x-position or y-position, respecively.
    
    ### Parameters
        - spriteGroup (``pygame.sprite.Group``): The group to relocate
        - direction (``str``): The direction of the room where ``spriteGroup`` should be relocated
    """    
    if direction == DOWN:
        for sprite in spriteGroup:
            sprite.changeRoomDown()

    if direction == RIGHT:
        for sprite in spriteGroup:
            sprite.changeRoomRight()

    if direction == UP:
        for sprite in spriteGroup:
            sprite.changeRoomUp()

    if direction == LEFT:
        for sprite in spriteGroup:
            sprite.changeRoomLeft()

def objectAccel(sprite):
    """Defines the relationship between acceleration, velocity, and position (and time, when called once every frame)
    
    ### Parameters
        - ``sprite`` ``(pygame.sprite.Sprite)``: The sprite that should follow the acceleration logic
    """    
    sprite.accel.x += sprite.vel.x * FRIC
    sprite.accel.y += sprite.vel.y * FRIC
    sprite.vel += sprite.accel * dt
    sprite.pos += sprite.vel + sprite.accel_const * sprite.accel

#------------------------------ Player class ------------------------------#
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
        self.gun_speed = 12
        self.gun_cooldown = 6
        self.hitTime_charge = 1200
        self.hitTime = 0
        self.lastHit = time.time()

        self.updateMaxStats()

        self.menu = InventoryMenu()
        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)

        self.inventory = {}
        for item in MAT.values():
            self.inventory.update({item: 0})

    def changeRoomRight(self):
        """Relocates the player one room to the right. This ``kill()``s all projectiles and explosions in the current room."""        
        room.room.x += 1
        room.layoutUpdate()
        
        self.pos.x -= WIN_WIDTH
        groupChangeRooms(all_portals, RIGHT)
        
        killGroup(all_projs, all_explosions)

    def changeRoomLeft(self):
        """Relocates the player one room to the left. This ``kill()``s all projectiles and explosions in the current room."""   
        room.room.x -= 1
        room.layoutUpdate()

        self.pos.x += WIN_WIDTH
        groupChangeRooms(all_portals, LEFT)

        killGroup(all_projs, all_explosions)

    def changeRoomUp(self):
        """Relocates the player one room up. This ``kill()``s all projectiles and explosions in the current room."""   
        room.room.y += 1
        room.layoutUpdate()

        self.pos.y += WIN_HEIGHT
        groupChangeRooms(all_portals, UP)

        killGroup(all_projs, all_explosions)

    def changeRoomDown(self):
        """Relocates the player one room down. This ``kill()``s all projectiles and explosions in the current room."""   
        room.room.y -= 1
        room.layoutUpdate()

        self.pos.y -= WIN_HEIGHT
        groupChangeRooms(all_portals, DOWN)

        killGroup(all_projs, all_explosions)

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

    def updateMaxStats(self):
        """Updates all of the player's max stats."""        
        self.max_hp = floor(50 * pow(1.009290219, self.level))
        self.max_attack = floor(10 * pow(1.019580042, self.level))
        self.max_defense = floor(15 * pow(1.016098331, self.level))

    def checkRoomChange(self):
        if self.pos.x <= 0:
            hideCurrentEnemies()
            self.changeRoomLeft()

        if self.pos.x >= WIN_WIDTH:
            hideCurrentEnemies()
            self.changeRoomRight()

        if player1.pos.y <= 0:
            hideCurrentEnemies()
            self.changeRoomUp()

        if player1.pos.y >= WIN_HEIGHT:
            hideCurrentEnemies()
            self.changeRoomDown()

class Player(PlayerBase):
    def __init__(self):
        """A player sprite that can move and shoot."""        
        super().__init__()
        all_players.add(self)
        self.show(LAYERS['player_layer'])

        self.spritesheet = Spritesheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(200, 400, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.bulletType = PROJ_P_STD
        
        self.can_fire_portal = False

    def movement(self):
        """When called once every frame, it allows the player to recive input from the user and move accordingly
        """        
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
            
            if isInputHeld[K_x] == True:
                self.accel_const = 1.04
            if isInputHeld[K_x] == False:
                self.accel_const = 0.52

            objectAccel(self)

            self.rect.center = self.pos
            self.hitbox.center = self.pos

    def shoot(self, vel):
        """Shoots a bullet
        
        ### Parameters
            - vel ``(float)``: The velocity the bullet will travel with
        """        
        angle_to_mouse = getAngleToMouse(self)

        velX = vel * -sin(rad(angle_to_mouse))
        velY = vel * -cos(rad(angle_to_mouse))

        if isInputHeld[1] and self.bulletType == PROJ_P_STD and anim_timer % self.gun_cooldown == 0:
            offset = vec((21, 30))
            players_projs.add(
                Projectile(self,
                    self.pos.x - (offset.x * cos(rad(angle_to_mouse))) - (offset.y * sin(rad(angle_to_mouse))),
                    self.pos.y + (offset.x * sin(rad(angle_to_mouse))) - (offset.y * cos(rad(angle_to_mouse))),
                    velX, velY, self.bulletType
                ),
                
                Projectile(self,
                    self.pos.x + (offset.x * cos(rad(angle_to_mouse))) - (offset.y * sin(rad(angle_to_mouse))),
                    self.pos.y - (offset.x * sin(rad(angle_to_mouse))) - (offset.y * cos(rad(angle_to_mouse))),
                    velX, velY, self.bulletType
                )
            )

        if keyReleased[3] % 2 == 0 and self.can_fire_portal:
            players_projs.add(Projectile(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75, PROJ_P_PORTAL))
            self.can_fire_portal = False

        elif keyReleased[3] % 2 != 0 and not self.can_fire_portal:
            players_projs.add(Projectile(self, self.pos.x, self.pos.y, velX * 0.75, velY * 0.75, PROJ_P_PORTAL))
            self.can_fire_portal = True

    def update(self):
        global anim_timer
        if can_update:
            if anim_timer % 5 == 0:
                if isInputHeld[1] == True:
                    if self.index == 4:
                        self.index = 0
                    self.index += 1
                else: # Idle animation
                    self.index = 0
            
            if self.hitTime < self.hitTime_charge:
                self.hitTime += 1

            self.original_image = self.original_images[self.index]
            self.image = pygame.transform.rotate(self.original_image, int(getAngleToMouse(self)))
            self.rect = self.image.get_rect(center = self.rect.center)

        # Gameplay
        self.updateLevel()
        self.updateMaxStats()
        
        if self.hp <= 0:
            self.kill()

#------------------------------ Enemy classes ------------------------------#
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

    def dropItems(self, table_index):
        drops = LTDROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)
        
        for item in drops[row][column]:
            ItemDrop(self, item)
            print(item)

class StandardGrunt(EnemyBase):
    def __init__(self, posX, posY):
        """A simple enemy that moves to random locations and shoots at random intervals

        Parameters
        ----------
        posX : float
            The x-position to spawn at
        posY : float
            The y-position to spawn at
        roomX : int
            The room's x-axis location in the grid of the room layout
        roomY : int
            The room's y-axis location in the grid of the room layout
        hp : int
            The maximum starting hp
        attack : int
            Attack value
        defense : int
            Defense value
        xp_worth : int
            The amount of XP a player will gain after defeating this enemy
        accel_const : float
            The acceleration constant
        """        
        super().__init__()
        all_sprites.add(self, layer = LAYERS['enemy_layer'])
        all_enemies.add(self)

        self.spritesheet = Spritesheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        #---------------------- Physics ----------------------#
        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(0, WIN_WIDTH), rand.randint(0, WIN_HEIGHT))

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 15, 10, 10, 25, 0.4)
        self.healthBar = HealthBar(self)

    def movement(self, canShoot):
        if self.hp > 0 and self.visible == True and can_update:
            global anim_timer
            if anim_timer % rand.randint(150, 200) == 0:
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, WIN_WIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, WIN_HEIGHT - self.image.get_height() - 64)

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

            objectAccel(self)
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 5, rand.randint(20, 30), PROJ_P_STD)
            else:
                pass

    def shoot(self, target, vel, shoot_time, bulletType):
        global anim_timer
        if anim_timer % shoot_time == 0 and self.hp > 0:
            self.is_shooting = True
            try:
                angle_to_target = getAngleToSprite(self, target)
            except:
                angle_to_target = 0

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            enemy_projs.add(Projectile(self, self.pos.x - (21 * cos(rad(angle_to_target))) - (30 * sin(rad(angle_to_target))), self.pos.y + (21 * sin(rad(angle_to_target))) - (30 * cos(rad(angle_to_target))), vel_x, vel_y, bulletType))

    def update(self):
        self.movement(True)
        global anim_timer
        if anim_timer % 5 == 0:
            if self.is_shooting == True:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.is_shooting = False

        # self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        # Rotate sprite to player
        self.image = pygame.transform.rotate(self.original_image, int(getAngleToSprite(self, getClosestPlayer(self))))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox.center = self.pos

        # Kill enemy if their HP reaches 0
        if self.hp <= 0:
            self.dropItems(0)
            awardXp(self)
            self.kill()

class OctoGrunt(EnemyBase):
    def __init__(self, posX, posY):
        super().__init__()
        all_sprites.add(self, layer = LAYERS['enemy_layer'])
        all_enemies.add(self)

        self.spritesheet = Spritesheet("sprites/enemies/octogrunt.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(0, WIN_WIDTH), rand.randint(0, WIN_HEIGHT))

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 44, 10, 10, 45, 0.4)
        self.healthBar = HealthBar(self)

    def movement(self, canShoot):
        if self.hp > 0 and self.visible and can_update:
            objectAccel(self)

            global anim_timer
            if anim_timer % rand.randint(250, 300) == 0:
                self.rand_pos.x = rand.randint(0, WIN_WIDTH)
                self.rand_pos.y = rand.randint(0, WIN_HEIGHT)

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
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 5, 80, PROJ_P_STD)
            else:
                pass

    def shoot(self, target, vel, shoot_time, bulletType):
        global anim_timer
        if anim_timer % shoot_time == 0 and self.hp > 0:
            self.is_shooting = True
            angle_to_target = getAngleToSprite(self, target)

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            OFFSET = 21

            enemy_projs.add(
                Projectile(self, self.pos.x - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel_x, vel_y, bulletType),
                Projectile(self, self.pos.x + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))), -vel_x, -vel_y, bulletType),

                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90)), bulletType, ),
                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 90)), -vel * -cos(rad(angle_to_target + 90)), bulletType),

                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 45)), vel * -cos(rad(angle_to_target + 45)), bulletType),
                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 45)), -vel * -cos(rad(angle_to_target + 45)), bulletType),

                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target - 45)), vel * -cos(rad(angle_to_target - 45)), bulletType),
                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target - 45)), -vel * -cos(rad(angle_to_target - 45)), bulletType),
            )

    def update(self):
        self.movement(True)
        global anim_timer
        if anim_timer % 5 == 0:
            if self.is_shooting == True:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.is_shooting = False
                else:
                    pass
            else:
                pass

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        # Rotate sprite to player
        self.image = pygame.transform.rotate(self.original_image, int(getAngleToSprite(self, getClosestPlayer(self))))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox.center = self.pos

        # Kill enemy if their HP reaches 0
        if self.hp <= 0:
            self.dropItems(1)
            awardXp(self)
            self.kill()

class Ambusher(EnemyBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show(LAYERS['enemy_layer'])
        all_enemies.add(self)

        self.spritesheet = Spritesheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.get_images(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        #---------------------- Physics ----------------------#
        self.pos = vec((posX, posY))
        
        self.last_dash = time.time()

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 15, 10, 10, 25, 0.4)
        self.healthBar = HealthBar(self)

    def movement(self, canShoot):
        if self.hp > 0 and self.visible:
            if time.time() - self.last_dash > 3:
                target = getClosestPlayer(self)
                self.image = self.images[self.index]
                self.original_image = self.original_images[self.index]

                self.last_dash = time.time()
            objectAccel(self)

    def update(self):
        self.movement(False)

        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox.center = self.pos

        # Kill enemy if their HP reaches 0
        if self.hp <= 0:
            self.dropItems(1)
            awardXp(self)
            self.kill()

#------------------------------ Interactible classes ------------------------------#
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
        self.movement()
        if self.hitbox.colliderect(player1):
            player1.inventory[self.mat] += 1
            self.kill()

#------------------------------ Projectile class ------------------------------#
class Projectile(pygame.sprite.Sprite):
    def __init__(self, shotFrom, posX, posY, velX, velY, bulletType):
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

        self.visible = True

        all_sprites.add(self, layer = LAYERS['proj_layer'])
        all_projs.add(self)

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.type = bulletType
        self.hitbox_adjust = vec(0, 0)

        if self.type == PROJ_P_STD:
            self.hitbox_adjust = vec(-2, -2)
            self.damage = PROJS[PROJ_P_STD]

        elif self.type == PROJ_P_PORTAL:
            self.hitbox_adjust = vec(0, 0)
            self.damage = PROJS[PROJ_P_PORTAL]

        else:
            self.hitbox_adjust = vec(0, 0)
            self.damage = 0

        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(-24, -24, 8, 8)
        self.hitbox = self.rect.inflate(self.hitbox_adjust.x, self.hitbox_adjust.y)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        # Rotate sprite to trajectory
        self.image = pygame.transform.rotate(self.original_image, int(getVecAngle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.shotFrom = shotFrom
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def teleport(self, portal_in):
        teleportProj(self, portal_in)

    def land(self):
        all_explosions.add(ProjExplode(self))
        self.kill()

    def update(self):
        if self.type == PROJ_P_STD:
            self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.hitbox_adjust = vec(-8, -8)

        if self.type == PROJ_P_PORTAL:
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

#------------------------------ Portal class ------------------------------#
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
            self.hitbox = self.rect.inflate(0, -50)
        if self.facing == RIGHT:
            self.image = pygame.transform.rotate(self.image, 90)
            self.hitbox = self.rect.inflate(-50, 0)
        if self.facing == UP:
            self.image = pygame.transform.rotate(self.image, 180)
            self.hitbox = self.rect.inflate(0, -50)
        if self.facing == LEFT:
            self.image = pygame.transform.rotate(self.image, 270)
            self.hitbox = self.rect.inflate(-50, 0)
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
    if wall.pos.x - 0.5 * wall.image.get_width() <= portal.pos.x <= wall.pos.x + 0.5 * wall.image.get_width() and portal.pos.y > wall.pos.y:
        return DOWN
    
    elif wall.pos.x - 0.5 * wall.image.get_width() <= portal.pos.x <= wall.pos.x + 0.5 * wall.image.get_width() and portal.pos.y < wall.pos.y:
        return UP

    elif wall.pos.y - 0.5 * wall.image.get_height() <= portal.pos.y <= wall.pos.y + 0.5 * wall.image.get_height() and portal.pos.x > wall.pos.x:
        return RIGHT
    
    elif wall.pos.y - 0.5 * wall.image.get_height() <= portal.pos.y <= wall.pos.y + 0.5 * wall.image.get_height() and portal.pos.x < wall.pos.x:
        return LEFT
    
    else:
        return None

#------------------------------ Bullet explosion class ------------------------------#
class ProjExplode(pygame.sprite.Sprite):
    def __init__(self, proj):
        """An explosion/shattering that is displayed on-screen when a projectile hits something

        Parameters:
        --------
            proj (pygame.sprite.Sprite): The projectile that is exploding
        """
        super().__init__()
        all_sprites.add(self, layer = LAYERS['explosion_layer'])

        self.proj = proj
        self.type = self.proj.type
        
        self.spritesheet = Spritesheet("sprites/bullets/bullets.png")
        self.index = 1

        if self.type == PROJ_P_STD:
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)

        elif self.type == PROJ_P_PORTAL:
            self.images = self.spritesheet.get_images(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.get_images(0, 0, 32, 32, 4)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        self.rect = self.proj.rect
        self.randRotation = rand.randint(1, 360)

        self.pos = self.proj.pos

    def update(self):
        global anim_timer
        if self.type == PROJ_P_STD or self.type == PROJ_E_STD:
            if anim_timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1

        elif self.type == PROJ_P_PORTAL:
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

#------------------------------ Wall class ------------------------------#
class Wall(WallBase):
    def __init__(self, topleftX_mult, topleftY_mult, widthMult, heightMult):
        super().__init__()
        all_sprites.add(self, layer = LAYERS['wall_layer'])
        all_walls.add(self)

        self.visible = True

        self.image = pygame.Surface((32 * widthMult, 32 * heightMult))
        self.texture = pygame.image.load("sprites/textures/wall.png")
        textureWall(self, self.texture)

        self.pos = getTopLeftCoordinates(self, topleftX_mult * 32, topleftY_mult * 32)
        self.rect.center = self.pos

    def update(self):
        self.rect.center = self.pos

#------------------------------ Room class ------------------------------#
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
            )

            # Search for an enemy container for this room
            try:
                container = next(c for c in all_containers if c.room == self.room)
                showEnemies(container)

            except StopIteration:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        Box(800, WIN_HEIGHT / 2),
                        Ambusher(500, 500)
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
                Wall(28, 4, 4, 4)
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

#------------------------------ UI classes ------------------------------#
class InventoryMenu(AbstractBase):
    def __init__(self):
        """A menu used to view collected items and utilize them for various purposes
        
        ### Parameters
            - ``owner`` ``(pygame.sprite.Sprite)``: The player whom the inventory belongs to
        """        
        super().__init__()
        self.last_time = time.time()
        
        self.add(
            RightMenuArrow(WIN_WIDTH - 16, WIN_HEIGHT / 2),
            LeftMenuArrow(80, WIN_HEIGHT / 2),
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
            can_update = False

        elif keyReleased[K_e] % 2 == 0 and keyReleased[K_e] > 0:
            self.hide()
            can_update = True

class RightMenuArrow(pygame.sprite.Sprite):
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
        
        self.rect = pygame.Rect(posX - 32, posY - 32, 128, 128)
        self.hitbox = pygame.Rect(posX - 32, posY - 32, 128, 128)

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

class LeftMenuArrow(pygame.sprite.Sprite):
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
        
        self.rect = pygame.Rect(posX - 32, posY - 32, 128, 128)
        self.hitbox = pygame.Rect(posX - 32, posY - 32, 128, 128)

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
            if self.index >= 61:
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
        self.count = player1.inventory[self.holding]
        self.images = self.createSlotImages()
        self.hover()

#------------------------------ Font class ------------------------------#
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
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos

    def update(self):
        global anim_timer
        if time.time() - self.start_time > 0.75:
            self.kill()

#------------------------------ Redraw game window ------------------------------#
def projectileCollide(entityGroup, proj, canHurt):
    """Destroys a given projectile upon a collision and renders an explosion
    
    ### Parameters
        - entityGroup (``pygame.sprite.Group``): The group of the entity the projectile is colliding with
        - proj (``pygame.sprite.Sprite``): The projectile involved in the collision
        - canHurt (``bool``): Should the projectile calculate damage upon impact?
    """    
    for colliding_entity in entityGroup:
        if not proj.hitbox.colliderect(colliding_entity.hitbox):
            continue
        
        if not colliding_entity.visible:
            continue

        if canHurt:
            if entityGroup == all_enemies:
                if rand.randint(1, 20) == 1:
                    colliding_entity.hp -= (calculateDamage(proj.shotFrom, colliding_entity, proj)) * 3
                    all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, 3 * calculateDamage(proj.shotFrom, colliding_entity, proj)))
                else:
                    colliding_entity.hp -= calculateDamage(proj.shotFrom, colliding_entity, proj)
                    all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(proj.shotFrom, colliding_entity, proj)))
                proj.land()

            elif entityGroup != all_enemies:
                colliding_entity.hp -= calculateDamage(proj.shotFrom, colliding_entity, proj)
                all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(proj.shotFrom, colliding_entity, proj)))
                if hasattr(colliding_entity, 'hitTime'):
                    colliding_entity.hitTime = 0
                    colliding_entity.lastHit = time.time()
                proj.land()

        elif not canHurt:
            if proj.type != PROJ_P_PORTAL:
                # If the projectile hits a portal
                if entityGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if proj.hitbox.colliderect(portal.hitbox):
                                proj.teleport(portal)
                        proj.kill()
                        return
                    
                    elif len(all_portals) < 2:
                        proj.kill()
                        return
                    
                # If the projectile isn't a portal and hits anything but a portal
                elif entityGroup != all_portals:
                    proj.land()

            elif proj.type == PROJ_P_PORTAL:
                if entityGroup == all_walls:
                    side = portalSideCheck(colliding_entity, proj)
                    if side == DOWN or side == UP:
                        if proj.pos.x - 32 > colliding_entity.pos.x - 0.5 * colliding_entity.image.get_width() and proj.pos.x + 32 < colliding_entity.pos.x + 0.5 * colliding_entity.image.get_width():
                            all_portals.add(Portal(proj.pos.x, proj.pos.y, side))
                            portalCountCheck()
                    elif side == RIGHT or side == LEFT:
                        if proj.pos.y - 32 > colliding_entity.pos.y - 0.5 * colliding_entity.image.get_height() and proj.pos.y + 32 < colliding_entity.pos.y + 0.5 * colliding_entity.image.get_height():
                            all_portals.add(Portal(proj.pos.x, proj.pos.y, side))
                            portalCountCheck()
                    proj.land()
                # If a portal hits anything but a wall
                else:
                    proj.land()

def bindProjectile(projectile, projTargetGroup):
    """Binds a projectile to its shooter and confines it to the window borders
    
    ### Parameters
        - projectile (``pygame.sprite.Sprite``): The projectile to bind
        - projTargetGroup (``pygame.sprite.Group``): The group of the projectile from which it was shot from (ex. ``players_proj``)
    """    
    if (
        projectile.pos.x < WIN_WIDTH and 
        projectile.pos.x > 0 and
        projectile.pos.y < WIN_HEIGHT and 
        projectile.pos.y > 0
    ):
        projectile.movement()
    else:
        projectile.kill()

    projectileCollide(projTargetGroup, projectile, True)
    projectileCollide(all_walls, projectile, False)
    projectileCollide(all_portals, projectile, False)

def redrawGameWindow():
    """Draws all entities every frame"""
    if can_update:
        # Updating players
        for a_player in all_players:
            collideCheck(a_player, enemy_projs)
            collideCheck(a_player, all_walls)
            collideCheck(a_player, all_movable)

            a_player.movement()
            a_player.shoot(a_player.gun_speed)
            a_player.checkRoomChange()

            # Teleport the player if they come into contact with a portal
            for portal in all_portals:
                if a_player.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                    tpLocation(a_player, portal)

        # Updating enemies
        for enemy in all_enemies:
            if enemy.visible:
                collideCheck(enemy, all_players,)
                collideCheck(enemy, players_projs)
                collideCheck(enemy, all_walls)

        # Updating movable objects
        for object in all_movable:
            object.movement()

        # Updating all item drops
        for item in all_drops:
            collideCheck(item, all_walls)

        # Updating player projectiles
        for projectile in players_projs:
            bindProjectile(projectile, all_enemies)

        # Updating enemy projectiles
        for projectile in enemy_projs:
            bindProjectile(projectile, all_players)

        # Updating UI
        for statBar in all_stat_bars:
            statBar.movement()

        # Updating walls
        for wall in all_walls:
            pass

        # Updating portals
        for portal in all_portals:
            pass

        # Updating all font characters
        for char in all_font_chars:
            char.movement()

    # Updating inventory
    player1.menu.update()

    all_sprites.update()
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

        checkKeyRelease(False, K_e)
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