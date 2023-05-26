import pygame, math
from constants import *
import random as rand

from groups import *

vec = pygame.math.Vector2

#------------------------------ Returns float ------------------------------#
def get_angle_to_mouse(any_sprite):
    """Gets the angle between a sprite and the mouse cursor
    
    ### Parameters
        - ``any_sprite`` ``(pygame.sprite.Sprite)``: The sprite to measure the angle from
    
    ### Returns
        - ``float``: The angle between ``any_sprite`` and the mouse cursor
    """    
    mouseX, mouseY = pygame.mouse.get_pos()
    length_to_x = mouseX - any_sprite.rect.x - 32
    length_to_y = mouseY - any_sprite.rect.y - 32
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
            
def get_angle_to_entity(any_sprite, target_sprite):
    """Gets the angle from one sprite to another
    
    ### Parameters
        - ``any_sprite`` ``(pygame.sprite.Sprite)``: The sprite to begin the measurement from
        - ``target_sprite`` ``(pygame.sprite.Sprite)``: The sprite to measure the angle to
    
    ### Returns
        - ``float``: The angle between the two sprites
    """    
    length_to_x = (target_sprite.pos.x - (0.5 * target_sprite.image.get_width())) - (any_sprite.pos.x - (0.5 * any_sprite.image.get_width()))
    length_to_y = (target_sprite.pos.y - (0.5 * target_sprite.image.get_height())) - (any_sprite.pos.y - (0.5 * any_sprite.image.get_height()))
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
    
    ### Parameters
        - ``vecX`` ``(float)``: The x-axis component of the vector
        - ``vecY`` ``(float)``: The y-axis component of the vector
    
    ### Returns
        - ``pygame.math.Vector2``: The angle of the resultant vector (in degrees)
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
    
    ### Parameters
        - ``sender`` ``(pygame.sprite.Sprite)``: The entity that shot the projectile
        - ``receiver`` ``(pygame.sprite.Sprite)``: The entity that got shot
        - ``proj`` ``(pygame.sprite.Sprite)``: The projectile the receiver got hit by
    
    ### Returns
        - ``int``: Infliction damage upon ``receiver``
    """    
    damage = sender.attack - receiver.defense + proj.damage

    if damage < 0:
        damage = 1

    return damage

#------------------------------ Returns string ------------------------------#
def collideSideCheck(object, instig):
    """Determines the side of an object that an instigator has hit
    
    ### Parameters
        - ``object`` ``(pygame.sprite.Sprite)``: The sprite that is being hit
        - ``instig`` ``(pygame.sprite.Sprite)``: The instigating sprite of the collision
    
    ### Returns
        - ``str``: The side the instigator has hit
    """    
    if object.pos.x - 0.5 * object.hitbox.width <= instig.pos.x <= object.pos.x + 0.5 * object.hitbox.width and instig.pos.y > object.pos.y:
        return DOWN
    
    elif object.pos.x - 0.5 * object.hitbox.width <= instig.pos.x <= object.pos.x + 0.5 * object.hitbox.width and instig.pos.y < object.pos.y:
        return UP

    elif object.pos.y - 0.5 * object.hitbox.height <= instig.pos.y <= object.pos.y + 0.5 * object.hitbox.height and instig.pos.x > object.pos.x:
        return RIGHT
    
    elif object.pos.y - 0.5 * object.hitbox.height <= instig.pos.y <= object.pos.y + 0.5 * object.hitbox.height and instig.pos.x < object.pos.x:
        return LEFT
    
    else:
        return None

#------------------------------ Returns pygame.math.Vector2 ------------------------------#
def getTopLeft(sprite, desired_x, desired_y):
    """Returns the coordinates of the topleft corner of a sprite that is centered at its middle
    
    ### Parameters
        - ``sprite`` ``(pygame.sprite.Sprite)``: The sprite to get the topleft coordinates of
        - ``desired_x`` ``(float)``: The x-value of the desired location of the sprite's topleft corner
        - ``desired_y`` ``(float)``: The y-value of the desired location of the sprite's topleft corner
    
    ### Returns
        - ``pygame.math.Vector2``: The coordinates of the sprite's center, with its topleft corner in the desired x and y locations
    """    
    width = sprite.image.get_width()
    height = sprite.image.get_height()
    return vec(desired_x + width / 2, desired_y + height / 2)

def getRandComponents(maxValue):
    """Given a maximum value, will output a vector containing two components that vectorially add to that value. The result can be positive or negative.
    
    ### Parameters
        - ``maxValue`` ``(pygame.math.vector2)``: The value in which the components will vectorially add to. The result can add to +maxValue ot -maxValue.
    
    ### Returns
        - ``pygame.math.Vector2``: The resultant random vector
    """    
    x = rand.uniform(-maxValue, maxValue)
    y = math.sqrt(pow(maxValue, 2) - pow(x, 2))
    if rand.choice((True, False)) == True:
        y = -y
    return vec(x, y)

#------------------------------ Returns None ------------------------------#
def collideCheck(instig, contact_list):
    """Check if an entity comes into contact with an entity from a specific group.
    If the entities do collide, the entities will perform a hitbox collision.
    
    ### Parameters
        - ``instig`` ``(pygame.sprite.Sprite)``: The instigator of the collision
        - ``contact_list`` ``(pygame.sprite.Group)``: The sprite group to check for a collision with
    """    
    global timer
    for entity in contact_list:
        if hasattr(entity, 'visible') and entity.visible:
            pushFromSide(instig, entity)
        elif hasattr(entity, 'visible') and not entity.visible:
            pass
        else:
            pushFromSide(instig, entity)

def pushFromSide(instig, entity):
    if instig.hitbox.colliderect(entity.hitbox):
        if instig.pos.y < (entity.pos.y + (0.5 * entity.hitbox.height) + 1) and instig.pos.y > (entity.pos.y - (0.5 * entity.hitbox.height) - 1):
            if instig.pos.x > entity.pos.x:
                instig.vel.x = 0
                instig.pos.x += 1
            else:
                instig.vel.x = 0
                instig.pos.x -= 1
        if instig.pos.x > (entity.pos.x - (0.5 * entity.hitbox.width) - 1) and instig.pos.x < (entity.pos.x + (0.5 * entity.hitbox.width) + 1):
            if instig.pos.y < entity.pos.y:
                instig.vel.y = 0
                instig.pos.y -= 1
            else:
                instig.vel.y = 0
                instig.pos.y += 1

def killGroup(*groups):
    """Calls ``.kill()`` for all sprites within one or more groups.
    """    
    for group in groups:
        for entity in group:
            entity.kill()

#------------------------------ Classes ------------------------------#
class CustomError(Exception):
    """Returns a custom error

    Args:
        Exception (str): Error to raise
    """
    pass