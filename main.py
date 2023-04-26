import pygame
from pygame.locals import *
import sys, math, time

import random as rand

from math import sin, cos, radians

from groups import *
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

    try:
        temp = min(playerCoords.values())
        result = [key for key in playerCoords if playerCoords[key] == temp]
        return result[0]
    except:
        pass

def awardXp(enemy):
    """Give all players an enemy's xp worth after it is killed
    Args:
        enemy (pygame.sprite.Sprite): The enemy that has been killed
    """
    for a_player in all_players:
        a_player.xp += enemy.xp_worth

def tpLocation(entity, portal_in):
    """Teleports an entity between portals given the portal the entity is entering
    Args:
        entity (pygame.sprite.Sprite): The player entering the portal
        portal_in (pygame.sprite.Sprite): The portal the player is entering
    """    
    for portal in all_portals:
        if portal != portal_in:
            other_portal = portal
            
    if other_portal.facing == DOWN:
        entity.pos.x = other_portal.pos.x
        entity.pos.y = other_portal.pos.y + other_portal.hitbox.height + entity.hitbox.height * 0.5
        entity.vel = vec(0, 0)

    elif other_portal.facing == RIGHT:
        entity.pos.x = other_portal.pos.x + other_portal.hitbox.width + entity.hitbox.width * 0.5
        entity.pos.y = other_portal.pos.y
        entity.vel = vec(0, 0)

    elif other_portal.facing == UP:
        entity.pos.x = other_portal.pos.x
        entity.pos.y = other_portal.pos.y - other_portal.hitbox.height - entity.hitbox.height * 0.5
        entity.vel = vec(0, 0)

    elif other_portal.facing == LEFT:
        entity.pos.x = other_portal.pos.x - other_portal.hitbox.width - entity.hitbox.width * 0.5
        entity.pos.y = other_portal.pos.y
        entity.vel = vec(0, 0)

def distFromCenterPortal(proj, portal_in):
    if portal_in.facing == DOWN or portal_in.facing == UP:
        return proj.pos.x - portal_in.pos.x
    if portal_in.facing == RIGHT or portal_in.facing == LEFT:
        return proj.pos.y - portal_in.pos.y

def teleportProj(proj, portalIn):
    for portal in all_portals:
        if portal != portalIn:
            portalOut = portal

    projGroup = players_projs

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
    """Defines acceleration for any entity's movement
    Args:
        object (pygame.sprite.Sprite): Any sprite object
    """    
    object.accel.x += object.vel.x * FRIC
    object.accel.y += object.vel.y * FRIC
    object.vel += object.accel * dt
    object.pos += object.vel + object.accel_const * object.accel

