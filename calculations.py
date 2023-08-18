import pygame
import math
import time

import random as rand

from spritesheet import Spritesheet

from constants import *
from groups import *

# ============================================================================ #
#                                 Returns float                                #
# ============================================================================ #
def getAngleToMouse(anySprite: pygame.sprite.Sprite) -> float:
    """Returns the angle between a sprite and the mouse cursor
    
    ### Arguments
        - anySprite ``(pygame.sprite.Sprite)``: The sprite to measure the angle from
    
    ### Returns
        - ``float``: The angle between ``any_sprite`` and the mouse cursor
    """    
    mouseX, mouseY = pygame.mouse.get_pos()
    length_to_x = mouseX - anySprite.pos.x
    length_to_y = mouseY - anySprite.pos.y
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


def getAngleToSprite(firstSprite: pygame.sprite.Sprite, secondSprite: pygame.sprite.Sprite) -> float:
    """Returns the angle from one sprite to another
    
    ### Arguments
        - firstSprite (``pygame.sprite.Sprite``): The sprite to begin the measurement from
        - secondSprite (``pygame.sprite.Sprite``): The sprite to measure the angle to
    
    ### Returns
        ``float``: The angle between the two sprites
    """    
    length_to_x = secondSprite.pos.x - firstSprite.pos.x
    length_to_y = secondSprite.pos.y - firstSprite.pos.y
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


def getAngleToCFromS(anySprite: pygame.sprite.Sprite, coords: pygame.math.Vector2) -> float:
    """Returns the angle between a sprite and a pair of coordinates. 
    ## NOTE: The angle is measured from the sprite to the coordinates!
    
    ### Arguments
        - anySprite (``pygame.sprite.Sprite``): _description_
        - coords (``pygame.math.Vector2``): _description_
    
    ### Returns
        - ``float``: _description_
    """    
    length_to_x = coords.x - anySprite.pos.x
    length_to_y = coords.y - anySprite.pos.y
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


def getAngleToCFromC(startCoords: pygame.math.Vector2, endCoords: pygame.math.Vector2) -> float:
    """Returns the angle between two coordinate points
    
    ### Arguments
        - startCoords (``pygame.math.Vector2``): The first set of coordinates
        - endCoords (``pygame.math.Vector2``): The second set of coordinates
    
    ### Returns
        - ``float``: The angle between the two coordinate point
    """    
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
    
    ### Arguments
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
    
    ### Arguments
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
    
    ### Arguments
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


def getTimeDiff(timeValue: float) -> float:
    """Returns the difference between the current time and another 
    
    ### Arguments
        - timeValue (``float``): The time to compare to the current time
    
    ### Returns
        - ``float``: The difference between the current time and the other time
    """    
    return time.time() - timeValue


# ------------------------------ Math Functions ------------------------------ #
def cerp(a: float, b: float, weight: float) -> float:
    """Cosinusoidally interpolates between two values given a weight

    ### Arguments
        - a (``float``): The starting value
        - b (``float``): The ending value
        - weight (``float``): The weight to interpolate by

    Returns:
        ``float``: The interpolated value
    """
    if weight < 0:
        weight = 0
    if weight > 1:
        weight = 1

    return ((a - b) / 2) * math.cos(math.pi * weight) + ((a + b) / 2)


def eerp(a: float, b: float, weight: float) -> float:
    """Exponentially interpolates between two values given a weight
    
    ### Arguments
        - a (``float``): The starting value
        - b (``float``): The ending value
        - weight (``float``): The weight to interpolate by
    
    ### Returns
        - ``float``: The interpolated value
    """    
    if (a < 0 and b > 0) or (a > 0 and b < 0):
        return ValueError('Error: \"a\" and \"b\" cannot have opposite signs')

    trueB = pow(a / b, -1)
    trueA = a

    if weight > 1:
        weight = 1
    elif weight < 0:
        weight = 0

    return trueA * pow(trueB, weight)


