import pygame
from pygame.locals import *
import sys, math
import random as rand

import spritesheet as ss
import constants as cst
import calculateStats as stats

pygame.init()

# Aliases
vec = pygame.math.Vector2
spriteGroup = pygame.sprite.Group
sin = math.sin
cos = math.cos
rad = math.radians

FPS = 60

framePerSec = pygame.time.Clock()

screenSize = (cst.WINDOW_WIDTH, cst.WINDOW_HEIGHT)
displaySurface = pygame.display.set_mode(screenSize, pygame.SCALED)
pygame.display.set_caption('Orbeeto')

all_sprites = pygame.sprite.LayeredUpdates()
all_players = spriteGroup()
all_enemies = spriteGroup()

all_stat_bars = spriteGroup()

all_projectiles = []
players_projectiles = spriteGroup()
enemy_projectiles = spriteGroup()
all_explosions = spriteGroup()

all_walls = spriteGroup()

all_rooms = []

def get_angle_to_mouse(entity):
    """Returns the angle between an entity and the mouse cursor

    Args:
        entity (pygame.sprite.Sprite): The entity to measure from the cursor

    Returns:
        float: The angle between the entity and the mouse cursor
    """

    mouseX, mouseY = pygame.mouse.get_pos()
    length_to_x = mouseX - entity.rect.x - 32
    length_to_y = mouseY - entity.rect.y - 32
    if length_to_x and length_to_y != 0:
        angle_to_mouse = -math.degrees(math.atan2(length_to_y, length_to_x)) - 90
        return angle_to_mouse
    else:
        if length_to_y == 0:
            if length_to_x > 0:
                angle_to_mouse = -90
                return angle_to_mouse
            else:
                angle_to_mouse = 90
                return angle_to_mouse
        else:
            if length_to_y > 0:
                angle_to_mouse = -180
                return angle_to_mouse
            else:
                angle_to_mouse = 0
                return angle_to_mouse
            
def get_angle_to_entity(selfEntity, targetEntity):
    """Returns the angle between two different entities

    Args:
        selfEntity (pygame.sprite.Sprite): The entity to reference the angle from
        targetEntity (pygame.sprite.Sprite): The entity to measure from the reference

    Returns:
        float: The angle between the two given entities
    """

    length_to_x = (targetEntity.pos.x - (0.5 * targetEntity.image.get_width())) - (selfEntity.pos.x - (0.5 * selfEntity.image.get_width()))
    length_to_y = (targetEntity.pos.y - (0.5 * targetEntity.image.get_height())) - (selfEntity.pos.y - (0.5 * selfEntity.image.get_height()))
    if length_to_x and length_to_y != 0:
        angle_to_mouse = -math.degrees(math.atan2(length_to_y, length_to_x)) - 90
        return angle_to_mouse
    else:
        if length_to_y == 0:
            if length_to_x > 0:
                angle_to_mouse = -90
                return angle_to_mouse
            else:
                angle_to_mouse = 90
                return angle_to_mouse
        else:
            if length_to_y > 0:
                angle_to_mouse = -180
                return angle_to_mouse
            else:
                angle_to_mouse = 0
                return angle_to_mouse
            
def get_dist_to_entity(selfEntity, targetEntity):
    """Returns the distance between two entities

    Args:
        selfEntity (pygame.sprite.Sprite): The entity to start the measurement from
        targetEntity (pygame.sprite.Sprite): The second entity to measure to from the first

    Returns:
        float: Distance between selfEntity and targetEntity
    """

    length_to_x = (targetEntity.pos.x - (0.5 * targetEntity.image.get_width())) - (selfEntity.pos.x - (0.5 * selfEntity.image.get_width()))
    length_to_y = (targetEntity.pos.y - (0.5 * targetEntity.image.get_height())) - (selfEntity.pos.y - (0.5 * selfEntity.image.get_height()))
    
    return math.sqrt((length_to_x**2) + (length_to_y**2))

def get_angle_vel(velX, velY):
    """Returns the angle of a resultant vector

    Args:
        velX (float): The x-axis component of the vector
        velY (float): The y-axis component of the vector

    Returns:
        float: The angle of the resultant vector (in degrees)
    """
    
    if velX and velY != 0:
        vel_angle = -math.degrees(math.atan2(velY, velX)) - 90
        return vel_angle
    else:
        if velY == 0:
            if velX > 0:
                vel_angle = -90
                return vel_angle
            else:
                vel_angle = 90
                return vel_angle
        else:
            if velY > 0:
                vel_angle = -180
                return vel_angle
            else:
                vel_angle = 0
                return vel_angle

