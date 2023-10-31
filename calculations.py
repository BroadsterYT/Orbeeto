import random as rand
import time

from constants import *
from groups import *
from spritesheet import Spritesheet


# ============================================================================ #
#                                 Returns float                                #
# ============================================================================ #
def get_angle_to_mouse(any_sprite) -> float:
    """Returns the angle between a sprite and the mouse cursor.

    Args:
        any_sprite: The sprite to measure the angle from

    Returns:
        float: The angle between the sprite and the mouse cursor
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    length_to_x = mouse_x - any_sprite.pos.x
    length_to_y = mouse_y - any_sprite.pos.y
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


def get_angle_to_sprite(first_sprite, second_sprite) -> float:
    """Returns the angle from one sprite to another.

    Args:
        first_sprite: The sprite to begin the measurement from
        second_sprite: The sprite to measure the angle to

    Returns:
        float: The angle between the two sprites
    """
    length_to_x = second_sprite.pos.x - first_sprite.pos.x
    length_to_y = second_sprite.pos.y - first_sprite.pos.y
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


def get_angle_to_c_from_s(any_sprite, coords) -> float:
    """Returns the angle between a sprite and a set of coordinates. The angle is measured from the sprite to the coords.

    Args:
        any_sprite: The sprite to measure from
        coords: The coordinates to measure from

    Returns:
        float: The angle between the sprite and the set of coordinates
    """
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


def get_angle_to_c_from_c(start_coords: pygame.math.Vector2, end_coords: pygame.math.Vector2) -> float:
    """Returns the angle between two coordinate points

    Args:
        start_coords: The first set of coordinates
        end_coords: The second set of coordinates

    Returns:
        float: The angle between the two coordinate points
    """
    length_x = end_coords.x - start_coords.x
    length_y = end_coords.y - start_coords.y
    if length_x and length_y != 0:
        return -math.degrees(math.atan2(length_y, length_x)) - 90
    else:
        if length_y == 0:
            if length_x > 0:
                return -90
            else:
                return 90
        else:
            if length_y > 0:
                return -180
            else:
                return 0


def get_dist_to_sprite(first_sprite, second_sprite) -> float:
    """Returns the distance between two sprites.

    Args:
        first_sprite: The sprite to start the measurement from
        second_sprite: The second sprite to measure the distance from the first

    Returns:
        float: The distance between the two sprites
    """
    length_to_x = second_sprite.pos.x - first_sprite.pos.x
    length_to_y = second_sprite.pos.y - first_sprite.pos.y

    return math.sqrt((length_to_x ** 2) + (length_to_y ** 2))


def get_dist_to_coords(start_coords: pygame.math.Vector2, end_coords: pygame.math.Vector2):
    """Returns the distance between two coordinates
    
    ### Arguments
        - startCoords (``pygame.math.Vector2``): The first set of coordinates
        - endCoords (``pygame.math.Vector2``): The second set of coordinates
    
    ### Returns
        - ``float``: The distance between the two coordinates
    """
    length_x = end_coords.x - start_coords.x
    length_y = end_coords.y - start_coords.y

    return math.sqrt(pow(length_x, 2) + pow(length_y, 2))


def get_vec_angle(vec_x: float, vec_y: float) -> float:
    """Returns the angle of a resultant vector

    Args:
        vec_x: The x-axis component of the vector
        vec_y: The y-axis component of the vector

    Returns:
        The angle of the resultant vector (in degrees)
    """
    if vec_x and vec_y != 0:
        vec_angle = -math.degrees(math.atan2(vec_y, vec_x)) - 90
        return vec_angle
    else:
        if vec_y == 0:
            if vec_x > 0:
                vec_angle = -90
                return vec_angle
            else:
                vec_angle = 90
                return vec_angle
        else:
            if vec_y > 0:
                vec_angle = -180
                return vec_angle
            else:
                vec_angle = 0
                return vec_angle


def get_time_diff(time_value: float) -> float:
    """Returns the difference between the current time and another.

    Args:
        time_value: The time to compare to the current time

    Returns:
        float: The difference between the current time and the other time
    """
    return time.time() - time_value


# ------------------------------ Math Functions ------------------------------ #
# noinspection SpellCheckingInspection
def cerp(a: int | float | vec, b: int | float | vec, weight: float) -> float:
    """Cosinusoidally interpolates between two values given a weight

    Args:
        a: The starting value
        b: The ending value
        weight: The weight to interpolate by

    Returns:
        float: The interpolated value
    """
    if weight < 0:
        weight = 0
    if weight > 1:
        weight = 1

    return ((a - b) / 2) * math.cos(math.pi * weight) + ((a + b) / 2)


# noinspection SpellCheckingInspection
def eerp(a: int | float | vec, b: int | float | vec, weight: float) -> float:
    """Exponentially interpolates between two values given a weight

    Args:
        a: The starting value
        b: The ending value
        weight: The weight to interpolate by

    Returns:
        float: The interpolated value

    Raises:
        ValueError: Raised if a and b have opposite signs
    """
    if (a < 0 < b) or (a > 0 > b):
        raise ValueError('Error: \"a\" and \"b\" cannot have opposite signs')

    true_b = pow(a / b, -1)
    true_a = a

    if weight > 1:
        weight = 1
    elif weight < 0:
        weight = 0

    return true_a * pow(true_b, weight)


# ============================================================================ #
#                                  Returns int                                 #
# ============================================================================ #
def calculate_damage(sender, receiver, proj) -> int:
    """Calculates the damage a sprite receives after being hit.

    Args:
        sender: The sprite that is inflicting the damage
        receiver: The sprite taking damage
        proj: The projectile the receiver got hit by

    Returns:
        int: The damage the receiver will take
    """
    damage = math.ceil((sender.atk / receiver.defense) * proj.damage)

    return damage


# ============================================================================ #
#                                Returns string                                #
# ============================================================================ #
def triangle_collide(instig, sprite) -> str:
    """Determines where two sprites collide using a triangulation approach.

    Args:
        instig: The instigator of the collision
        sprite: The sprite being collided into

    Returns:
        str: The side the instigator struck upon the other sprite
    """
    # Bottom right corner
    point_a = vec(sprite.pos.x + sprite.hitbox.width // 2,
                  sprite.pos.y + sprite.hitbox.height // 2)

    # Top right corner
    point_b = vec(sprite.pos.x + sprite.hitbox.width // 2,
                  sprite.pos.y - sprite.hitbox.height // 2)

    # Top left corner
    point_c = vec(sprite.pos.x - sprite.hitbox.width // 2,
                  sprite.pos.y - sprite.hitbox.height // 2)

    # Bottom left corner
    point_d = vec(sprite.pos.x - sprite.hitbox.width // 2,
                  sprite.pos.y + sprite.hitbox.height // 2)

    len_point_a = get_dist_to_coords(instig.pos, point_a)
    len_point_b = get_dist_to_coords(instig.pos, point_b)
    len_point_c = get_dist_to_coords(instig.pos, point_c)
    len_point_d = get_dist_to_coords(instig.pos, point_d)

    angle_a = rad(get_angle_to_c_from_c(instig.pos, point_a) + 90)
    angle_b = rad(get_angle_to_c_from_c(instig.pos, point_b) + 90)
    angle_c = rad(get_angle_to_c_from_c(instig.pos, point_c) + 90)
    angle_d = rad(get_angle_to_c_from_c(instig.pos, point_d) + 90)

    height_ap = abs(len_point_a * sin(angle_a))
    height_bp = abs(len_point_b * cos(angle_b))
    height_cp = abs(len_point_c * sin(angle_c))
    height_dp = abs(len_point_d * cos(angle_d))

    def is_closest_side(height: float):
        if height == height_ap:
            if (height_ap < height_bp and
                    height_ap < height_cp and
                    height_ap < height_dp):
                return True
            else:
                return False

        elif height == height_bp:
            if (height_bp < height_ap and
                    height_bp < height_cp and
                    height_bp < height_dp):
                return True
            else:
                return False

        elif height == height_cp:
            if (height_cp < height_ap and
                    height_cp < height_bp and
                    height_cp < height_dp):
                return True
            else:
                return False

        elif height == height_dp:
            if (height_dp < height_ap and
                    height_dp < height_bp and
                    height_dp < height_cp):
                return True
            else:
                return False

        else:
            raise ValueError('Error: height value is not a valid input')

    if is_closest_side(height_ap):
        if instig.pos.x >= point_b.x:
            return EAST
        if instig.pos.x <= point_d.x:
            return WEST

        return SOUTH

    elif is_closest_side(height_bp):
        if instig.pos.y >= point_a.y:
            return SOUTH
        if instig.pos.y <= point_c.y:
            return NORTH

        return EAST

    elif is_closest_side(height_cp):
        if instig.pos.x >= point_b.x:
            return EAST
        if instig.pos.x <= point_d.x:
            return WEST

        return NORTH

    elif is_closest_side(height_dp):
        if instig.pos.y >= point_a.y:
            return SOUTH
        if instig.pos.y <= point_c.y:
            return NORTH

        return WEST


def wall_side_check(wall, proj) -> str:
    """Checks for which side of a wall a projectile hit and returns that value

    Args:
        wall: The wall being hit
        proj: The projectile being fired

    Returns:
        str: The side of the wall that the projectile hit
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


