import pygame
from pygame.locals import *
import sys, math, time
import random as rand

from math import sin, cos, tan, radians

from spritesheet import *
from constants import *
from calculateStats import *
from calculations import *

pygame.init()

# Aliases
vec = pygame.math.Vector2
spriteGroup = pygame.sprite.Group
rad = radians

clock = pygame.time.Clock()

screenSize = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED)
pygame.display.set_caption('Orbeeto')

all_sprites = pygame.sprite.LayeredUpdates()
all_players = spriteGroup()
all_enemies = spriteGroup()

all_stat_bars = spriteGroup()

all_projectiles = spriteGroup()
players_projectiles = spriteGroup()
enemy_projectiles = spriteGroup()
all_explosions = spriteGroup()
all_portals = spriteGroup()

all_walls = spriteGroup()
all_rooms = []

def getClosestPlayer(selfEntity):
    """Returns the closest player entity from another given entity

    Args:
        selfEntity (pygame.sprite.Sprite): The entity to locate the closest player from

    Returns:
        pygame.sprite.Sprite: The closest player entity to selfEntity
    """
    playerCoords = {}
    for a_player in all_players:
        playerCoords[a_player] = get_dist_to_entity(selfEntity, a_player)

    temp = min(playerCoords.values())
    result = [key for key in playerCoords if playerCoords[key] == temp]
    
    return result[0]

def awardXp(enemy):
    """Give all players an enemy's xp worth after it is killed

    Args:
        enemy (pygame.sprite.Sprite): The enemy that has been killed
    """
    for a_player in all_players:
        a_player.xp += enemy.xp_worth

def teleportLocation(a_player, portal_in):
    """Teleports a player between portals given the portal the player is entering

    Args:
        a_player (pygame.sprite.Sprite): The player entering the portal
        portal_in (pygame.sprite.Sprite): The portal the player is entering
    """    
    for portal in all_portals:
        if portal != portal_in:
            other_portal = portal
            
    if other_portal.facing == DOWN:
        a_player.pos.x = other_portal.pos.x
        a_player.pos.y = other_portal.pos.y + other_portal.hitbox.height + a_player.hitbox.height * 0.5
        # a_player.accel = vec(0, 0)
        a_player.vel = vec(0, 0)

    elif other_portal.facing == RIGHT:
        a_player.pos.x = other_portal.pos.x + other_portal.hitbox.width + a_player.hitbox.width * 0.5
        a_player.pos.y = other_portal.pos.y
        # a_player.accel = vec(0, 0)
        a_player.vel = vec(0, 0)

    elif other_portal.facing == UP:
        a_player.pos.x = other_portal.pos.x
        a_player.pos.y = other_portal.pos.y - other_portal.hitbox.height - a_player.hitbox.height * 0.5
        # a_player.accel = vec(0, 0)
        a_player.vel = vec(0, 0)

    elif other_portal.facing == LEFT:
        a_player.pos.x = other_portal.pos.x - other_portal.hitbox.width - a_player.hitbox.width * 0.5
        a_player.pos.y = other_portal.pos.y
        # a_player.accel = vec(0, 0)
        a_player.vel = vec(0, 0)

def distFromCenterPortal(proj, portal_in):
    if portal_in.facing == DOWN or portal_in.facing == UP:
        return proj.pos.x - portal_in.pos.x
    if portal_in.facing == RIGHT or portal_in.facing == LEFT:
        return proj.pos.y - portal_in.pos.y