def collideCheck(object, contact_list):
    """Check if an entity comes into contact with an entity from a specific group.
    If the entities do collide, the entities will perform a hitbox collision.

    Args:
        entity (pygame.sprite.Sprite): The instigator of the collision
        contact_list (pygame.sprite.Group): The group to check for collisions with the instigator
    """
    
    global timer
    for entity in contact_list:
        if object.hitbox.colliderect(entity.hitbox):
            if object.pos.y < (entity.pos.y + (0.5 * entity.hitbox.height) + 1) and object.pos.y > (entity.pos.y - (0.5 * entity.hitbox.height) - 1):
                if object.pos.x > entity.pos.x:
                    object.vel.x = 0
                    object.pos.x += 1
                else:
                    object.vel.x = 0
                    object.pos.x -= 1
            if object.pos.x > (entity.pos.x - (0.5 * entity.hitbox.width) - 1) and object.pos.x < (entity.pos.x + (0.5 * entity.hitbox.width) + 1):
                if object.pos.y < entity.pos.y:
                    object.vel.y = 0
                    object.pos.y -= 1
                else:
                    object.vel.y = 0
                    object.pos.y += 1

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

def calculateDamage(sender, receiver, projectile):
    """Calculates the damage an entity receives after being hit

    Args:
        sender (pygame.sprite.Sprite): The entity that shot the projectile
        receiver (pygame.sprite.Sprite): The entity that got shot
        projectile (pygame.sprite.Sprite): The projectile the receiver got hit by

    Returns:
        int: Infliction damage upon receiver
    """

    return math.ceil(((sender.attack / receiver.defense) * projectile.damage))

def awardXp(enemy):
    """Give all players an enemy's xp worth after it is killed

    Args:
        enemy (pygame.sprite.Sprite): The enemy that has been killed
    """
    
    for a_player in all_players:
        a_player.xp += enemy.xp_worth

## Sprite functions
def getTopleftX(sprite, desired_x):
    """Returns the topleft x-value of a sprite that is centered at its middle

    Args:
        sprite (pygame.sprite.Sprite): The sprite to get the topleft x-value location for
        desired_x (int): The x-value of the desired location of the sprite's topleft corner

    Returns:
        int: x-value of the sprite's location from its center, where its topleft corner will be along its desired x-axis location
    """

    width = sprite.image.get_width()
    return (width / 2) + desired_x

def getTopleftY(sprite, desired_y):
    """Returns the topleft y-value of a sprite that is centered at its middle

    Args:
        sprite (pygame.sprite.Sprite): The sprite to get the topleft y-value location for
        desired_x (int): The y-value of the desired location of the sprite's topleft corner

    Returns:
        int: y-value of the sprite's location from its center, where its topleft corner will be along its desired y-axis location
    """

    height = sprite.image.get_height()
    return (height / 2) + desired_y

#------------------------------ Player class ------------------------------#
class PlayerBase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.accel_const = 0.52
        self.pos = vec((cst.WINDOW_WIDTH / 2, cst.WINDOW_HEIGHT / 2))
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
        for i in range(cst.WINDOW_WIDTH - 1):
            self.pos.x -= 1
        
        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

    def changeRoomLeft(self):
        for i in range(cst.WINDOW_WIDTH + 1):
            self.pos.x += 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

    def changeRoomUp(self):
        for i in range(cst.WINDOW_HEIGHT - 1):
            self.pos.y += 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

    def changeRoomDown(self):
        for i in range(cst.WINDOW_HEIGHT + 1):
            self.pos.y -= 1

        for enemy in all_enemies:
            enemy.healthBar.kill()
            enemy.kill()

