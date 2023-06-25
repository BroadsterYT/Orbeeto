import pygame, math
from constants import *
import random as rand

from groups import *

# ------------------------------- Returns float ------------------------------ #
def getAngleToMouse(any_sprite: pygame.sprite.Sprite) -> float:
    """Gets the angle between a sprite and the mouse cursor
    
    ### Parameters
        - any_sprite ``(pygame.sprite.Sprite)``: The sprite to measure the angle from
    
    ### Returns
        - ``float``: The angle between ``any_sprite`` and the mouse cursor
    """    
    mouseX, mouseY = pygame.mouse.get_pos()
    length_to_x = mouseX - any_sprite.pos.x
    length_to_y = mouseY - any_sprite.pos.y
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


def getAngleToSprite(any_sprite: pygame.sprite.Sprite, target_sprite: pygame.sprite.Sprite) -> float:
    """Gets the angle from one sprite to another
    
    ### Parameters
        - any_sprite (``pygame.sprite.Sprite``): The sprite to begin the measurement from
        - target_sprite (``pygame.sprite.Sprite``): The sprite to measure the angle to
    
    ### Returns
        ``float``: The angle between the two sprites
    """    
    length_to_x = target_sprite.pos.x - any_sprite.pos.x
    length_to_y = target_sprite.pos.y - any_sprite.pos.y
    if length_to_x and length_to_y != 0:
        angle = -math.degrees(math.atan2(length_to_y, length_to_x)) - 90
        return angle
    else:
        if length_to_y == 0:
            if length_to_x > 0:
                angle = -90
                return angle
            else:
                angle = 90
                return angle
        else:
            if length_to_y > 0:
                angle = -180
                return angle
            else:
                angle = 0
                return angle


def getAngleToCFromS(any_sprite: pygame.sprite.Sprite, coords: pygame.math.Vector2) -> float:
    length_to_x = coords.x - any_sprite.pos.x
    length_to_y = coords.y - any_sprite.pos.y
    if length_to_x and length_to_y != 0:
        angle = -math.degrees(math.atan2(length_to_y, length_to_x)) - 90
        return angle
    else:
        if length_to_y == 0:
            if length_to_x > 0:
                angle = -90
                return angle
            else:
                angle = 90
                return angle
        else:
            if length_to_y > 0:
                angle = -180
                return angle
            else:
                angle = 0
                return angle


def getAngleToCFromC(startCoords: pygame.math.Vector2, endCoords: pygame.math.Vector2):
    lengthX = endCoords.x - startCoords.x
    lengthY = endCoords.y - startCoords.y
    if lengthX and lengthY != 0:
        angle = -math.degrees(math.atan2(lengthY, lengthX)) - 90
        return angle
    else:
        if lengthY == 0:
            if lengthX > 0:
                angle = -90
                return angle
            else:
                angle = 90
                return angle
        else:
            if lengthY > 0:
                angle = -180
                return angle
            else:
                angle = 0
                return angle


def getDistToSprite(selfEntity: pygame.sprite.Sprite, targetEntity: pygame.sprite.Sprite) -> float:
    """Gets the distance between two entities
    
    ### Parameters
        - selfEntity (``pygame.sprite.Sprite``): The entity to start the measurement from
        - targetEntity (``pygame.sprite.Sprite``): The second entity to measure to from the first
    
    ### Returns
        - ``float``: Distance between ``selfEntity`` and ``targetEntity``
    """    
    length_to_x = targetEntity.pos.x - selfEntity.pos.x
    length_to_y = targetEntity.pos.y - selfEntity.pos.y
    
    return math.sqrt((length_to_x**2) + (length_to_y**2))


def getDistToCoords(startCoords: pygame.math.Vector2, endCoords: pygame.math.Vector2):
    """Returns the distance between two coordinates
    
    ### Parameters
        - startCoords (``pygame.math.Vector2``): The first set of coordinates
        - endCoords (``pygame.math.Vector2``): The second set of coordinates
    
    ### Returns
        - ``float``: The distance between the two coordinates
    """    
    lengthX = endCoords.x - startCoords.x
    lengthY = endCoords.y - startCoords.y
    
    return math.sqrt(pow(lengthX, 2) + pow(lengthY, 2))


