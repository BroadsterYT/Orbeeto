"""
Contains all important global calculations.
"""
import math
import random as rand
import time
import timeit

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl

import constants as cst
import enemies
import groups
import timer


# ============================================================================ #
#                                 Returns float                                #
# ============================================================================ #
def get_angle_to_mouse(any_sprite) -> float:
    """Returns the angle between a sprite and the mouse cursor.

    :param any_sprite: The sprite to measure the angle from
    :return: The angle between the sprite and the mouse cursor
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    length_to_x = mouse_x - any_sprite.pos.x
    length_to_y = mouse_y - any_sprite.pos.y
    len_vec = vec(-length_to_x, -length_to_y)
    return len_vec.angle_to(vec(cst.WINWIDTH // 2, cst.WINHEIGHT // 2)) + 60


def get_angle(first_obj, sec_obj) -> float:
    """Returns the angle between two sprites/coordinates

    :param first_obj: The first object
    :param sec_obj: The second object
    :return: The angle between the two objects
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
                return 270
            else:
                return 90
        else:
            if length_to_y > 0:
                return 180
            else:
                return 0


def get_dist(first_input, sec_input) -> float:
    """Returns the distance between two coordinates.

    :param first_input: The position to start the measure from
    :param sec_input: The position to measure the distance from the first
    :return: The distance between the two locations
    """
    # if isinstance(first_input, vec):
    #     first_vec = first_input
    # else:
    #     first_vec = first_input.pos
    #
    # if isinstance(sec_input, vec):
    #     sec_vec = sec_input
    # else:
    #     sec_vec = sec_input.pos

    # length_x = sec_vec.x - first_vec.x
    # length_y = sec_vec.y - first_vec.y

    length_x = sec_input.x - first_input.x
    length_y = sec_input.y - first_input.y

    return math.sqrt(length_x ** 2 + length_y ** 2)


def get_vec_angle(vec_x: int | float, vec_y: int | float) -> float:
    """Returns the angle of a resultant vector

    :param vec_x: The x-axis component of the vector
    :param vec_y: The y-axis component of the vector
    :return: The angle of the resultant vector (in degrees)
    """
    if vec_x and vec_y != 0:
        vec_angle = -math.degrees(math.atan2(vec_y, vec_x)) - 90
        return vec_angle
    else:
        if vec_y == 0:
            if vec_x > 0:
                return 270
            else:
                return 90
        else:
            if vec_y > 0:
                return 180
            else:
                return 0


def get_time_diff(time_value: float) -> float:
    """Returns the difference between the current time and another.

    :param time_value: The time to compare to the current time
    :return: The difference between the current time and the other time
    """
    return time.time() - time_value


def get_game_tdiff(time_value: float) -> float:  # noqa
    """Returns the difference between the game time and the given time.

    :param time_value: The value to compare to the game time
    :return: The difference between the game time and the given time
    """
    return timer.g_timer.time - time_value


# ------------------------------ Math Functions ------------------------------ #
# noinspection SpellCheckingInspection
def cerp(a: int | float, b: int | float, weight: float) -> float:
    """Cosinusoidally interpolates between two values given a weight

    :param a: The starting value
    :param b: The ending value
    :param weight: The weight to interpolate by
    :return: The interpolated value
    """
    if weight < 0:
        weight = 0
    if weight > 1:
        weight = 1

    return ((a - b) / 2) * math.cos(math.pi * weight) + ((a + b) / 2)


# noinspection SpellCheckingInspection
def eerp(a: int | float, b: int | float, weight: float) -> float:
    """Exponentially interpolates between two values given a weight

    :param a: The starting value
    :param b: The ending value
    :param weight: The weight to interpolate by
    :return: The interpolated value
    :raises ValueError: Raised if a and b have opposite signs
    """
    if (a < 0 < b) or (a > 0 > b):
        raise ValueError('Error: \"a\" and \"b\" cannot have opposite signs')

    true_b = b / a
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

    :param receiver: The sprite taking damage
    :param proj: The projectile the receiver got hit by
    :return: The damage the receiver will take
    """
    damage = math.ceil(proj.damage / ((receiver.defense * 100) / 100))
    if damage <= 0:
        damage = 1

    return damage


# ============================================================================ #
#                                Returns string                                #
# ============================================================================ #
def get_opposite(value):
    """Returns the value opposite of the input

    :param value: The value to get the opposite of
    :return: The opposite of the input
    """
    match value:
        # ---------- str inputs ---------- #
        case cst.SOUTH:
            return cst.NORTH
        case cst.EAST:
            return cst.WEST
        case cst.NORTH:
            return cst.SOUTH
        case cst.WEST:
            return cst.EAST

        # ---------- int inputs ---------- #
        case ctrl.K_MOVE_DOWN:
            return ctrl.K_MOVE_UP
        case ctrl.K_MOVE_RIGHT:
            return ctrl.K_MOVE_LEFT
        case ctrl.K_MOVE_UP:
            return ctrl.K_MOVE_DOWN
        case ctrl.K_MOVE_LEFT:
            return ctrl.K_MOVE_RIGHT


def triangle_collide(instig, sprite) -> str:
    """Determines where two sprites collide using a triangulation approach

    :param instig: The instigator of the collision
    :param sprite: The sprite being collided into
    :return: The side the instigator struck upon the other sprite

                    Side C
                +------------+
                +            +
        Side D  +            +  Side B
                +            +
                +------------+
                    Side A
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

    # height_ap = abs(get_dist(instig.pos, point_a) * math.sin(angle_a))
    # height_bp = abs(get_dist(instig.pos, point_b) * math.cos(angle_b))
    # height_cp = abs(get_dist(instig.pos, point_c) * math.sin(angle_c))
    # height_dp = abs(get_dist(instig.pos, point_d) * math.cos(angle_d))

    def is_closest_side(height: float) -> bool:
        """Determines if the given distance is the one closest to the instigator (the shortest)

        :param height: The distance from a side to the instigator
        :return: If the distance is the shortest (True) or not (False)
        """
        height_list = [height_ap, height_bp, height_cp, height_dp]
        height_list.remove(height)

        output = True
        for dist in height_list:
            if not (height < dist):
                output = False
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