class Player(PlayerBase):
    def __init__(self, hitbox_adjustX, hitbox_adjustY):
        super().__init__()
        all_sprites.add(self)
        all_sprites.change_layer(self, 0)
        all_players.add(self)

        self.spritesheet = ss.SpriteSheet("sprites/orbeeto/orbeeto.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(200, 400, 64, 64)
        self.hitbox = self.rect.inflate(hitbox_adjustX, hitbox_adjustY)

    def movement(self):
        self.accel = vec(0, 0)
        keyPressed = pygame.key.get_pressed()
        if keyPressed[K_a]:
            self.accel.x = -self.accel_const
        if keyPressed[K_d]:
            self.accel.x = self.accel_const
        if keyPressed[K_s]:
            self.accel.y = self.accel_const
        if keyPressed[K_w]:
            self.accel.y = -self.accel_const

        self.accel.x += self.vel.x * cst.FRIC
        self.accel.y += self.vel.y * cst.FRIC
        self.vel += self.accel
        self.pos += self.vel + self.accel_const * self.accel

        self.rect.center = self.pos
        self.hitbox.center = self.pos

        # When beyond window borders
        if self.pos.x >= cst.WINDOW_WIDTH:
            self.pos.x = cst.WINDOW_WIDTH
        if self.pos.x <= 0:
            self.pos.x = 0

        if self.pos.y >= cst.WINDOW_HEIGHT:
            self.pos.y = cst.WINDOW_HEIGHT
        if self.pos.y <= 0:
            self.pos.y = 0

    def shoot(self, vel, cannonSide, bulletType=cst.PROJ_BULLET):
        angle_to_mouse = get_angle_to_mouse(self)

        vel_x = vel * -sin(rad(angle_to_mouse))
        vel_y = vel * -cos(rad(angle_to_mouse))

        if cannonSide == cst.SHOOT_LEFT:
            players_projectiles.add(Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, cst.DMG_BULLET, bulletType))
        elif cannonSide == cst.SHOOT_RIGHT:
            players_projectiles.add(Projectile(self, self.pos.x + (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y - (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, cst.DMG_BULLET, bulletType))
        elif cannonSide == cst.SHOOT_MIDDLE:
            players_projectiles.add(Projectile(self, self.pos.x, self.pos.y, vel_x, vel_y, self.attack, bulletType))

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
        else:
            pass
        
        if self.hitTime < self.hitTime_charge:
            self.hitTime += 1

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]

        # Rotate sprite to mouse and draw hitbox
        self.image = pygame.transform.rotate(self.original_image, int(get_angle_to_mouse(self)))
        self.rect = self.image.get_rect(center = self.rect.center)

        # Gameplay
        stats.updateLevel(self)
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
        super().__init__()
        all_sprites.add(self)
        all_sprites.change_layer(self, 0)
        all_enemies.add(self)

        self.spritesheet = ss.SpriteSheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.accel_const = accel_const

        self.roomCoords = vec((0, 0))

        self.pos = vec((posX + (self.roomCoords.x * cst.WINDOW_WIDTH), posY + (self.roomCoords.y * cst.WINDOW_HEIGHT)))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.rand_pos = vec(rand.randint(0, cst.WINDOW_WIDTH), rand.randint(0, cst.WINDOW_HEIGHT))

        # Game stats
        self.max_hp = hp
        self.hp = self.max_hp
        self.max_attack = attack
        self.attack = self.max_attack
        self.max_defense = defense
        self.defense = self.max_defense
        self.xp_worth = xp_worth

    def rand_movement(self, canShoot):
        if (
            self.hp > 0 and 
            self.pos.x > 0 and
            self.pos.x < cst.WINDOW_WIDTH and
            self.pos.y > 0 and
            self.pos.y < cst.WINDOW_HEIGHT
        ):
            self.accel.x += self.vel.x * cst.FRIC
            self.accel.y += self.vel.y * cst.FRIC
            self.vel += self.accel
            self.pos += self.vel + self.accel_const * self.accel

            global timer
            if timer % rand.randint(150, 200) == 0:
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, cst.WINDOW_WIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, cst.WINDOW_HEIGHT - self.image.get_height() - 64)

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
                self.shoot(getClosestPlayer(self), 5, rand.randint(20, 30), cst.PROJ_BULLET)
            else:
                pass

    def shoot(self, target, vel, shoot_time, bulletType):
        global timer
        if timer % shoot_time == 0 and self.hp > 0:
            self.is_shooting = True
            angle_to_mouse = get_angle_to_entity(self, target)

            vel_x = vel * -sin(rad(angle_to_mouse))
            vel_y = vel * -cos(rad(angle_to_mouse))

            enemy_projectiles.add(Projectile(self, self.pos.x - (21 * cos(rad(angle_to_mouse))) - (30 * sin(rad(angle_to_mouse))), self.pos.y + (21 * sin(rad(angle_to_mouse))) - (30 * cos(rad(angle_to_mouse))), vel_x, vel_y, cst.DMG_BULLET, bulletType))

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
        all_sprites.add(self)
        all_sprites.change_layer(self, 0)
        all_enemies.add(self)

        self.spritesheet = ss.SpriteSheet("sprites/enemies/standard_grunt.png")
        self.images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.original_images = self.spritesheet.getImages(0, 0, 64, 64, 5)
        self.index = 0

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.hitbox = self.rect.inflate(-32, -32)

        self.accel_const = accel_const

        self.roomCoords = vec((0, 0))

        self.pos = vec((posX + (self.roomCoords.x * cst.WINDOW_WIDTH), posY + (self.roomCoords.y * cst.WINDOW_HEIGHT)))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.rand_pos = vec(rand.randint(0, cst.WINDOW_WIDTH), rand.randint(0, cst.WINDOW_HEIGHT))

        # Game stats
        self.max_hp = hp
        self.hp = self.max_hp
        self.max_attack = attack
        self.attack = self.max_attack
        self.max_defense = defense
        self.defense = self.max_defense
        self.xp_worth = xp_worth

    def rand_movement(self, canShoot):
        if (
            self.hp > 0 and 
            self.pos.x > 0 and
            self.pos.x < cst.WINDOW_WIDTH and
            self.pos.y > 0 and
            self.pos.y < cst.WINDOW_HEIGHT
        ):
            self.accel.x += self.vel.x * cst.FRIC
            self.accel.y += self.vel.y * cst.FRIC
            self.vel += self.accel
            self.pos += self.vel + self.accel_const * self.accel

            global timer
            if timer % rand.randint(250, 300) == 0:
                self.rand_pos.x = rand.randint(0, cst.WINDOW_WIDTH)
                self.rand_pos.y = rand.randint(0, cst.WINDOW_HEIGHT)

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
                self.shoot(getClosestPlayer(enemy), 5, 80, cst.PROJ_BULLET)
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
                # Projectile(self, self.pos.x - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel_x, vel_y, cst.DMG_BULLET, bulletType),
                # Projectile(self, self.pos.x + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))), -vel_x, -vel_y, cst.DMG_BULLET, bulletType),

                # Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90)), cst.DMG_BULLET, bulletType),
                # Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 90)), -vel * -cos(rad(angle_to_target + 90)), cst.DMG_BULLET, bulletType),

                # Projectile(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 45)), vel * -cos(rad(angle_to_target + 45)), cst.DMG_BULLET, bulletType),
                # Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 45)), -vel * -cos(rad(angle_to_target + 45)), cst.DMG_BULLET, bulletType),

                Projectile(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel * -sin(rad(angle_to_target - 45)), vel * -cos(rad(angle_to_target - 45)), cst.DMG_BULLET, bulletType),
                # Projectile(self, self.pos.x, self.pos.y, -vel * -sin(rad(angle_to_target - 45)), -vel * -cos(rad(angle_to_target - 45)), cst.DMG_BULLET, bulletType)
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
        all_sprites.add(self)
        all_sprites.change_layer(self, 1000)
        all_stat_bars.add(self)
        
        self.spritesheet = ss.SpriteSheet("sprites/stat_bars/health_bar.png", False)
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
        all_sprites.add(self)
        all_sprites.change_layer(self, 1000)
        all_stat_bars.add(self)

        self.spritesheet = ss.SpriteSheet("sprites/stat_bars/dodge_bar.png", False)
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
    def __init__(self, shotFrom, x, y, velX, velY, bulletDamage, bulletType):
        super().__init__()
        all_sprites.add(self)

        self.roomCoords = vec((0, 0))

        self.pos = vec((x, y))
        self.vel = vec(velX, velY)

        self.type = bulletType
        self.hitbox_adjust = vec(0, 0)

        if self.type == cst.PROJ_BULLET:
            self.hitbox_adjust = vec(-2, -2)
        elif self.type == cst.PROJ_PORTAL:
            self.hitbox_adjust = vec(0, 0)
        else:
            self.hitbox_adjust = vec(0, 0)

        self.spritesheet = ss.SpriteSheet("sprites/bullets/bullets.png")
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
        self.image = pygame.transform.rotate(self.original_image, int(get_angle_vel(self.vel.x, self.vel.y)))
        self.rect = self.image.get_rect(center = self.rect.center)

        # Game stats
        self.shotFrom = shotFrom
        self.damage = bulletDamage
    
    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        if self.type == cst.PROJ_BULLET:
            self.spritesheet = ss.SpriteSheet("sprites/bullets/bullets.png")
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.hitbox_adjust = vec(-8, -8)

        if self.type == cst.PROJ_PORTAL:
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
            self.image = pygame.transform.rotate(self.original_image, int(get_angle_vel(self.vel.x, self.vel.y)))
            self.rect = self.image.get_rect(center = self.rect.center)