def getVecAngle(vecX: float, vecY: float) -> float:
    """Returns the angle of a resultant vector
    
    ### Parameters
        - vecX (``float``): The x-axis component of the vector
        - vecY (``float``): The y-axis component of the vector
    
    ### Returns
        - ``float``: The angle of the resultant vector (in degrees)
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


# -------------------------------- Returns int ------------------------------- #
def calculateDamage(sender: pygame.sprite.Sprite, receiver: pygame.sprite.Sprite, proj: pygame.sprite.Sprite) -> int:
    """Calculates the damage an entity receives after being hit
    
    ### Parameters
        - sender ``(pygame.sprite.Sprite)``: The entity that shot the projectile
        - receiver ``(pygame.sprite.Sprite)``: The entity that got shot
        - proj ``(pygame.sprite.Sprite)``: The projectile the receiver got hit by
    
    ### Returns
        - ``int``: Infliction damage upon ``receiver``
    """    
    damage = math.floor((sender.attack / receiver.defense) * proj.damage)

    if damage < 1:
        damage = 1

    return damage


# ------------------------------ Returns string ------------------------------ #
def collideSideCheck(object: pygame.sprite.Sprite, instig: pygame.sprite.Sprite) -> str:
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


# ------------------------ Returns pygame.math.Vector2 ----------------------- #
def getTopLeftCoordinates(sprite, desired_x, desired_y) -> pygame.math.Vector2:
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


def getRandComponents(maxValue) -> pygame.math.Vector2:
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


# ----------------------- Returns pygame.sprite.Sprite ----------------------- #
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


# ------------------------------- Returns None ------------------------------- #
def collideCheck(instig: pygame.sprite.Sprite, *contactLists: pygame.sprite.Group) -> None:
    """Check if a sprite comes into contact with another sprite from a specific group.
    If the sprites do collide, then they will perform a hitbox collision.
    
    ### Parameters
        - instig (``pygame.sprite.Sprite``): The instigator of the collision
        - contactLists (``pygame.sprite.Group``): The sprite group(s) to check for a collision with
    """    
    for list in contactLists:
        for entity in list:
            if hasattr(entity, 'visible') and entity.visible:
                pushFromSide(instig, entity)
            elif hasattr(entity, 'visible') and not entity.visible:
                pass
            else:
                pushFromSide(instig, entity)


def pushFromSide(instig: pygame.sprite.Sprite, entity: pygame.sprite.Sprite) -> None:
    if instig.hitbox.colliderect(entity.hitbox):
        if instig.pos.y < (entity.pos.y + (0.5 * entity.hitbox.height) + 1) and instig.pos.y > (entity.pos.y - (0.5 * entity.hitbox.height) - 1):
            if instig.pos.x > entity.pos.x: # Right
                instig.pos.x = entity.pos.x + (entity.hitbox.width // 2) + (instig.hitbox.width // 2)
            else: # Left
                instig.pos.x = entity.pos.x - (entity.hitbox.width // 2) - (instig.hitbox.width // 2)
        elif instig.pos.x > (entity.pos.x - (0.5 * entity.hitbox.width) - 1) and instig.pos.x < (entity.pos.x + (0.5 * entity.hitbox.width) + 1):
            if instig.pos.y < entity.pos.y: # Up
                # instig.vel.y = 0
                instig.pos.y = entity.pos.y - (entity.hitbox.height // 2) - (instig.hitbox.height // 2)
            else: # Down
                # instig.vel.y = 0
                instig.pos.y = entity.pos.y + (entity.hitbox.height // 2) + (instig.hitbox.height // 2)


def killGroups(*groups: pygame.sprite.Group) -> None:
    """Calls ``.kill()`` for all sprites within one or more groups."""    
    for group in groups:
        for entity in group:
            if hasattr(entity, 'shatter'):
                entity.shatter()
            else:
                entity.kill()


def initStats(sprite: pygame.sprite.Sprite, hp: int, attack: int, defense: int, xp: int, accel_const: float) -> None:
    """Quickly initialize the stats of any enemy sprite
    
    ### Parameters
        - sprite (``pygame.sprite.Sprite``): The enemy to initilaize
        - hp (``int``): Amount of health the enemy should have
        - attack (``int``): Attack value the enemy should have
        - defense (``int``): Defense value the enemy should have
        - xp (``int``): The amount of xp the player should receive after killing the enemy
        - accel_const (``float``): How fast the enemy should move
    """    
    sprite.max_hp = hp
    sprite.hp = hp
    sprite.max_attack = attack
    sprite.attack = attack
    sprite.max_defense = defense
    sprite.defense = defense
    sprite.xp_worth = xp
    sprite.accel_const = accel_const


def swapColor(image: pygame.Surface, old_color: tuple, new_color: tuple) -> None:
    """Swaps one color of a sprite with another
    
    ### Parameters
        - image (``pygame.Surface``): The image to swap a color within
        - old_color (``tuple``): The color being replaced
        - new_color (``tuple``): The new color replacing the old color
    
    ### Returns
        - ``pygame.Surface``: The image with swapped colors
    """    
    new_img = image.copy()
    for x in range(new_img.get_width()):
        for y in range(new_img.get_height()):
            current_color = new_img.get_at((x, y))
            if current_color == old_color:
                new_img.set_at((x, y), new_color)
    return new_img


def groupChangeRooms(spriteGroup: pygame.sprite.Group, direction: str) -> None:
    """Changes the room of all sprites within a group. This is achieved by adding or subtracting the window's width or height from the sprite's x-position or y-position, respecively.
    
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


# ---------------------------------- Classes --------------------------------- #
class CustomError(Exception):
    """Returns a custom error

    Args:
        Exception (str): Error to raise
    """
    pass