# ============================================================================ #
#                                  Returns int                                 #
# ============================================================================ #
def calculateDamage(sender: pygame.sprite.Sprite, receiver: pygame.sprite.Sprite, proj: pygame.sprite.Sprite) -> int:
    """Calculates the damage an entity receives after being hit
    
    ### Arguments
        - sender ``(pygame.sprite.Sprite)``: The entity that shot the projectile
        - receiver ``(pygame.sprite.Sprite)``: The entity that got shot
        - proj ``(pygame.sprite.Sprite)``: The projectile the receiver got hit by
    
    ### Returns
        - ``int``: Infliction damage upon ``receiver``
    """    
    damage = math.ceil((sender.atk / receiver.defense) * proj.damage)

    # if damage < 1:
    #     damage = 1

    return damage


# ============================================================================ #
#                                Returns string                                #
# ============================================================================ #
def collideSideCheck(instig: pygame.sprite.Sprite, object: pygame.sprite.Sprite) -> str:
    # Bottom center of sprite
    pointA = vec(object.pos.x,
                object.pos.y + object.hitbox.height)
    # Right center of sprite
    pointB = vec(object.pos.x + object.hitbox.width,
                object.pos.y)
    # Top center of sprite
    pointC = vec(object.pos.x,
                object.pos.y - object.hitbox.height)
    # Left center of sprite
    pointD = vec(object.pos.x - object.hitbox.width,
                object.pos.y)
    
    lenPointA, lenPointB = getDistToCoords(instig.pos, pointA), getDistToCoords(instig.pos, pointB)
    lenPointC, lenPointD = getDistToCoords(instig.pos, pointC), getDistToCoords(instig.pos, pointD)


    def isClosestPoint(point: pygame.math.Vector2) -> pygame.math.Vector2:
        if point == pointA:
            if (lenPointA < lenPointB and
                lenPointA < lenPointC and
                lenPointA < lenPointD):
                return True
            else:
                return False

        elif point == pointB:
            if (lenPointB < lenPointA and
                lenPointB < lenPointC and
                lenPointB < lenPointD):
                return True
            else:
                return False

        elif point == pointC:
            if (lenPointC < lenPointA and
                lenPointC < lenPointB and
                lenPointC < lenPointD):
                return True
            else:
                return False

        elif point == pointD:
            if (lenPointD < lenPointA and
                lenPointD < lenPointB and
                lenPointD < lenPointC):
                return True
            else:
                return False

        else:
            raise CustomError("Error: Point arg does not match any defined point")


    if isClosestPoint(pointB):
        return EAST
    
    elif isClosestPoint(pointD):
        return WEST
    
    elif isClosestPoint(pointC):
        return NORTH
    
    elif isClosestPoint(pointA):
        return SOUTH


def wallSideCheck(wall: pygame.sprite.Sprite, proj: pygame.sprite.Sprite) -> str:
    """Checks for which side of a wall a projectile hit and returns that value
    
    ### Arguments
        - wall (``pygame.sprite.Sprite``): The wall being hit
        - proj (``pygame.sprite.Sprite``): The projectile being fired
    
    ### Returns
        - ``str``: The side of the wall that the projectile hit
    """    
    if wall.pos.x - wall.hitbox.width * 0.45 <= proj.pos.x <= wall.pos.x + wall.hitbox.width * 0.45:
        if proj.pos.y < wall.pos.y:
            return NORTH
        elif proj.pos.y > wall.pos.y:
            return SOUTH
        
    elif wall.pos.y - wall.hitbox.height * 0.45 <= proj.pos.y <= wall.pos.y + wall.hitbox.height * 0.45:
        if proj.pos.x < wall.pos.x:
            return WEST
        elif proj.pos.x > wall.pos.x:
            return EAST
        
    else:
        pass


