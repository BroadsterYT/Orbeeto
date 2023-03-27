import pygame, math
from constants import *

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

#------------------------------ Returns None ------------------------------#
def objectAccel(object):
    """Defines accelearion for any object's movement

    Args:
        object (pygame.sprite.Sprite): Any sprite object
    """    
    object.accel.x += object.vel.x * FRIC
    object.accel.y += object.vel.y * FRIC
    object.vel += object.accel
    object.pos += object.vel + object.accel_const * object.accel

#------------------------------ Classes ------------------------------#
class CustomError(Exception):
    """Returns a custom error

    Args:
        Exception (str): Error to raise
    """
    pass