import pygame, math
import random as rand
from constants import *

vec = pygame.math.Vector2

#------------------------------ Returns float ------------------------------#
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

def get_vec_angle(vecX, vecY):
    """Returns the angle of a resultant vector

    Args:
        velX (float): The x-axis component of the vector
        velY (float): The y-axis component of the vector

    Returns:
        float: The angle of the resultant vector (in degrees)
    """
    if vecX and vecY != 0:
        vec_angle = -math.degrees(math.atan2(vecY, vecX)) - 90
        return vec_angle
    else:
        if vecY == 0:
            if vecX > 0:
                vec_angle = -90
                return vec_angle
            else:
                vec_angle = 90
                return vec_angle
        else:
            if vecY > 0:
                vec_angle = -180
                return vec_angle
            else:
                vec_angle = 0
                return vec_angle

#------------------------------ Returns int ------------------------------#
def calculateDamage(sender, receiver, proj):
    """Calculates the damage an entity receives after being hit

    Args:
        sender (pygame.sprite.Sprite): The entity that shot the projectile
        receiver (pygame.sprite.Sprite): The entity that got shot
        projectile (pygame.sprite.Sprite): The projectile the receiver got hit by

    Returns:
        int: Infliction damage upon receiver
    """
    damage = sender.attack - receiver.defense + proj.damage

    if damage < 0:
        damage = 1

    return damage

#------------------------------ Returns pygame.math.Vector2 ------------------------------#
def getTopLeft(sprite, desired_x, desired_y):
    """Returns the coordinates of the topleft corner of a sprite that is centered at its middle

    Args:
        sprite (pygame.sprite.Sprite): The sprite to get the topleft coordinates of
        desired_x (int): The x-value of the desired location of the sprite's topleft corner
        desired_y (int): The y-value of the desired location of the sprite's topleft corner

    Returns:
        pygame.math.Vector2: The coordinates of the sprite's center, with its topleft corner in the desired x and y locations
    """    
    width = sprite.image.get_width()
    height = sprite.image.get_height()
    return vec(desired_x + width / 2, desired_y + height / 2)

#------------------------------ Returns None ------------------------------#
def collideCheck(object, contact_list):
    """Check if an entity comes into contact with an entity from a specific group.
    If the entities do collide, the entities will perform a hitbox collision.

    Args:
        object (pygame.sprite.Sprite): The instigator of the collision
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

def killGroup(spriteGroup):
    """Run sprite.kill() for all entities in a group.

    Args:
        spriteGroup (pygame.sprite.Group): The group to kill all sprites within
    """    
    for entity in spriteGroup:
        entity.kill()

#------------------------------ Classes ------------------------------#
class CustomError(Exception):
    """Returns a custom error

    Args:
        Exception (str): Error to raise
    """
    pass