# ============================================================================ #
#                                Returns Vector2                               #
# ============================================================================ #
def get_top_left_coords(sprite_width: int, sprite_height: int, desired_x: float,
                        desired_y: float) -> vec:
    """Returns the coordinates of the top-left corner of a sprite that is centered at its middle.

    Args:
        sprite_width: The width of the sprite (in pixels)
        sprite_height: The height of the sprite (in pixels)
        desired_x: Where the sprite's center should be placed along the x-axis
        desired_y: Where the sprite's center should be placed along the y-axis

    Returns:
        pygame.math.Vector2: The coordinates of the sprite's top-left corner
    """
    return vec(desired_x + sprite_width // 2, desired_y + sprite_height // 2)


def get_rand_components(max_value: int | float) -> vec:
    """Given a maximum value, will output a vector containing two components that vectorially add to that value.
    The result can be positive or negative.

    Args:
        max_value: The value the components will vectorially add to. The result can add to +maxValue or -maxValue.

    Returns:
        pygame.math.Vector2: The resultant random vector
    """
    x = rand.uniform(-max_value, max_value)
    y = math.sqrt(pow(max_value, 2) - pow(x, 2))
    if rand.choice((True, False)):
        y = -y
    return vec(x, y)


# ============================================================================ #
#                                Returns Surface                               #
# ============================================================================ #
def combine_images(base_img: pygame.Surface, top_img: pygame.Surface) -> pygame.Surface:
    """Combines two images directly on top of one another

    Args:
        base_img: The image to place first
        top_img: The image being pasted on top of the first image

    Returns:
        pygame.Surface: The combined image
    """
    new_img: pygame.Surface = pygame.Surface(vec(max(base_img.get_width(), top_img.get_width())),
                                             max(base_img.get_height(), top_img.get_height()))
    center_x = (new_img.get_width() - base_img.get_width()) // 2
    center_y = (new_img.get_height() - base_img.get_height()) // 2
    new_img.blit(base_img, vec(center_x, center_y))

    center_x = (new_img.get_width() - top_img.get_width()) // 2
    center_y = (new_img.get_height() - top_img.get_height()) // 2
    new_img.blit(top_img, vec(center_x, center_y))
    new_img.set_colorkey(BLACK)
    return new_img


def text_to_image(text: str, font_img: str, char_width: int, char_height: int, char_count: int) -> pygame.Surface:
    """Converts a string of text into an image with a given font.

    Args:
        text: The text string to convert into an image
        font_img: The folder directory of the font to use
        char_width: The width of each individual character (in pixels)
        char_height: The height of each individual character (in pixels)
        char_count: The number of characters in the spritesheet (1 = 1 image in sprite sheet)

    Returns:
        pygame.Surface: The converted image
    """
    spritesheet = Spritesheet(font_img, 37)
    images = spritesheet.get_images(char_width, char_height, char_count)
    char_list = []

    final_image = pygame.Surface(vec(len(text) * char_width, char_height))

    for char in text:
        if char in LETTERS.keys():
            char_list.append(images[LETTERS[char]])
        elif char in NUMBERS:
            char_list.append(images[int(char) + 26])
        elif char in SYMBOLS:
            char_list.append(images[SYMBOLS[char] + 36])

    count = 0
    for _ in char_list:
        final_image.blit(char_list[count], vec(count * char_width, 0))
        count += 1

    final_image.set_colorkey(BLACK)
    return final_image


# ============================================================================ #
#                                Returns Sprite                                #
# ============================================================================ #
def get_closest_player(check_sprite):
    """Checks for the closest player to a given sprite.

    Args:
        check_sprite: The sprite checking for the closest player

    Returns:
        Player: The closest player to the sprite
    """
    player_coords = {}
    for a_player in all_players:
        player_coords[a_player] = get_dist_to_sprite(check_sprite, a_player)

    try:
        temp = min(player_coords.values())
        result = [key for key in player_coords if player_coords[key] == temp]
        return result[0]
    except IndexError:
        return check_sprite


def get_other_portal(portal_in):
    """Returns the other portal present in the all_portals list.

    Args:
        portal_in: The portal that is known

    Returns:
        Portal: The other portal in the all_portals list
    """
    for portal in all_portals:
        if portal != portal_in:
            return portal


# ============================================================================ #
#                                 Returns None                                 #
# ============================================================================ #
def kill_groups(*groups) -> None:
    """Calls .kill() for all sprites within one or more groups.
    """
    for group in groups:
        for entity in group:
            if hasattr(entity, 'shatter'):
                entity.shatter()
            else:
                entity.kill()


def swap_color(image: pygame.Surface, old_color: tuple, new_color: tuple) -> pygame.Surface:
    """Swaps one color of a sprite with another color.

    Args:
        image: The image to swap a color within
        old_color: The color being replaced
        new_color: The new color replacing the old color

    Returns:
        pygame.Surface: The image with the swapped color
    """
    new_img = image.copy()
    for x in range(new_img.get_width()):
        for y in range(new_img.get_height()):
            current_color = new_img.get_at((x, y))
            if current_color == old_color:
                new_img.set_at((x, y), new_color)
    return new_img


class CustomError(Exception):
    pass
