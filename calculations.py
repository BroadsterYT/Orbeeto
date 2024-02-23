import random as rand
import math
import time

import pygame
from pygame.math import Vector2 as vec
from text import fontinfo

import constants as cst
import groups
import spritesheet


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
                return -90
            else:
                return 90
        else:
            if length_to_y > 0:
                return -180
            else:
                return 0


def get_angle(first_obj, sec_obj) -> float:
    """Returns the angle between two sprites/coordinates

    Args:
        first_obj: The first object
        sec_obj: The second object

    Returns:
        float: The angle between the two objects
    """
    if type(first_obj) is pygame.math.Vector2:
        first_pos = first_obj.copy()
    else:
        first_pos = first_obj.pos

    if type(sec_obj) is pygame.math.Vector2:
        sec_pos = sec_obj.copy()
    else:
        sec_pos = sec_obj.pos

    length_to_x = sec_pos.x - first_pos.x
    length_to_y = sec_pos.y - first_pos.y

    if length_to_x and length_to_y != 0:
        angle = -math.degrees(math.atan2(length_to_y, length_to_x)) - 90
        return angle
    else:
        if length_to_y == 0:
            if length_to_x > 0:
                return -90
            else:
                return 90
        else:
            if length_to_y > 0:
                return -180
            else:
                return 0


def get_dist(first_input, sec_input) -> float:
    """Returns the distance between two sprites or coordinates.

    Args:
        first_input: The object to start the measure from
        sec_input: The second object to measure the distance from the first

    Returns:
        float: The distance between the two objects
    """
    if type(first_input) is pygame.math.Vector2:
        first_vec = first_input
    else:
        first_vec = first_input.pos

    if type(sec_input) is pygame.math.Vector2:
        sec_vec = sec_input
    else:
        sec_vec = sec_input.pos

    length_x = sec_vec.x - first_vec.x
    length_y = sec_vec.y - first_vec.y

    return math.sqrt(length_x**2 + length_y**2)


def get_vec_angle(vec_x: int | float, vec_y: int | float) -> float:
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
                return -90
            else:
                return 90
        else:
            if vec_y > 0:
                return -180
            else:
                return 0


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
def cerp(a: int | float, b: int | float, weight: float) -> float:
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
def eerp(a: int | float, b: int | float, weight: float) -> float:
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
def calculate_damage(receiver, proj) -> int:
    """Calculates the damage a sprite receives after being hit.

    Args:
        receiver: The sprite taking damage
        proj: The projectile the receiver got hit by

    Returns:
        int: The damage the receiver will take
    """
    damage = math.ceil(proj.damage - receiver.defense)
    if damage <= 0:
        damage = 1

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

    len_point_a = get_dist(instig.pos, point_a)
    len_point_b = get_dist(instig.pos, point_b)
    len_point_c = get_dist(instig.pos, point_c)
    len_point_d = get_dist(instig.pos, point_d)

    angle_a = math.radians(get_angle(instig.pos, point_a) + 90)
    angle_b = math.radians(get_angle(instig.pos, point_b) + 90)
    angle_c = math.radians(get_angle(instig.pos, point_c) + 90)
    angle_d = math.radians(get_angle(instig.pos, point_d) + 90)

    height_ap = abs(len_point_a * math.sin(angle_a))
    height_bp = abs(len_point_b * math.cos(angle_b))
    height_cp = abs(len_point_c * math.sin(angle_c))
    height_dp = abs(len_point_d * math.cos(angle_d))

    def is_closest_side(height: float) -> bool:
        """Determines if the given distance is the one closest to the instigator (the shortest)

        Args:
            height: The distance from a side to the instigator

        Returns:
            bool: If the distance is the shortest (True) or not (False)
        """
        height_list = [height_ap, height_bp, height_cp, height_dp]
        height_list.remove(height)

        output = True
        for dist in height_list:
            if height < dist:
                output = True
            else:
                output = False
                break
        return output

    if is_closest_side(height_ap):
        if instig.pos.x >= point_b.x:
            return cst.EAST
        if instig.pos.x <= point_d.x:
            return cst.WEST
        return cst.SOUTH

    elif is_closest_side(height_bp):
        if instig.pos.y >= point_a.y:
            return cst.SOUTH
        if instig.pos.y <= point_c.y:
            return cst.NORTH
        return cst.EAST

    elif is_closest_side(height_cp):
        if instig.pos.x >= point_b.x:
            return cst.EAST
        if instig.pos.x <= point_d.x:
            return cst.WEST
        return cst.NORTH

    elif is_closest_side(height_dp):
        if instig.pos.y >= point_a.y:
            return cst.SOUTH
        if instig.pos.y <= point_c.y:
            return cst.NORTH
        return cst.WEST