def teleportProjectile(proj, portalIn):
    for portal in all_portals:
        if portal != portalIn:
            portalOut = portal

    projGroup = players_projectiles

    if portalIn.facing == DOWN:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y + 8, proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + distFromCenterPortal(proj, portalIn), -proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y - 8, proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + distFromCenterPortal(proj, portalIn), proj.vel.y, proj.vel.x, proj.type))

    if portalIn.facing == RIGHT:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y + 8, proj.vel.y, -proj.vel.x, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + distFromCenterPortal(proj, portalIn), -proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y - 8, -proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + distFromCenterPortal(proj, portalIn), proj.vel.x, proj.vel.y, proj.type))

    if portalIn.facing == UP:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y + 8, proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + distFromCenterPortal(proj, portalIn), proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y - 8, -proj.vel.x, -proj.vel.y, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + distFromCenterPortal(proj, portalIn), -proj.vel.y, proj.vel.x, proj.type))

    if portalIn.facing == LEFT:
        if portalOut.facing == DOWN:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y + 8, proj.vel.y, proj.vel.x, proj.type))
        if portalOut.facing == RIGHT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + 8, portalOut.pos.y + distFromCenterPortal(proj, portalIn), proj.vel.x, proj.vel.y, proj.type))
        if portalOut.facing == UP:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x + distFromCenterPortal(proj, portalIn), portalOut.pos.y - 8, proj.vel.y, -proj.vel.x, proj.type))
        if portalOut.facing == LEFT:
            projGroup.add(Projectile(proj.shotFrom, portalOut.pos.x, portalOut.pos.y + distFromCenterPortal(proj, portalIn), proj.vel.x, proj.vel.y, proj.type))

def objectAccel(object):
    """Defines accelearion for any object's movement

    Args:
        object (pygame.sprite.Sprite): Any sprite object
    """    
    object.accel.x += object.vel.x * FRIC * dt
    object.accel.y += object.vel.y * FRIC * dt
    object.vel += object.accel * dt
    object.pos += (object.vel + object.accel_const * object.accel) * dt