def groupChangeRooms(spriteGroup, direction):
    """Change the room location of all sprites in a sprite group given a direction.
    Args:
        spriteGroup (pygame.sprite.Group): The sprite group changing rooms
        direction (str): The room switching direction
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

#------------------------------ Player class ------------------------------#
class PlayerBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.room = vec((0, 0))

        self.pos = vec((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.room = vec((0, 0))

        #---------- Game stats ----------#
        self.xp = 0
        self.level = 0
        self.max_hp = 50
        self.hp = 50
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
        room.room.x += 1
        room.layoutUpdate()
        
        self.pos.x -= WINDOW_WIDTH
        groupChangeRooms(all_portals, RIGHT)
        
        killGroup(all_projs, all_explosions)

    def changeRoomLeft(self):
        room.room.x -= 1
        room.layoutUpdate()

        self.pos.x += WINDOW_WIDTH
        groupChangeRooms(all_portals, LEFT)

        killGroup(all_projs, all_explosions)

    def changeRoomUp(self):
        room.room.y += 1
        room.layoutUpdate()

        self.pos.y += WINDOW_HEIGHT
        groupChangeRooms(all_portals, UP)

        killGroup(all_projs, all_explosions)

    def changeRoomDown(self):
        room.room.y -= 1
        room.layoutUpdate()

        self.pos.y -= WINDOW_HEIGHT
        groupChangeRooms(all_portals, DOWN)

        killGroup(all_projs, all_explosions)

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

    def teleport(self, portal_in):
        tpLocation(self, portal_in)

    def shoot(self, vel, cannonSide, bulletType=PROJ_P_STD):
        angle_to_mouse = get_angle_to_mouse(self)

        vel_x = vel * -sin(rad(angle_to_mouse))
        vel_y = vel * -cos(rad(angle_to_mouse))

        if is_leftMouse_held == True:
            if timer % self.gun_cooldown == 0:
                players_projs.add(
                    Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType),
                    Projectile(self, self.pos.x + (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y - (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType)
                )

        elif cannonSide == SHOOT_MIDDLE:
            players_projs.add(Projectile(self, self.pos.x, self.pos.y, vel_x, vel_y, bulletType))

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
        self.visible = True

        self.pos = vec((0, 0))
        self.is_shooting = False
        self.healthBar = HealthBar(self)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

def storeEnemies():
    """Stores all of the sprites in a container into the enemy dictionary. This allows the game to remember objects that disappear from the screen.
    """    
    for container in all_containers:
        if container.room == room.room:
            new_cont = container.copy()
            container_sprites.update([((container.room.x, container.room.y), new_cont)])
            for sprite in container.sprites():
                sprite.hide()

class StandardGrunt(EnemyBase):
    def __init__(self, posX, posY, roomX, roomY, hp, attack, defense, xp_worth, accel_const):
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

        self.room = vec((roomX, roomY))

        self.pos = vec((posX, posY))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.rand_pos = vec(rand.randint(0, WINDOW_WIDTH), rand.randint(0, WINDOW_HEIGHT))

        #---------- Game stats ----------#
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

            enemy_projs.add(Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, bulletType))

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
    def __init__(self, posX, posY, roomX, roomY, hp, attack, defense, xp_worth, accel_const):
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

        self.room = vec((roomX, roomY))

        self.pos = vec((posX, posY))
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

            enemy_projs.add(
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

#------------------------------ Box class ------------------------------#
class Push(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        all_sprites.add(self, layer = 1)
        all_movable.add(self)

        self.spritesheet = SpriteSheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 1)
        self.index = 0

        self.pos = vec((posX, posY))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.accel_const = 0.4

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect

        self.rect.center = self.pos

    def movement(self):
        self.accel = vec(0, 0)
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
        all_projs.add(self)

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

        self.shotFrom = shotFrom
    
    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def teleport(self, portal_in):
        teleportProj(self, portal_in)

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
        self.hitbox.center = self.pos

        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

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
class AbstractBase(pygame.sprite.AbstractGroup):
    def __init__(self):
        """The base class for all standard abstract groups. Contains methods to help manipulate the abstract group.
        """        
        super().__init__()
    
    def add(self, *sprites):
        """Add one or more sprites to the abstract group.

        Args:
            sprites (pygame.sprite.Sprite): The sprite(s) to add to the group
        """        
        for sprite in sprites:
            super().add(sprite)

    def kill_all(self):
        killGroup(self.sprites())

class Room(AbstractBase):
    def __init__(self, roomX, roomY):
        """The room where all the current action (a lot) is taking place
        Args:
            roomX (int): The room's x-axis location in the grid of the room layout
            roomY (int): The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        all_rooms.append(self)
        self.room = vec((roomX, roomY))

    def layoutUpdate(self):
        """Updates the layout of the room.
        """        
        for sprite in self.sprites():
            sprite.kill()
        
        #---------- Room Layouts ----------#
        if self.room == vec(0, 0):
            self.add(
                Wall(0, 0, 4, 4),
                Wall(36, 0, 4, 4),
                Wall(0, 18.5, 4, 4),
                Wall(36, 18.5, 4, 4),
                Push(800, WINDOW_HEIGHT / 2)
            )

            found_match = False
            for cont in all_containers:
                if cont.room == self.room:
                    found_match = True
                    searchIndex = all_containers.index(cont)
                    searchKey = (cont.room.x, cont.room.y)
                    break

            if found_match:
                print(all_containers[searchIndex])
                # print(f"Added sprites!")

            else:
                print("Created new!")
                all_containers.append(
                    EnemyContainer(
                        self.room.x, self.room.y,
                        StandardGrunt(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 0, 0, 25, 10, 10, 25, 0.3),
                        StandardGrunt(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 0, 0, 25, 10, 10, 25, 0.3)
                    )
                )

        elif self.room == vec(1, 0):
            self.add(
                Wall(0, 0, 40, 4),
                Wall(0, 18.5, 40, 4),
            )

        elif self.room == vec(0, 1):
            self.add(
                Wall(0, 0, 4, 22.5),
                Wall(36, 0, 4, 22.5),
                Wall(8, 4, 4, 4),
                Wall(28, 4, 4, 4)
            )

    def update(self):
        pass