# ============================================================================ #
#                               Returns iterator                               #
# ============================================================================ #
def chain(*iterables):
    """Given multiple iterables, will return a generator containing all elements of all iterables.

    Args:
        *iterables: The iterables to chain together

    Returns:
        A generator containing all elements of all iterables
    """
    for it in iterables:
        for element in it:
            yield element


# ============================================================================ #
#                                Returns Vector2                               #
# ============================================================================ #
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


def get_scroll_weight(obj) -> vec:
    """Returns the weight an object's acceleration should use when centering the screen.

    Args:
        obj: The object being centered on the screen

    Returns:
        The acceleration weight vector to use during a room scroll
    """
    mult = 2
    scroll_weight = vec(
        -mult * math.tan((math.pi / (2 * cst.WINWIDTH)) * obj.pos.x - math.pi / 4),
        -mult * math.tan((math.pi / (2 * cst.WINHEIGHT)) * obj.pos.y - math.pi / 4)
    )
    return scroll_weight


class ScreenShakeQueue:
    """An object that handles screen-shaking capabilities."""
    def __init__(self):
        self.queue = []

    def add(self, amplitude: int | float, duration: int, rate_of_decay: int | float = 1) -> None:
        """Adds a screen shake to the queue of screen shakes.

        Args:
            amplitude: How intense the shake should be
            duration: How long the shake should last
            rate_of_decay: The intensity of the decay. Set to 1 by default. Should be greater than or equal to 0.
        """
        new_queue = []
        for tick in range(duration):
            decay = (pow(duration - tick, rate_of_decay)) / pow(duration, rate_of_decay)
            queue_input = vec(rand.uniform(-amplitude, amplitude) * decay, rand.uniform(-amplitude, amplitude) * decay)
            new_queue.append(queue_input)

        self.queue = self.__combine_queues(new_queue)

    def __combine_queues(self, waiting_queue):
        combined_list = []
        max_length = max(len(self.queue), len(waiting_queue))

        for i in range(max_length):
            value1 = self.queue[i] if i < len(self.queue) else vec(0, 0)
            value2 = waiting_queue[i] if i < len(waiting_queue) else vec(0, 0)
            combined_list.append(value1 + value2)

        return combined_list

    def run(self):
        if len(self.queue) != 0:
            output = self.queue[0]
            self.queue.pop(0)
            return output
        else:
            return vec(0, 0)


screen_shake_queue = ScreenShakeQueue()


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
    new_img.set_colorkey(cst.BLACK)
    return new_img


def text_to_image(text: str, a_font: fontinfo.Font) -> pygame.Surface:
    """Converts a string of text into an image with a given font.

    Args:
        text: The text string to convert into an image
        a_font: The font object to retrieve font data from

    Returns:
        pygame.Surface: The converted image
    """
    sheet = spritesheet.Spritesheet(a_font.path, a_font.chars_per_row)
    images = sheet.get_images(a_font.char_width, a_font.char_height, a_font.char_count)
    char_list = []

    final_image = pygame.Surface(vec(len(text) * a_font.char_width, a_font.char_height))

    # TODO: Make all fonts follow the same text-to-image logic
    if a_font.path == 'sprites/ui/font.png' or a_font.path == 'sprites/ui/small_font.png':
        for char in text:
            if char in cst.LETTERS.keys():
                char_list.append(images[cst.LETTERS[char]])
            elif char in cst.NUMBERS:
                char_list.append(images[int(char) + 26])
            elif char in cst.SYMBOLS:
                char_list.append(images[cst.SYMBOLS[char] + 36])
    else:
        for char in text:
            if char in cst.UPPERCASE.keys():
                char_list.append(images[cst.UPPERCASE[char]])
            elif char in cst.LOWERCASE.keys():
                char_list.append(images[cst.LOWERCASE[char]])
            elif char in cst.NEW_NUMBERS.keys():
                char_list.append(images[cst.NEW_NUMBERS[char]])
            elif char in cst.NEW_SYMBOLS.keys():
                char_list.append(images[cst.NEW_SYMBOLS[char]])

    count = 0
    for _ in char_list:
        final_image.blit(char_list[count], vec(count * a_font.char_width, 0))
        count += 1

    final_image.set_colorkey(cst.BLACK)
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
    for a_player in groups.all_players:
        player_coords[a_player] = get_dist(check_sprite, a_player)

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
    for portal in groups.all_portals:
        if portal != portal_in:
            return portal


# ============================================================================ #
#                                 Returns None                                 #
# ============================================================================ #
def kill_groups(*any_groups) -> None:
    """Calls ``.kill()`` for all sprites within one or more groups.
    """
    for group in any_groups:
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