#------------------------------ Player class ------------------------------#
class PlayerBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = vec((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.roomCoords = vec((0, 0))
        self.isChangingRooms = False

        # Game stats
        self.xp = 0
        self.level = 0
        self.max_hp = 75
        self.hp = 75
        self.max_attack = 10
        self.attack = 10
        self.max_defense = 15
        self.defense = 15
        self.gun_speed = 12
        self.gun_cooldown = 6
        self.hitTime_charge = 1200
        self.hitTime = 0

        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)

    def changeRoomRight(self):
        self.pos.x -= WINDOW_WIDTH + 1
        
        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

        for portal in all_portals:
            portal.changeRoomRight()

        for proj in all_projectiles:
            proj.kill()

        for boom in all_explosions:
            boom.kill()

    def changeRoomLeft(self):
        self.pos.x += WINDOW_WIDTH + 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

        for portal in all_portals:
            portal.changeRoomLeft()

        for proj in all_projectiles:
            proj.kill()

        for boom in all_explosions:
            boom.kill()

    def changeRoomUp(self):
        self.pos.y += WINDOW_HEIGHT + 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

        for portal in all_portals:
            portal.changeRoomUp()

        for proj in all_projectiles:
            proj.kill()

        for boom in all_explosions:
            boom.kill()

    def changeRoomDown(self):
        self.pos.y -= WINDOW_HEIGHT - 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

        for portal in all_portals:
            portal.changeRoomDown()

        for proj in all_projectiles:
            proj.kill()

        for boom in all_explosions:
            boom.kill()

class Player(PlayerBase):
    def __init__(self, hitbox_adjustX, hitbox_adjustY):
        super().__init__()
        all_sprites.add(self, layer = 1)
        all_players.add(self)

        self.accel_const = 0.52

        self.spritesheet = SpriteSheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(200, 400, 64, 64)
        self.hitbox = self.rect.inflate(hitbox_adjustX, hitbox_adjustY)

    def movement(self):
        self.accel = vec(0, 0)
        if is_a_held == True:
            self.accel.x = -self.accel_const * dt
        if is_d_held == True:
            self.accel.x = self.accel_const * dt
        if is_s_held == True:
            self.accel.y = self.accel_const * dt
        if is_w_held == True:
            self.accel.y = -self.accel_const * dt
        
        if is_x_held == True:
            self.accel_const = 1.04
        if is_x_held == False:
            self.accel_const = 0.52

        objectAccel(self)

        self.rect.center = self.pos
        self.hitbox.center = self.pos

        # When beyond window borders
        if self.pos.x >= WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH
        if self.pos.x <= 0:
            self.pos.x = 0

        if self.pos.y >= WINDOW_HEIGHT:
            self.pos.y = WINDOW_HEIGHT
        if self.pos.y <= 0:
            self.pos.y = 0

    def teleport(self, portal_in):
        teleportLocation(self, portal_in)

    def shoot(self, vel, cannonSide, bulletType=PROJ_P_STD):
        angle_to_mouse = get_angle_to_mouse(self)

        vel_x = vel * -sin(rad(angle_to_mouse))
        vel_y = vel * -cos(rad(angle_to_mouse))

        if is_leftMouse_held == True:
            if timer % a_player.gun_cooldown == 0:
                players_projectiles.add(
                    Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType),
                    Projectile(self, self.pos.x + (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y - (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType)
                )

        elif cannonSide == SHOOT_MIDDLE:
            players_projectiles.add(Projectile(self, self.pos.x, self.pos.y, vel_x, vel_y, bulletType))

    def update(self):
        global timer
        if timer % 5 == 0:
            global is_leftMouse_held
            if is_leftMouse_held == True:
                if self.index == 4:
                    self.index = -1
                self.index += 1
            else: # Idle animation
                self.index = 0
        
        if self.hitTime < self.hitTime_charge:
            self.hitTime += 1

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.image = pygame.transform.rotate(self.original_image, int(get_angle_to_mouse(self)))
        self.rect = self.image.get_rect(center = self.rect.center)

        # Gameplay
        updateLevel(self)
        if self.hp <= 0:
            self.kill()

#------------------------------ Enemy classes ------------------------------#
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = vec((0, 0))
        
        self.is_shooting = False

        self.healthBar = HealthBar(self)

    def changeRoomRight(self):
        self.kill()

    def changeRoomLeft(self):
        self.kill()

    def changeRoomUp(self):
        self.kill()

    def changeRoomDown(self):
        self.kill()

class StandardGrunt(EnemyBase):
    def __init__(self, posX, posY, hp, attack, defense, xp_worth, accel_const):
        """A simple enemy that moves to random locations and shoots at random intervals

        Args:
            posX (float): x-position to spawn at
            posY (float): y-position to spawn at
            hp (int): Maximum health points
            attack (int): Attack value
            defense (int): Defense value
            xp_worth (int): XP to gain by defeating this enemy
            accel_const (float): Acceleration constant
        """        
        super().__init__()
        all_sprites.add(self, layer = 1)
        all_enemies.add(self)

        self.spritesheet = SpriteSheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.accel_const = accel_const

        self.roomCoords = vec((0, 0))

        self.pos = vec((posX + (self.roomCoords.x * WINDOW_WIDTH), posY + (self.roomCoords.y * WINDOW_HEIGHT)))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.rand_pos = vec(rand.randint(0, WINDOW_WIDTH), rand.randint(0, WINDOW_HEIGHT))

        # Game stats
        self.max_hp = hp
        self.hp = self.max_hp
        self.max_attack = attack
        self.attack = self.max_attack
        self.max_defense = defense
        self.defense = self.max_defense
        self.xp_worth = xp_worth

    def rand_movement(self, canShoot):
        if self.hp > 0:
            objectAccel(self)

            global timer
            if timer % rand.randint(150, 200) == 0:
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, WINDOW_WIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, WINDOW_HEIGHT - self.image.get_height() - 64)

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
                self.shoot(getClosestPlayer(self), 5, rand.randint(20, 30), PROJ_P_STD)
            else:
                pass

    def shoot(self, target, vel, shoot_time, bulletType):
        global timer
        if timer % shoot_time == 0 and self.hp > 0:
            self.is_shooting = True
            angle_to_mouse = get_angle_to_entity(self, target)

            vel_x = vel * -sin(rad(angle_to_mouse))
            vel_y = vel * -cos(rad(angle_to_mouse))

            enemy_projectiles.add(Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType))

    def update(self):
        global timer
        if timer % 5 == 0:
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
        self.image = pygame.transform.rotate(self.original_image, int(get_angle_to_entity(self, getClosestPlayer(self))))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox.center = self.pos

        # Kill enemy if their HP reaches 0
        if self.hp <= 0:
            awardXp(self)
            self.kill()

