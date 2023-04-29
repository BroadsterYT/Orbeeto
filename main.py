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
    Parameters:
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
        return selfEntity

def awardXp(enemy):
    """Give all players an enemy's xp worth after it is killed
    Parameters:
        enemy (pygame.sprite.Sprite): The enemy that has been killed
    """
    for a_player in all_players:
        a_player.xp += enemy.xp_worth

def tpLocation(entity, portal_in):
    """Teleports an entity between portals given the portal the entity is entering
    Parameters:
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

def groupChangeRooms(spriteGroup, direction):
    """Change the room location of all sprites in a sprite group given a direction.
    Parameters:
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

def objectAccel(object):
    """Defines acceleration for any entity's movement
    Parameters:
        object (pygame.sprite.Sprite): Any sprite object
    """    
    object.accel.x += object.vel.x * FRIC
    object.accel.y += object.vel.y * FRIC
    object.vel += object.accel * dt
    object.pos += object.vel + object.accel_const * object.accel

#------------------------------ Player class ------------------------------#
class PlayerBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all player objects. It contains parameters and methods to gain better control over player objects.
        """        
        super().__init__()
        self.room = vec((0, 0))
        self.visible = True

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

    def hide(self):
        self.visible = False
        all_sprites.remove(self)

    def show(self):
        self.visible = True
        all_sprites.add(self, layer = LAYERS['player_layer'])

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
    def __init__(self):
        """A player that can move and shoot.
        """        
        super().__init__()
        all_players.add(self)
        self.show()

        self.accel_const = 0.52

        self.spritesheet = SpriteSheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(200, 400, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

    def movement(self):
        self.accel = vec(0, 0)
        if self.visible:
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
        """Shoot a projectile

        Parameters:
        ----------
            vel (float): The speed the bullet should be fired at

            cannonSide (str): What side should the projectile be shot from?

            bulletType (str, optional): _description_. Defaults to PROJ_P_STD.
        """        
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
        all_sprites.remove(self)
        all_sprites.remove(self.healthBar)

    def show(self):
        self.visible = True
        all_sprites.add(self, layer = 1)
        all_sprites.add(self.healthBar, layer = 100)

def hideEnemies():
    """Hides all of the enemy sprites in the current room
    """    
    for container in all_containers:
        if container.room == room.room:
            for sprite in container.sprites():
                sprite.hide()

def showEnemies(container):
    for sprite in container.sprites():
        sprite.show()

class StandardGrunt(EnemyBase):
    def __init__(self, posX, posY, roomX, roomY, hp, attack, defense, xp_worth, accel_const):
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
        if self.hp > 0 and self.visible == True:
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
            try:
                angle_to_mouse = get_angle_to_entity(self, target)
            except:
                angle_to_mouse = 0

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
        all_sprites.add(self, layer = LAYERS['enemy_layer'])
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

                Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90)), bulletType, ),
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

#------------------------------ Interactible classes ------------------------------#
class MovableBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.visible = True

    def hide(self):
        self.visible = False
        all_sprites.remove(self)

    def show(self):
        self.visible = True
        all_sprites.add(self, layer = LAYERS['movable_layer'])

class Box(MovableBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show()
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

class DropBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
    
    def hide(self):
        self.visible = False
        all_sprites.remove(self)

    def show(self):
        self.visible = True
        all_sprites.add(self, layer = LAYERS['drops_layer'])

class ItemDrop(DropBase):
    def __init__(self, droppedFrom):
        """An item or material dropped by an enemey that is able to be collected

        Parameters:
        -------
            droppedFrom (pygame.sprite.Sprite): The enemy that the item was dropped from
        """        
        super().__init__()
        self.show()
        self.droppedFrom = droppedFrom
        self.start_time = time.time()
        
        self.spritesheet = SpriteSheet("sprites/bullets/bullets.png")
        self.images = self.spritesheet.getImages(0, 0, 16, 16, 9)
        self.index = 0

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.detect = pygame.Rect(0, 0, 32, 32)

    def movement(self):
        self.accel = vec(0, 0)
        if self.visible:
            pass

#------------------------------ Stat bar classes ------------------------------#
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, entity):
        super().__init__()
        all_sprites.add(self, layer = LAYERS['statBar_layer'])
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
        all_sprites.add(self, layer = LAYERS['statBar_layer'])
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
        """A projectile object that moves at a constant velocity

        Parameters:
        ----------
            shotFrom (pygame.sprite.Sprite): The entity the projectile is being shot from

            posX (float): The x-position that the projectile should be spawned at

            posY (float): The y-position that the projectile should be spawned at

            velX (float): The x-axis component of the projectile's velocity

            velY (float): The y-axis component of the projectile's velocity

            bulletType (str): The type of projectile that should be spawned

            doesBreak (bool): Should the bullet terminate upon impact?

            ricochet (bool, optional): Should the bullet bounce off of walls? Defaults to False.
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

    def land(self):
        all_explosions.add(ProjExplode(self))
        self.kill()

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
        
        self.visible = True
    
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

    Parameters:
    ----------
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
        
        self.spritesheet = SpriteSheet("sprites/bullets/bullets.png")
        self.index = 1

        if self.type == PROJ_P_STD:
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)

        elif self.type == PROJ_P_PORTAL:
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        self.rect = self.proj.rect
        self.randRotation = rand.randint(1, 360)

        self.pos = self.proj.pos

    def update(self):
        global timer
        if self.type == PROJ_P_STD or self.type == PROJ_E_STD:
            if timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1

        elif self.type == PROJ_P_PORTAL:
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
        all_sprites.add(self, layer = LAYERS['wall_layer'])
        all_walls.add(self)

        self.visible = True

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

        Parameters:
        ----
            sprites (pygame.sprite.Sprite): The sprite(s) to add to the group
        """        
        for sprite in sprites:
            super().add(sprite)

    def killAll(self):
        killGroup(self.sprites())

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
            )

            # Search for an enemy container for this room
            found_match = False
            for container in all_containers:
                if container.room == self.room:
                    found_match = True
                    searchIndex = all_containers.index(container)
                    break

            # If a match is found, show the sprites:
            if found_match:
                showEnemies(all_containers[searchIndex])

            # If a match is not found, make a new enemy container:
            else:
                all_containers.append(
                    EntityContainer(
                        self.room.x, self.room.y,
                        Box(800, WINDOW_HEIGHT / 2)
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

#------------------------------ Font class ------------------------------#
class DamageChar(pygame.sprite.Sprite):
    def __init__(self, posX, posY, damage):
        super().__init__()
        global timer
        all_sprites.add(self, layer = LAYERS['text_layer'])
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
def projectileCollide(entityGroup, proj, canHurt):
    """Destroys a given projectile upon a collision and renders an explosion
    
    Parameters:
    ------
        entityGroup (pygame.sprite.Group): The group of the entity the projectile is colliding with

        proj (pygame.sprite.Sprite): The projectile involved in the collision

        canHurt (bool): Should the projectile calculate damage upon impact? Defaults to False.
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

            # If the entity is not an enemy 
            elif entityGroup != all_enemies:
                colliding_entity.hp -= calculateDamage(proj.shotFrom, colliding_entity, proj)
                all_font_chars.add(DamageChar(colliding_entity.pos.x, colliding_entity.pos.y, calculateDamage(proj.shotFrom, colliding_entity, proj)))
                if hasattr(colliding_entity, 'hitTime'):
                    colliding_entity.hitTime = 0
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

    Parameters:
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
    else:
        projectile.kill()

    projectileCollide(projTargetGroup, projectile, True)
    projectileCollide(all_walls, projectile, False)
    projectileCollide(all_portals, projectile, False)

def redrawGameWindow():
    """Draws all entities every frame"""
    global timer
    # Updating players
    for a_player in all_players:
        collideCheck(a_player, enemy_projs)
        collideCheck(a_player, all_walls)
        collideCheck(a_player, all_movable)

        a_player.movement()
        a_player.shoot(12, None)

        # Teleport the player if they come into contact with a portal
        for portal in all_portals:
            if a_player.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                a_player.teleport(portal)

    # Updating enemies
    for enemy in all_enemies:
        print(enemy.visible)
        if enemy.visible == True:
            collideCheck(enemy, all_players,)
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
player1 = Player()

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
        hideEnemies()
        player1.changeRoomLeft()

    if player1.pos.x >= WINDOW_WIDTH:
        hideEnemies()
        player1.changeRoomRight()

    if player1.pos.y <= 0:
        hideEnemies()
        player1.changeRoomUp()

    if player1.pos.y >= WINDOW_HEIGHT:
        hideEnemies()
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