#------------------------------ Bullet explosion class ------------------------------#
class BulletExplode(pygame.sprite.Sprite):
    def __init__(self, bullet):
        super().__init__()
        all_sprites.add(self)
        all_sprites.change_layer(self, 1)

        self.bullet = bullet
        self.type = bullet.type
        
        self.spritesheet = ss.SpriteSheet("sprites/bullets/bullets.png")
        self.index = 1

        if self.type == cst.PROJ_BULLET:
            self.images = self.spritesheet.getImages(0, 0, 32, 32, 4)
            self.original_images = self.spritesheet.getImages(0, 0, 32, 32, 4)

        self.image = self.images[self.index]
        self.original_image = self.original_images[self.index]
        self.rect = self.bullet.rect
        self.randRotation = rand.randint(0, 360)

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
        all_sprites.add(self)
        all_sprites.change_layer(self, 100)
        all_walls.add(self)

        self.image = pygame.Surface((32 * widthMult, 32 * heightMult))
        self.rect = self.image.get_rect()

        self.pos = vec((getTopleftX(self, topleftX_mult * 32), getTopleftY(self, topleftY_mult * 32)))
        self.rect.center = self.pos

        self.hitbox = self.rect

    def movement(self):
        pass

    def update(self):
        self.rect.center = self.pos