class OctoGrunt(EnemyBase):
    def __init__(self, posX, posY, hp, attack, defense, xp_worth, accel_const):
        super().__init__()
        all_sprites.add(self, layer = 1)
        all_enemies.add(self)

        self.spritesheet = SpriteSheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.accel_const = accel_const

        self.roomCoords = vec((0, 0))

        self.pos = vec((posX + (self.roomCoords.x * WINDOW_WIDTH), posY + (self.roomCoords.y * WINDOW_HEIGHT)))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.rand_pos = vec(rand.randint(0, WINDOW_WIDTH), rand.randint(0, WINDOW_HEIGHT))

        # Game stats
        self.max_hp = hp
        self.hp = self.max_hp
        self.max_attack = attack
        self.attack = self.max_attack
        self.max_defense = defense
        self.defense = self.max_defense
        self.xp_worth = xp_worth

    def rand_movement(self, canShoot):
        if self.hp > 0:
            objectAccel(self)

            global timer
            if timer % rand.randint(250, 300) == 0:
                self.rand_pos.x = rand.randint(0, WINDOW_WIDTH)
                self.rand_pos.y = rand.randint(0, WINDOW_HEIGHT)

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
                self.shoot(getClosestPlayer(enemy), 5, 80, PROJ_P_STD)
            else:
                pass

    def shoot(self, target, vel, shoot_time, bulletType):
        global timer
        if timer % shoot_time == 0 and self.hp > 0:
            self.is_shooting = True
            angle_to_target = get_angle_to_entity(self, target)

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            OFFSET = 21

            enemy_projectiles.add(
                Projectile(self, self.pos.x - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel_x, vel_y, bulletType),
                Projectile(self, self.pos.x + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))), -vel_x, -vel_y, bulletType),

                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90)), bulletType),
                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 90)), -vel * -cos(rad(angle_to_target + 90)), bulletType),

                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 45)), vel * -cos(rad(angle_to_target + 45)), bulletType),
                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 45)), -vel * -cos(rad(angle_to_target + 45)), bulletType),

                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target - 45)), vel * -cos(rad(angle_to_target - 45)), bulletType),
                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target - 45)), -vel * -cos(rad(angle_to_target - 45)), bulletType),
            )

    def update(self):
        global timer
        if timer % 5 == 0:
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
        self.image = pygame.transform.rotate(self.original_image, int(get_angle_to_entity(self, getClosestPlayer(self))))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox.center = self.pos

        # Kill enemy if their HP reaches 0
        if self.hp <= 0:
            awardXp(self)
            self.kill()

#------------------------------ Stat bar classes ------------------------------#
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        all_sprites.add(self, layer = 100)
        all_stat_bars.add(self)
        
        self.spritesheet = SpriteSheet("sprites/stat_bars/health_bar.png", False)
        self.images = self.spritesheet.getImages(0, 0, 128, 16, 18)
        self.original_images = self.spritesheet.getImages(0, 0, 128, 16, 18)
        self.index = 17

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.rect = pygame.Rect(0, 0, 128, 16)
        self.entity = entity
        self.pos = self.entity.pos

    def movement(self):
        self.rect.center = vec(self.entity.pos.x, self.entity.pos.y + 42)
    
    def update(self):
        if self.entity.hp > 0:
            self.index = math.floor((16 * self.entity.hp) / self.entity.max_hp)
            self.image = self.images[self.index]
            self.original_image = self.original_images[self.index]
            self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.index = 17
            self.image = self.images[self.index]
            self.kill()