# ============================================================================ #
#                                Returns Vector2                               #
# ============================================================================ #
def getTopLeftCoords(spriteWidth: int, spriteHeight: int, desiredX: float, desiredY: float) -> pygame.math.Vector2:
    """Returns the coordinates of the topleft corner of a sprite that is centered at its middle
    
    ### Arguments
        - spriteWidth (``int``): _description_
        - spriteHeight (``int``): _description_
        - desiredX (``float``): _description_
        - desiredY (``float``): _description_
    
    ### Returns
        - ``pygame.math.Vector2``: _description_
    """    
    return vec(desiredX + spriteWidth // 2, desiredY + spriteHeight // 2)


def getRandComponents(maxValue) -> pygame.math.Vector2:
    """Given a maximum value, will output a vector containing two components that vectorially add to that value. The result can be positive or negative.
    
    ### Arguments
        - ``maxValue`` ``(pygame.math.vector2)``: The value in which the components will vectorially add to. The result can add to +maxValue ot -maxValue.
    
    ### Returns
        - ``pygame.math.Vector2``: The resultant random vector
    """    
    x = rand.uniform(-maxValue, maxValue)
    y = math.sqrt(pow(maxValue, 2) - pow(x, 2))
    if rand.choice((True, False)) == True:
        y = -y
    return vec(x, y)


def getTpVel(portalInDir: str, portalOutDir: str, sprite: pygame.sprite.Sprite) -> pygame.math.Vector2:
    velCopy: pygame.math.Vector2 = sprite.vel.copy()
    if portalInDir == SOUTH:
        if portalOutDir == SOUTH:
            return velCopy.rotate(180)
        if portalOutDir == EAST:
            return velCopy.rotate(90)
        if portalOutDir == NORTH:
            return velCopy
        if portalOutDir == WEST:
            return velCopy.rotate(270)
    
    if portalInDir == EAST:
        if portalOutDir == SOUTH:
            return vec(velCopy.y, -velCopy.x)
        if portalOutDir == EAST:
            return vec(-velCopy.x, -velCopy.y)
        if portalOutDir == NORTH:
            return vec(-velCopy.y, velCopy.x)
        if portalOutDir == WEST:
            return velCopy

    if portalInDir == NORTH:
        if portalOutDir == SOUTH:
            return velCopy
        if portalOutDir == EAST:
            return vec(velCopy.y, velCopy.x)
        if portalOutDir == NORTH:
            return vec(-velCopy.x, -velCopy.y)
        if portalOutDir == WEST:
            return vec(-velCopy.y, velCopy.x)

    if portalInDir == WEST:
        if portalOutDir == SOUTH:
            return vec(velCopy.y, velCopy.x)
        if portalOutDir == EAST:
            return velCopy
        if portalOutDir == NORTH:
            return vec(velCopy.y, -velCopy.x)
        if portalOutDir == WEST:
            return vec(-velCopy.x, -velCopy.y)


# ============================================================================ #
#                                Returns Surface                               #
# ============================================================================ #
def combineImages(baseImg: pygame.Surface, topImg: pygame.Surface) -> pygame.Surface:
    """Combines two images directly on top of one another
    
    ### Arguments
        - baseImg (``pygame.Surface``): The image to place first
        - topImg (``pygame.Surface``): The image being pasted on top of the first image
    
    ### Returns
        - ``pygame.Surface``: The combined image
    """    
    newImg: pygame.Surface = pygame.Surface(vec(max(baseImg.get_width(), topImg.get_width())), max(baseImg.get_height(), topImg.get_height()))
    centerX = (newImg.get_width() - baseImg.get_width()) // 2
    centerY = (newImg.get_height() - baseImg.get_height()) // 2
    newImg.blit(baseImg, vec(centerX, centerY))

    centerX = (newImg.get_width() - topImg.get_width()) // 2
    centerY = (newImg.get_height() - topImg.get_height()) // 2
    newImg.blit(topImg, vec(centerX, centerY))
    newImg.set_colorkey(BLACK)
    return newImg


def textToImage(text: str, fontImg: str, charWidth: int, charHeight: int, charCount: int) -> pygame.Surface:
    """Converts a spring of text into a surface with a given font
    
    ### Arguments
        - text (``str``): _description_
        - fontImg (``str``): _description_
        - charWidth (``int``): _description_
        - charHeight (``int``): _description_
        - charCount (``int``): _description_
    
    ### Returns
        - ``pygame.Surface``: _description_
    """    
    spritesheet = Spritesheet(fontImg, 37)
    images = spritesheet.get_images(charWidth, charHeight, charCount)
    charList = []

    finalImage = pygame.Surface(vec(len(text) * charWidth, charHeight))

    for char in text:
        if char in LETTERS.keys():
            charList.append(images[LETTERS[char]])
        elif char in NUMBERS:
            charList.append(images[int(char) + 26])
        elif char in SYMBOLS:
            charList.append(images[SYMBOLS[char] + 36])

    count = 0
    for char in charList:
        finalImage.blit(charList[count], vec(count * charWidth, 0))
        count += 1

    finalImage.set_colorkey(BLACK)
    return finalImage


# ============================================================================ #
#                                Returns Sprite                                #
# ============================================================================ #
def getClosestPlayer(checkSprite: pygame.sprite.Sprite) -> pygame.sprite.Sprite:
    """Checks for the closest player to a given sprite.
    
    ### Arguments
         checkSprite ``(pygame.sprite.Sprite)``: The entity checking for the closest player
    
    ### Returns
        - ``pygame.sprite.Sprite``: The player closest to ``checkSprite``
    """    
    playerCoords = {}
    for a_player in all_players:
        playerCoords[a_player] = getDistToSprite(checkSprite, a_player)

    try:
        temp = min(playerCoords.values())
        result = [key for key in playerCoords if playerCoords[key] == temp]
        return result[0]
    except:
        return checkSprite


def getOtherPortal(portalIn: pygame.sprite.Sprite) -> pygame.sprite.Sprite:
    for portal in all_portals:
        if portal != portalIn:
            return portal


# ============================================================================ #
#                                 Returns None                                 #
# ============================================================================ #

# ----------------------------- Hitbox Detection ----------------------------- #
def blockFromSide(instig: pygame.sprite.Sprite, sprite: pygame.sprite.Sprite) -> None:
    """If a sprite instigates a collision with another, the sprites will physically engage in a collision
    
    ### Arguments
        - instig (``pygame.sprite.Sprite``): The instigator of the collision
        - sprite (``pygame.sprite.Sprite``): The sprite being collided into
    """    
    if instig.hitbox.colliderect(sprite.hitbox):
        # Bottom center of sprite
        pointA = vec(sprite.pos.x,
                     sprite.pos.y + sprite.hitbox.height)
        # Right center of sprite
        pointB = vec(sprite.pos.x + sprite.hitbox.width,
                     sprite.pos.y)
        # Top center of sprite
        pointC = vec(sprite.pos.x,
                     sprite.pos.y - sprite.hitbox.height)
        # Left center of sprite
        pointD = vec(sprite.pos.x - sprite.hitbox.width,
                     sprite.pos.y)
        
        lenPointA, lenPointB = getDistToCoords(instig.pos, pointA), getDistToCoords(instig.pos, pointB)
        lenPointC, lenPointD = getDistToCoords(instig.pos, pointC), getDistToCoords(instig.pos, pointD)
        

        def isClosestPoint(point: pygame.math.Vector2) -> pygame.math.Vector2:
            if point == pointA:
                if (lenPointA < lenPointB and
                    lenPointA < lenPointC and
                    lenPointA < lenPointD):
                    return True
                else:
                    return False

            elif point == pointB:
                if (lenPointB < lenPointA and
                    lenPointB < lenPointC and
                    lenPointB < lenPointD):
                    return True
                else:
                    return False

            elif point == pointC:
                if (lenPointC < lenPointA and
                    lenPointC < lenPointB and
                    lenPointC < lenPointD):
                    return True
                else:
                    return False

            elif point == pointD:
                if (lenPointD < lenPointA and
                    lenPointD < lenPointB and
                    lenPointD < lenPointC):
                    return True
                else:
                    return False

            else:
                CustomError("Error: Point arg does not match any defined point")


        # If hitting the right side
        if (isClosestPoint(pointB) and
            instig.vel.x < 0 and
            instig.pos.x <= sprite.pos.x + (sprite.hitbox.width + instig.hitbox.width) // 2):
            instig.vel.x = 0
            instig.pos.x = sprite.pos.x + (sprite.hitbox.width + instig.hitbox.width) // 2

        # Hitting bottom side
        if (isClosestPoint(pointA) and
            instig.vel.y < 0 and
            instig.pos.y <= sprite.pos.y + (sprite.hitbox.height + instig.hitbox.height) // 2):
            instig.vel.y = 0
            instig.pos.y = sprite.pos.y + (sprite.hitbox.height + instig.hitbox.height) // 2

        # Hitting left side
        if (isClosestPoint(pointD) and
            instig.vel.x > 0 and
            instig.pos.x >= sprite.pos.x - (sprite.hitbox.width + instig.hitbox.width) // 2):
            instig.vel.x = 0
            instig.pos.x = sprite.pos.x - sprite.hitbox.width // 2 - instig.hitbox.width // 2

        # Hitting top side
        if (isClosestPoint(pointC) and
            instig.vel.y > 0 and
            instig.pos.y >= sprite.pos.y - (sprite.hitbox.width + instig.hitbox.width) // 2):
            instig.vel.y = 0
            instig.pos.y = sprite.pos.y - sprite.hitbox.height // 2 - instig.hitbox.height // 2


# ---------------------------------------------------------------------------- #
def killGroups(*groups: pygame.sprite.Group) -> None:
    """Calls ``.kill()`` for all sprites within one or more groups."""    
    for group in groups:
        for entity in group:
            if hasattr(entity, 'shatter'):
                entity.shatter()
            else:
                entity.kill()


def initStats(sprite: pygame.sprite.Sprite, hp: int, attack: int, defense: int, xp: int, cAccel: float) -> None:
    """Quickly initialize the stats of any enemy sprite
    
    ### Arguments
        - sprite (``pygame.sprite.Sprite``): The enemy to initilaize
        - hp (``int``): Amount of health the enemy should have
        - attack (``int``): Attack value the enemy should have
        - defense (``int``): Defense value the enemy should have
        - xp (``int``): The amount of xp the player should receive after killing the enemy
        - cAccel (``float``): How fast the enemy should move
    """    
    sprite.maxHp = hp
    sprite.hp = hp
    sprite.maxAtk = attack
    sprite.atk = attack
    sprite.maxDef = defense
    sprite.defense = defense
    sprite.xpWorth = xp
    sprite.cAccel = cAccel


def swapColor(image: pygame.Surface, old_color: tuple, new_color: tuple) -> None:
    """Swaps one color of a sprite with another
    
    ### Arguments
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


def groupChangeRooms(direction: str, *spriteGroups: pygame.sprite.Group) -> None:
    """Changes the room of all sprites within a group. This is achieved by adding or subtracting the window's width or height from the sprite's x-position or y-position, respecively.
    
    ### Arguments
        - direction (``str``): The direction of the room where ``spriteGroup`` should be relocated
        - spriteGroup (``pygame.sprite.Group``): The group to relocate
    """    
    for group in spriteGroups:
        if direction == SOUTH:
            for sprite in group:
                sprite.changeRoom(SOUTH)

        if direction == EAST:
            for sprite in group:
                sprite.changeRoom(EAST)

        if direction == NORTH:
            for sprite in group:
                sprite.changeRoom(NORTH)

        if direction == WEST:
            for sprite in group:
                sprite.changeRoom(WEST)


class CustomError(Exception):
    pass


if __name__ == '__main__':
    pass