class EnemyContainer(AbstractBase):
    def __init__(self, roomX, roomY, *sprites):
        """A container for enemies. Contains data about all enemies in a room.

        Args:
            roomX (int): The room's x-axis location in the grid of the room layout
            roomY (int): The room's y-axis location in the grid of the room layout
            sprites (pygame.sprite.Sprite): The sprite(s) to add to the container
        """        
        super().__init__()
        self.room = vec((roomX, roomY))

        for sprite in sprites:
            self.add(sprite)

    def copy(self):
        new_sprites = []
        for sprite in self.sprites():
            new_sprites.append(sprite)
        return EnemyContainer(self.room.x, self.room.y, new_sprites)

#------------------------------ Font class ------------------------------#
class DamageChar(pygame.sprite.Sprite):
    def __init__(self, posX, posY, damage):
        super().__init__()
        global timer
        all_sprites.add(self, layer = 51)
        all_font_chars.add(self)
        
        self.spritesheet = SpriteSheet("sprites/ui/font.png")
        self.images = self.spritesheet.getImages(0, 0, 9, 14, 36)

        self.pos = vec((posX, posY))
        self.vel = vec(0, -2)

        self.timeStart = timer

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
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center = self.rect.center)
        self.rect.center = self.pos

    def movement(self):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.rect.center = self.pos

    def update(self):
        global timer
        if timer == self.timeStart + 40:
            self.kill()