# def is_closest_side(height_a: float, height_b: float, height_c: float, height_d: float, height_comp: float) -> bool:
#     height_list = np.array([height_a, height_b, height_c, height_d], dtype=float)
#
#     output = True
#     for dist in height_list:
#         if height_comp < dist:
#             output = True
#         else:
#             output = False
#             break
#     return output


# ============================================================================ #
#                                Returns Vector2                               #
# ============================================================================ #
def get_rand_components(max_value: int | float) -> vec:
    """Given a maximum value, will output a vector containing two components that vectorially add to that value.
    The result can be positive or negative.

    :param max_value: The value the components will vectorially add to. The result can add to +max_value or -max_value.
    :return: The resultant random vector
    """
    x = rand.uniform(-max_value, max_value)
    y = math.sqrt(pow(max_value, 2) - pow(x, 2))
    if rand.choice((True, False)):
        y = -y
    return vec(x, y)


def get_scroll_weight(obj) -> vec:
    """Returns the weight an object's acceleration should use when centering the screen.

    :param obj: The object being centered on the screen
    :return: The acceleration weight vector to use during a room scroll
    """
    mult = 2.5
    scroll_weight = vec(
        -mult * math.tan((math.pi / (2 * cst.WINWIDTH)) * obj.pos.x - math.pi / 4),
        -mult * math.tan((math.pi / (2 * cst.WINHEIGHT)) * obj.pos.y - math.pi / 4)
    )
    return scroll_weight


class ScreenShakeQueue:
    """An object that handles screen-shaking capabilities."""

    def __init__(self):
        self.queue = []

    def add(self, amplitude: int | float, duration: int, rate_of_decay: int | float = 1.2) -> None:
        """Adds a screen shake to the queue of screen shakes.

        :param amplitude: How intense the shake should be
        :param duration: How long the shake should last
        :param rate_of_decay: The intensity of the decay. Set to 1.2 by default. Should be greater than or equal to 0.
        :return: None
        """
        new_queue = []
        for tick in range(duration):
            decay = (pow(duration - tick, rate_of_decay)) / pow(duration, rate_of_decay)
            queue_input = vec(rand.uniform(-amplitude, amplitude) * decay, rand.uniform(-amplitude, amplitude) * decay)
            new_queue.append(queue_input)

        self.queue = self._combine_queues(new_queue)

    def _combine_queues(self, waiting_queue):
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
#                                Returns Sprite                                #
# ============================================================================ #
def get_closest_player():
    """Checks for the closest player to a given sprite.

    Returns:
        Player: The closest player to the sprite
    """
    for sprite in groups.all_players:  # No need to do full linear search, there's only one player
        return sprite


def get_other_portal(portal_in):
    """Returns the other portal present in the all_portals list.

    :param portal_in: The portal that is known
    :return: The other portal in the all_portals list
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

    :param image: The image to swap a color within
    :param old_color: The color being replaced
    :param new_color: The new color replacing the old color
    :return: The image with the swapped color
    """
    new_img = image.copy()
    for x in range(new_img.get_width()):
        for y in range(new_img.get_height()):
            current_color = new_img.get_at((x, y))
            if current_color == old_color:
                new_img.set_at((x, y), new_color)
    return new_img


if __name__ == '__main__':
    import rooms
    import constants as cst

    main_room = rooms.Room(0, 0)
    instig_test = enemies.StandardGrunt(200.590643, 500.42378293)
    sprite_test = enemies.StandardGrunt(300.475234, 875.5463)
    timer = time.time()

    print(timeit.timeit('get_dist(instig_test.pos, sprite_test.pos)', number=10000, globals=globals()))