#------------------------------ Room class ------------------------------#
class Room(pygame.sprite.AbstractGroup):
    """The room where all the current action (a lot) is taking place

    Args:
        roomCoordsX (int): The room's x-axis location in the grid of the room layout
        roomCoordsY (int): The room's y-axis location in the grid of the room layout
    """
        
    def __init__(self, roomCoordsX, roomCoordsY):
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
                OctoGrunt(cst.WINDOW_WIDTH / 2, cst.WINDOW_HEIGHT / 2, 25, 10, 10, 25, 0.3)
            )

        elif self.roomCoords == vec(1, 0):
            self.sprites.add(
                Wall(0, 0, 40, 4),
                Wall(0, 18.5, 40, 4),
                StandardGrunt(cst.WINDOW_WIDTH / 2, cst.WINDOW_HEIGHT / 2, 25, 10, 10, 25, 0.35),
                StandardGrunt(cst.WINDOW_WIDTH / 2, cst.WINDOW_HEIGHT / 2, 25, 10, 10, 50, 0.35)
            )

        elif self.roomCoords == vec(0, 1):
            self.sprites.add(
                Wall(0, 0, 4, 22.5),
                Wall(36, 0, 4, 22.5),
                Wall(8, 4, 4, 4),
                Wall(28, 4, 4, 4)
            )

        self.sprites.draw(displaySurface)

#------------------------------ Redraw game window ------------------------------#
def projectileCollide(entityGroup, projectile, projGroup, canHurt = False):
    """Destroys a given projectile upon a collision and renders an explosion

    Args:
        entityGroup (pygame.sprite.Group): The group of the entity the projectile is colliding with
        projectile (pygame.sprite.Sprite): The projectile involved in the collision
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_projectiles)
        canHurt (bool): Should the projectile calculate damage upon impact? Defaults to False.
    """

    for entity in entityGroup:
        if entity.hitbox.colliderect(projectile.hitbox):
            if canHurt == True:
                entity.hp -= calculateDamage(projectile.shotFrom, entity, projectile)
            # Try to add bullet explosion for projectile
            try:
                all_explosions.add(BulletExplode(projectile))
            except:
                print("Error: explosion error")
            # Try to remove projectile
            try:
                projGroup.remove(projectile)
            except:
                pass