#------------------------------ Redraw game window ------------------------------#
def projectileCollide(entityGroup, proj, doesShatter, canHurt):
    """Destroys a given projectile upon a collision and renders an explosion
    Args:
        entityGroup (pygame.sprite.Group): The group of the entity the projectile is colliding with
        proj (pygame.sprite.Sprite): The projectile involved in the collision
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_projectiles)
        canHurt (bool): Should the projectile calculate damage upon impact? Defaults to False.
    """
    for entity in entityGroup:
        if proj.hitbox.colliderect(entity.hitbox):
            if canHurt == True and entityGroup == all_enemies: # If a player's bullet hits an enemy, there's a chance to crit.
                if rand.randint(1, 20) == 1:
                    entity.hp -= (calculateDamage(proj.shotFrom, entity, proj)) * 3
                    all_font_chars.add(DamageChar(entity.pos.x, entity.pos.y, 3 * calculateDamage(proj.shotFrom, entity, proj)))
                else:
                    entity.hp -= calculateDamage(proj.shotFrom, entity, proj)
                    all_font_chars.add(DamageChar(entity.pos.x, entity.pos.y, calculateDamage(proj.shotFrom, entity, proj)))

            if canHurt == True and entityGroup != all_enemies:
                entity.hp -= calculateDamage(proj.shotFrom, entity, proj)
                all_font_chars.add(DamageChar(entity.pos.x, entity.pos.y, calculateDamage(proj.shotFrom, entity, proj)))

                try:
                    entity.hitTime = 0 # Will work if entity is a player (which will be most likely)
                except:
                    pass

            if (
                proj.type != PROJ_P_PORTAL and
                entityGroup == all_portals and
                len(all_portals) == 2
            ): # If proj is not a portal and there are 2 portals already existing
                for portal in all_portals:
                    if proj.hitbox.colliderect(portal.hitbox):
                        proj.teleport(portal)

            if proj.type == PROJ_P_PORTAL and entityGroup == all_walls:
                side = portalSideCheck(entity, proj)
                if side == DOWN or side == UP:
                    if proj.pos.x - 32 > entity.pos.x - 0.5 * entity.image.get_width() and proj.pos.x + 32 < entity.pos.x + 0.5 * entity.image.get_width():
                        all_portals.add(Portal(proj.pos.x, proj.pos.y, side))
                        portalCountCheck()
                if side == RIGHT or side == LEFT:
                    if proj.pos.y - 32 > entity.pos.y - 0.5 * entity.image.get_height() and proj.pos.y + 32 < entity.pos.y + 0.5 * entity.image.get_height():
                        all_portals.add(Portal(proj.pos.x, proj.pos.y, side))
                        portalCountCheck()

            if doesShatter == True and proj.type != PROJ_P_PORTAL:
                all_explosions.add(BulletExplode(proj))

            proj.kill()

def bindProjectile(projectile, projTargetGroup):
    """Binds a projectile to its shooter and confines it to the window borders
    Args:
        projectile (pygame.sprite.Sprite): The projectile to bind
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_proj)
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
    # Updating players
    for a_player in all_players:
        collideCheck(a_player, all_enemies)
        collideCheck(a_player, enemy_projs)
        collideCheck(a_player, all_walls)
        collideCheck(a_player, all_movable)

        a_player.movement()
        a_player.shoot(12, None)
        a_player.update()

        for portal in all_portals:
            if a_player.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                a_player.teleport(portal)

    # Updating enemies
    for enemy in all_enemies:
        collideCheck(enemy, all_players)
        collideCheck(enemy, players_projs)
        collideCheck(enemy, all_walls)

    # Updating movable objects
    for object in all_movable:
        object.movement()

    # Updating player projectiles
    for projectile in players_projs:
        bindProjectile(projectile, all_enemies)

    # Updating enemy projectiles
    for projectile in enemy_projs:
        bindProjectile(projectile, all_players)

    # Updating explosions
    for bullet in all_explosions:
        pass

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

    # Updating rooms
    for room in all_rooms:
        pass

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()

#------------------------------ Initialing parameters ------------------------------#
player1 = Player(-32, -32)

# Load rooms
room = Room(0, 0)
room.layoutUpdate()

# Time control
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
    dt = (time.time() - last_time) * 60
    last_time = time.time()

    timer += 1

    if player1.hp <= 0:
        killGroup(all_sprites)
        pygame.quit()
        sys.exit()

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
            player1.shoot(player1.gun_cooldown, SHOOT_MIDDLE, PROJ_P_PORTAL)

        is_a_held = keyPressed[K_a]
        is_w_held = keyPressed[K_w]
        is_s_held = keyPressed[K_s]
        is_d_held = keyPressed[K_d]
        is_x_held = keyPressed[K_x]

    screen.fill((255, 255, 255))

    #------------------------------ Game operation ------------------------------#
    ## Changing rooms
    if player1.pos.x <= 0:
        storeEnemies()
        player1.changeRoomLeft()

    if player1.pos.x >= WINDOW_WIDTH:
        storeEnemies()
        player1.changeRoomRight()

    if player1.pos.y <= 0:
        storeEnemies()
        player1.changeRoomUp()

    if player1.pos.y >= WINDOW_HEIGHT:
        storeEnemies()
        player1.changeRoomDown()

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