class DodgeBar(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        all_sprites.add(self, layer = 100)
        all_stat_bars.add(self)

        self.spritesheet = SpriteSheet("sprites/stat_bars/dodge_bar.png", False)
        self.images = self.spritesheet.getImages(0, 0, 128, 16, 18)
        self.original_images = self.spritesheet.getImages(0, 0, 128, 16, 18)
        self.index = 17

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        self.rect = pygame.Rect(0, 0, 128, 16)
        self.entity = entity
        self.pos = self.entity.pos
    
    def movement(self):
        self.rect.center = vec(self.entity.pos.x, self.entity.pos.y + 60)

    def update(self):
        if self.entity.hp > 0:
            if self.entity.hitTime < self.entity.hitTime_charge:
                self.index = math.floor((17 * self.entity.hitTime) / self.entity.hitTime_charge)
                self.image = self.images[self.index]
                self.original_image = self.original_images[self.index]
                self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.index = 17
            self.image = self.images[self.index]
            self.kill()

#------------------------------ Projectile class ------------------------------#
class Projectile(pygame.sprite.Sprite):
    def __init__(self, shotFrom, posX, posY, velX, velY, bulletType, ricochet = False):
        """An object that travels at a specific velocity

        Args:
            shotFrom (pygame.sprite.Sprite): The entity the bullet was shot from
            posX (int): The x-position where the projectile will spawn
            posY (int): The y-position where the projectile will spawn
            velX (int): The x-axis component of the projectile's velocity
            velY (int): The y-axis component of the projectile's velocity
            bulletType (str): The type of projectile to fire
            ricochet (bool): Can the projectile ricochet off walls? Defaults to False.
        """
        super().__init__()
        all_sprites.add(self, layer = 1)
        all_projectiles.add(self)

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.type = bulletType
        self.hitbox_adjust = vec(0, 0)

        if self.type == PROJ_P_STD:
            self.hitbox_adjust = vec(-2, -2)
            self.damage = PROJ_DICT[PROJ_P_STD]

        elif self.type == PROJ_P_PORTAL:
            self.hitbox_adjust = vec(0, 0)
            self.damage = PROJ_DICT[PROJ_P_PORTAL]

        else:
            self.hitbox_adjust = vec(0, 0)
            self.damage = 0

        self.spritesheet = SpriteSheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
        self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(-24, -24, 8, 8)
        self.hitbox = self.rect.inflate(self.hitbox_adjust.x, self.hitbox_adjust.y)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        # Rotate sprite to trajectory
        self.image = pygame.transform.rotate(self.original_image, int(get_vec_angle(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        # Game stats
        self.shotFrom = shotFrom
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def teleport(self, portal_in):
        teleportProjectile(self, portal_in)

    def update(self):
        if self.type == PROJ_P_STD:
            self.spritesheet = SpriteSheet("sprites/bullets/bullets.png")
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.hitbox_adjust = vec(-8, -8)

        if self.type == PROJ_P_PORTAL:
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 5, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 5, 4)
            self.hitbox_adjust = vec(0, 0)
            if timer % 5 == 0:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                else:
                    pass
        
            self.image = self.images[self.index]
            self.original_image = self.original_images[self.index]

            # Rotate sprite to trajectory
            self.image = pygame.transform.rotate(self.original_image, int(get_vec_angle(self.vel.x, self.vel.y)))
            self.rect = self.image.get_rect(center = self.rect.center)

#------------------------------ Portal class ------------------------------#
class PortalBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    def changeRoomRight(self):
        self.pos.x -= WINDOW_WIDTH

    def changeRoomLeft(self):
        self.pos.x += WINDOW_WIDTH

    def changeRoomUp(self):
        self.pos.y += WINDOW_HEIGHT

    def changeRoomDown(self):
        self.pos.y -= WINDOW_HEIGHT

class Portal(PortalBase):
    def __init__(self, posX, posY, facing=DOWN):
        """An intering means of transportation...

        Args:
            posX (int): Spawn location along x-axis
            posY (int): Spawn location along y-axis
            facing (str): Dir. of velocity after being expelled
        """        
        super().__init__()
        all_sprites.add(self, layer = 11)
        
        self.pos = vec((posX, posY))
        self.facing = facing

        self.spritesheet = SpriteSheet("sprites/portals/portals.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 1)
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
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

def portalCountCheck():
    """If there are more than two portals present during gameplay, the oldest one will be deleted to make room for another one
    """    
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

    Args:
        wall (pygame.sprite.Sprite): The wall being hit
        portal (pygame.sprite.Sprite): The projectile that is hitting the wall
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
class BulletExplode(pygame.sprite.Sprite):
    def __init__(self, bullet):
        super().__init__()
        all_sprites.add(self, layer = 1)

        self.bullet = bullet
        self.type = self.bullet.type
        
        self.spritesheet = SpriteSheet("sprites/bullets/bullets.png")
        self.index = 1

        if self.type == PROJ_P_STD:
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        self.rect = self.bullet.rect
        self.randRotation = rand.randint(1, 360)

        self.pos = self.bullet.pos

    def update(self):
        global timer
        if timer % 5 == 0:
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
class Wall(pygame.sprite.Sprite):
    def __init__(self, topleftX_mult, topleftY_mult, widthMult, heightMult):
        super().__init__()
        all_sprites.add(self, layer = 10)
        all_walls.add(self)

        self.image = pygame.Surface((32 * widthMult, 32 * heightMult))
        self.texture = pygame.image.load("sprites/textures/wall.png")
        textureWall(self, self.texture)

        self.pos = getTopLeft(self, topleftX_mult * 32, topleftY_mult * 32)
        self.rect.center = self.pos

    def update(self):
        self.rect.center = self.pos

#------------------------------ Room class ------------------------------#
class Room(pygame.sprite.AbstractGroup):
    def __init__(self, roomCoordsX, roomCoordsY):
        """The room where all the current action (a lot) is taking place

        Args:
            roomCoordsX (int): The room's x-axis location in the grid of the room layout
            roomCoordsY (int): The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        all_rooms.append(self)
        self.roomCoords = vec((roomCoordsX, roomCoordsY))

        self.sprites = spriteGroup()

    def layoutUpdate(self):
        for sprite in self.sprites:
            sprite.kill()
            
        if self.roomCoords == vec(0, 0):
            self.sprites.add(
                Wall(0, 0, 4, 4),
                Wall(36, 0, 4, 4),
                Wall(0, 18.5, 4, 4),
                Wall(36, 18.5, 4, 4),
                OctoGrunt(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 25, 10, 10, 25, 0.3)
            )

        elif self.roomCoords == vec(1, 0):
            self.sprites.add(
                Wall(0, 0, 40, 4),
                Wall(0, 18.5, 40, 4),
                StandardGrunt(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 25, 10, 10, 25, 0.35),
                StandardGrunt(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 25, 10, 10, 50, 0.35)
            )

        elif self.roomCoords == vec(0, 1):
            self.sprites.add(
                Wall(0, 0, 4, 22.5),
                Wall(36, 0, 4, 22.5),
                Wall(8, 4, 4, 4),
                Wall(28, 4, 4, 4)
            )

        self.sprites.draw(screen)

#------------------------------ Redraw game window ------------------------------#
def projectileCollide(entityGroup, projectile, doesShatter, canHurt):
    """Destroys a given projectile upon a collision and renders an explosion

    Args:
        entityGroup (pygame.sprite.Group): The group of the entity the projectile is colliding with
        projectile (pygame.sprite.Sprite): The projectile involved in the collision
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_projectiles)
        canHurt (bool): Should the projectile calculate damage upon impact? Defaults to False.
    """
    for entity in entityGroup:
        if projectile.hitbox.colliderect(entity.hitbox):
            if canHurt == True:
                entity.hp -= calculateDamage(projectile.shotFrom, entity, projectile)
                try:
                    entity.hitTime = 0
                except:
                    pass

            if (
                projectile.type != PROJ_P_PORTAL and
                entityGroup == all_portals and
                len(all_portals) == 2
            ):
                for portal in all_portals:
                    if projectile.hitbox.colliderect(portal.hitbox):
                        projectile.teleport(portal)

            if projectile.type == PROJ_P_PORTAL and entityGroup == all_walls:
                side = portalSideCheck(entity, projectile)
                if side == DOWN or side == UP:
                    if projectile.pos.x - 32 > entity.pos.x - 0.5 * entity.image.get_width() and projectile.pos.x + 32 < entity.pos.x + 0.5 * entity.image.get_width():
                        all_portals.add(Portal(projectile.pos.x, projectile.pos.y, side))
                        portalCountCheck()
                if side == RIGHT or side == LEFT:
                    if projectile.pos.y - 32 > entity.pos.y - 0.5 * entity.image.get_height() and projectile.pos.y + 32 < entity.pos.y + 0.5 * entity.image.get_height():
                        all_portals.add(Portal(projectile.pos.x, projectile.pos.y, side))
                        portalCountCheck()

            if doesShatter == True and projectile.type != PROJ_P_PORTAL:
                all_explosions.add(BulletExplode(projectile))

            projectile.kill()

def bindProjectile(projectile, projGroup, projTargetGroup):
    """Binds a projectile to its shooter and confines it to the window borders

    Args:
        projectile (pygame.sprite.Sprite): The projectile to bind
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_projectiles)
        projTargetGroup (pygame.sprite.Group): The group of the entities that should take damage from the given projectile
    """
    if (
        projectile.pos.x < WINDOW_WIDTH and 
        projectile.pos.x > 0 and
        projectile.pos.y < WINDOW_HEIGHT and 
        projectile.pos.y > 0
    ):
        projectile.movement()
        projectile.update()
    else:
        projectile.kill()

    projectileCollide(projTargetGroup, projectile, True, True)
    projectileCollide(all_walls, projectile, True, False)
    projectileCollide(all_portals, projectile, False, False)
    
def redrawGameWindow():
    """Draws all entities every frame"""
    global timer
    # Drawing all player characters every frame
    for a_player in all_players:
        collideCheck(a_player, all_enemies)
        collideCheck(a_player, enemy_projectiles)
        collideCheck(a_player, all_walls)

        a_player.movement()
        a_player.shoot(12, None)
        a_player.update()

        for portal in all_portals:
            if a_player.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                a_player.teleport(portal)

    # Drawing all enemies every frame
    for enemy in all_enemies:
        collideCheck(enemy, all_players)
        collideCheck(enemy, players_projectiles)
        collideCheck(enemy, all_walls)

        enemy.update()

    # Drawing all players' projectiles every frame
    for projectile in players_projectiles:
        bindProjectile(projectile, players_projectiles, all_enemies)

    # Drawing all enemy projectiles every frame
    for projectile in enemy_projectiles:
        bindProjectile(projectile, enemy_projectiles, all_players)

    # Drawing all explosions every frame
    for bullet in all_explosions:
        bullet.update()

    # Drawing all stat bars every frame
    for statBar in all_stat_bars:
        statBar.movement()
        statBar.update()

    # Drawing all walls every frame
    for wall in all_walls:
        wall.update()

    # Drawing all portals every frame
    for portal in all_portals:
        portal.update()

    all_sprites.draw(screen)
    pygame.display.update()

#------------------------------ Initialing parameters ------------------------------#
player = Player(-32, -32)

# Load rooms
room = Room(0, 0)
room.layoutUpdate()

timer = 0
last_time = time.time()

is_leftMouse_held = False
is_rightMouse_held = False
is_middleMouse_held = False

is_a_held = False
is_w_held = False
is_s_held = False
is_d_held = False

is_x_held = False

loadXpRequirements()

#------------------------------ Main loop ------------------------------#
running = True
while running:
    
    dt = (time.time() - last_time) * 68
    last_time = time.time()

    timer += 1
    print(dt)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        keyPressed = pygame.key.get_pressed()
        if keyPressed[K_ESCAPE]:
            running = False
        
        is_leftMouse_held = pygame.mouse.get_pressed()[0]
        is_middleMouse_held = pygame.mouse.get_pressed()[1]
        is_rightMouse_held = pygame.mouse.get_pressed()[2]

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            player.shoot(player.gun_cooldown, SHOOT_MIDDLE, PROJ_P_PORTAL)

        is_a_held = keyPressed[K_a]
        is_w_held = keyPressed[K_w]
        is_s_held = keyPressed[K_s]
        is_d_held = keyPressed[K_d]
        is_x_held = keyPressed[K_x]

    screen.fill((255, 255, 255))

    #------------------------------ Game operation ------------------------------#
    ## Changing rooms
    for a_player in all_players:
        if a_player.pos.x == 0:
            a_player.changeRoomLeft()
            room.roomCoords.x -= 1
            room.layoutUpdate()

        if a_player.pos.x == WINDOW_WIDTH:
            a_player.changeRoomRight()
            room.roomCoords.x += 1
            room.layoutUpdate()

        if a_player.pos.y == 0:
            a_player.changeRoomUp()
            room.roomCoords.y += 1
            room.layoutUpdate()

        if a_player.pos.y == WINDOW_HEIGHT:
            a_player.changeRoomDown()
            room.roomCoords.y -= 1
            room.layoutUpdate()

    # Random enemy movement for testing purposes
    for enemy in all_enemies:
        enemy.rand_movement(True)

    # Regenerate health for testing purposes
    for a_player in all_players:
        if timer % 5 == 0 and a_player.hp < a_player.max_hp and is_middleMouse_held == True:
            a_player.hp += 2
        else:
            pass 

    #------------------------------ Redraw window ------------------------------#
    redrawGameWindow()
    clock.tick_busy_loop(FPS)