def bindProjectile(projectile, projGroup, projTargetGroup):
    """Binds a projectile to its shooter and confines it to the window borders

    Args:
        projectile (pygame.sprite.Sprite): The projectile to bind
        projGroup (pygame.sprite.Group): The group of the projectile from which it was shot from (ex. players_projectiles)
        projTargetGroup (pygame.sprite.Group): The group of the entities that should take damage from the given projectile
    """

    displaySurface.blit(projectile.image, projectile.rect)
    if (
        projectile.pos.x < cst.WINDOW_WIDTH and 
        projectile.pos.x > 0 and
        projectile.pos.y < cst.WINDOW_HEIGHT and 
        projectile.pos.y > 0
    ):
        projectile.movement()
        projectile.update()
    else:
        projGroup.remove(projectile)

    projectileCollide(projTargetGroup, projectile, projGroup, True)
    projectileCollide(all_walls, projectile, projGroup)
    
def redrawGameWindow():
    """Draws all entities every frame"""
    global timer
    # Drawing all player characters every frame
    for a_player in all_players:
        displaySurface.blit(a_player.image, a_player.rect)
        collideCheck(a_player, all_enemies)
        collideCheck(a_player, enemy_projectiles)
        collideCheck(a_player, all_walls)

        a_player.movement()
        a_player.update()

    # Drawing all enemies every frame
    for enemy in all_enemies:
        displaySurface.blit(enemy.image, enemy.rect)
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
        displaySurface.blit(bullet.image, bullet.rect)
        bullet.update()

    # Drawing all stat bars every frame
    for statBar in all_stat_bars:
        all_sprites.move_to_front(statBar)
        displaySurface.blit(statBar.image, statBar.rect)
        statBar.movement()
        statBar.update()

    # Drawing all walls every frame
    for wall in all_walls:
        displaySurface.blit(wall.image, wall.rect)
        all_sprites.move_to_back(wall)
        wall.update()

    pygame.display.update()

#------------------------------ Initialing parameters ------------------------------#
player = Player(-32, -32)

# Load rooms
room = Room(0, 0)
room.layoutUpdate()

timer = 0

is_leftMouse_held = False
is_rightMouse_held = False
is_middleMouse_held = False

stats.loadXpRequirements()

print(pygame.display.get_desktop_sizes())

#------------------------------ Main loop ------------------------------#
running = True
while running:
    timer += 1

    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if keyPressed[K_ESCAPE]:
            running = False
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            is_leftMouse_held = True

        if event.type == MOUSEBUTTONUP and event.button == 1:
            is_leftMouse_held = False

        if event.type == MOUSEBUTTONDOWN and event.button == 2:
            is_middleMouse_held = True

        if event.type == MOUSEBUTTONUP and event.button == 2:
            is_middleMouse_held = False

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            is_rightMouse_held = True
            player.shoot(player.gun_cooldown / 2, cst.SHOOT_MIDDLE, cst.PROJ_PORTAL)

        if event.type == MOUSEBUTTONUP and event.button == 3:
            is_rightMouse_held = False

    displaySurface.fill((255, 255, 255))

    #------------------------------ Game operation ------------------------------#
    ## Changing rooms
    for a_player in all_players:
        if a_player.pos.x == 0:
            a_player.changeRoomLeft()
            room.roomCoords.x -= 1
            room.layoutUpdate()

        if a_player.pos.x == cst.WINDOW_WIDTH:
            a_player.changeRoomRight()
            room.roomCoords.x += 1
            room.layoutUpdate()

        if a_player.pos.y == 0:
            a_player.changeRoomUp()
            room.roomCoords.y += 1
            room.layoutUpdate()

        if a_player.pos.y == cst.WINDOW_HEIGHT:
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

    # Autofire timer
    for a_player in all_players:
        if timer % a_player.gun_cooldown == 0:
            if is_leftMouse_held == True:
                a_player.shoot(a_player.gun_speed, cst.SHOOT_LEFT, cst.PROJ_BULLET)
                a_player.shoot(a_player.gun_speed, cst.SHOOT_RIGHT, cst.PROJ_BULLET)

    #------------------------------ Redraw window ------------------------------#
    redrawGameWindow()
    framePerSec.tick_busy_loop(FPS)