import pygame
import time
import copy

import calculations as calc
import constants as cst
import groups
import portals
from spritesheet import Spritesheet

vec = pygame.math.Vector2


def get_room():
    """Returns the room object being used

    Returns:
        Room: The central room object
    """
    return groups.all_rooms[0]


class ActorBase(pygame.sprite.Sprite):
    """The base class for all actors in the game.
    """
    def __init__(self):
        super().__init__()
        self.visible = True
        self.can_update = True
        self._layer = 1

        self.last_frame = time.time()

        self._pos = vec((0, 0))
        self.pos_copy = self._pos.copy()  # For adjusting sprites within the scrolling rooms
        
        self._room_pos = vec(0, 0)  # For maintaining position within a moving room
        
        self._vel = vec(0, 0)
        self._vel_const = vec(0, 0)  # Only for bullets; otherwise this will stay (0, 0)
        self._accel = vec(0, 0)
        self._accel_const = 0.3

        self.spritesheet = None
        self.orig_images = None
        self.orig_image = None
        self.images = None
        self.image = None
        self.index = None

        self.rect = None
        self.hitbox = None

        self.is_grappled = False
        self.grappled_by = None

    # ----------------- Setting properties ----------------- #
    @property
    def layer(self):
        """The layer the sprite should be drawn in. Higher values are drawn on top of lower values."""
        return self._layer

    @layer.setter
    def layer(self, value: int):
        self._layer = value

    @property
    def pos(self):
        """The position of the sprite according to the bounds of the screen. (0, 0) is the top left of the screen."""
        return self._pos

    @pos.setter
    def pos(self, value: pygame.math.Vector2):
        self._pos = value

    @property
    def room_pos(self):
        """The position of the sprite within its current room."""
        return self._room_pos

    @room_pos.setter
    def room_pos(self, value: pygame.math.Vector2):
        self._room_pos = value

    @property
    def vel(self):
        """The velocity of the sprite."""
        return self._vel

    @vel.setter
    def vel(self, value: pygame.math.Vector2):
        self._vel = value
        if -0.001 < self._vel.x < 0.001:
            self._vel.x = 0

    @property
    def vel_const(self):
        """The velocity constant of the sprite. It determines how fast a sprite moving with a constant velocity
        should move along the x-axis and y-axis. If the sprite moves according to acceleration and not velocity alone,
        then this value will not be used."""
        return self._vel_const

    @vel_const.setter
    def vel_const(self, value: pygame.math.Vector2):
        self._vel_const = value

    @property
    def accel(self):
        """The acceleration of the sprite."""
        return self._accel

    @accel.setter
    def accel(self, value: pygame.math.Vector2):
        self._accel = value

    @property
    def accel_const(self):
        """The acceleration constant to use when accelerating the sprite. The higher this value, the faster
        the sprite will move."""
        return self._accel_const

    @accel_const.setter
    def accel_const(self, value: int | float):
        self._accel_const = value

    # -------------------------------- Visibility -------------------------------- #
    def hide(self) -> None:
        """Makes the sprite invisible. The sprite's ``update()`` method cannot be called.
        """
        self.visible = False
        if hasattr(self, 'health_bar'):
            self.health_bar.hide()
            self.health_bar.number.hide()
        groups.all_sprites.remove(self)

    def show(self, layer_send: int) -> None:
        """Makes the sprite visible. The sprite's ``update()`` method can be called.

        Args:
            layer_send: The layer to draw the sprite onto. (Higher values are drawn on top of lower values.)

        Returns:
            None
        """
        self.visible = True
        if hasattr(self, 'health_bar'):
            self.health_bar.show(cst.LAYER['statbar'])
        groups.all_sprites.add(self, layer=layer_send)

    # ----------------------------- Images and Rects ----------------------------- #
    def set_images(self, image_file: str, frame_width: int, frame_height: int, sprites_per_row: int,
                   image_count: int, image_offset: int = 0, index: int = 0) -> None:
        """Initializes the sprite's spritesheet, images, and animations.

        Args:
            image_file: The path of the spritesheet image
            frame_width: The width of each individual frame
            frame_height: The height of each individual frame
            sprites_per_row: The number of sprites within each row of the sprite sheet
            image_count: The number of images in the sprite's animation
            image_offset: The index of the frame to begin the snip from
            index: The index of the sprite's animation to start from

        Returns:
            None
        """
        self.spritesheet = Spritesheet(image_file, sprites_per_row)
        self.orig_images = self.spritesheet.get_images(frame_width, frame_height, image_count, image_offset)
        self.images = self.spritesheet.get_images(frame_width, frame_height, image_count, image_offset)
        self.index = index

        self.render_images()

    def render_images(self) -> None:  # TODO: Update docstring
        """

        Returns:
            None
        """
        self.image = self.images[self.index]
        self.orig_image = self.orig_images[self.index]

    def set_rects(self, rect_pos_x: float, rect_pos_y: float, rect_width: int, rect_height: int,
                  hitbox_width: int, hitbox_height: int, set_pos: bool = True) -> None:
        """Defines the rect and hitbox of a sprite.

        Args:
            rect_pos_x: The x-axis position to spawn the rect and hitbox
            rect_pos_y: The y-axis position to spawn the rect and hitbox
            rect_width: The width of the rect
            rect_height: The height of the rect
            hitbox_width: The width of the hitbox
            hitbox_height: The height of the hitbox
            set_pos: Should the rect and hitbox be snapped to the position of the sprite? Is ``true`` by default.

        Returns:
            None
        """
        self.rect = pygame.Rect(rect_pos_x, rect_pos_y, rect_width, rect_height)
        self.hitbox = pygame.Rect(rect_pos_x, rect_pos_y, hitbox_width, hitbox_height)

        if set_pos:
            self.center_rects()

    def rotate_image(self, angle: float) -> None:
        """Rotates the sprite's image by a specific angle

        Args:
            angle: The angle to rotate the sprite's image by
        """
        self.orig_image = self.orig_images[self.index]
        self.image = pygame.transform.rotate(self.orig_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    # ---------------------------------- Physics --------------------------------- # 
    def center_rects(self):
        """Sets the ``rect`` and ``hitbox`` of the sprite to its position."""
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def set_room_pos(self):
        """Calculates the position of the sprite within its current room and assigns that value to self.room_pos
        """        
        room = get_room()
        self.room_pos = vec((self.pos.x - room.pos.x, self.pos.y - room.pos.y))

    def vel_movement(self, adjust_centers_first: bool) -> None:
        """Makes a sprite move according to its velocity (self.vel)

        Args:
            adjust_centers_first: Should rect and hitbox be snapped to its position before or after the vel calculation?
        """
        if adjust_centers_first:
            self.center_rects()
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y

        else:
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y
            self.center_rects()

    def accel_movement(self) -> None:
        """Makes a sprite move according to its acceleration (self.accel and self.accel_const).
        """
        self.accel.x += self.vel.x * cst.FRIC
        self.accel.y += self.vel.y * cst.FRIC
        self.vel += self.accel
        self.pos += self.vel + self.accel_const * self.accel

        self.center_rects()

    def get_accel(self) -> pygame.math.Vector2:
        """Returns the acceleration the sprite should have. (Should be overridden if the sprite does not use
        acceleration or if the sprite does not move at all).
        """
        room = get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()
        return final_accel

    def collide_check(self, *contact_lists: list) -> None:
        """Check if the sprite comes into contact with another sprite from a specific group.
        If the sprites do collide, then they will perform a hitbox collision.

        Args:
            *contact_lists: The sprite group(s) to check for a collision with

        Returns:
            None
        """
        for group in contact_lists:
            for sprite in group:
                if sprite.visible:
                    self.__block_from_side(sprite)

    def __block_from_side(self, sprite) -> None:
        if self.hitbox.colliderect(sprite.hitbox):
            width = (self.hitbox.width + sprite.hitbox.width) // 2
            height = (self.hitbox.height + sprite.hitbox.height) // 2

            # If hitting the right side
            if calc.triangle_collide(self, sprite) == cst.EAST:
                self.vel.x = 0
                self.pos.x = sprite.pos.x + width

            # Hitting bottom side
            if calc.triangle_collide(self, sprite) == cst.SOUTH:
                self.vel.y = 0
                self.pos.y = sprite.pos.y + height

            # Hitting left side
            if calc.triangle_collide(self, sprite) == cst.WEST:
                self.vel.x = 0
                self.pos.x = sprite.pos.x - width

            # Hitting top side
            if calc.triangle_collide(self, sprite) == cst.NORTH:
                self.vel.y = 0
                self.pos.y = sprite.pos.y - height

    def teleport(self, portal_in):
        portal_out = calc.get_other_portal(portal_in)
        width = (portal_out.hitbox.width + self.hitbox.width) // 2
        height = (portal_out.hitbox.height + self.hitbox.height) // 2

        dir_in = portal_in.facing
        dir_out = portal_out.facing

        def align_sprite(offset: float, direction: str) -> None:
            """Places the sprite in the correct spot after teleporting.

            Args:
                offset: The difference between the sprite's position and the entering portal's center
                direction: The direction the exiting portal is facing

            Returns:
                None
            """
            if direction == cst.SOUTH:
                self.pos.x = portal_out.pos.x - offset
                self.pos.y = portal_out.pos.y + height + abs(vel_adjust.y)

            elif direction == cst.EAST:
                self.pos.x = portal_out.pos.x + width + abs(vel_adjust.x)
                self.pos.y = portal_out.pos.y - offset

            elif direction == cst.NORTH:
                self.pos.x = portal_out.pos.x + offset
                self.pos.y = portal_out.pos.y - height - abs(vel_adjust.y)

            elif direction == cst.WEST:
                self.pos.x = portal_out.pos.x - width - abs(vel_adjust.x)
                self.pos.y = portal_out.pos.y + offset

        def rotate_vel() -> None:
            align_sprite(dist_offset, dir_out)
            self.vel_const = self.vel_const.rotate(dir_list[dir_out])
            self.vel = self.vel.rotate(dir_list[dir_out])

        # Makes sure that sprites don't repeatedly get thrown back into the portals b/c of room velocity
        room = get_room()
        vel_adjust: vec = room.vel.copy()

        dir_list = {cst.SOUTH: 180, cst.EAST: 90, cst.NORTH: 0, cst.WEST: 270}

        if dir_in == cst.SOUTH:
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            rotate_vel()

        elif dir_in == cst.EAST:
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            dir_list.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            rotate_vel()

        elif dir_in == cst.NORTH:
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            dir_list.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            rotate_vel()

        elif dir_in == cst.WEST:
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            dir_list.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            rotate_vel()

    def __animate(self) -> None:
        """Runs the animation sequence of the sprite.
        """
        pass


class AbstractBase(pygame.sprite.AbstractGroup):
    """The base class for all standard abstract groups. Contains methods to help manipulate the abstract group.
    """
    def __init__(self):
        super().__init__()
        self.can_update = True
    
    # def add(self, *sprites):
    #     """Adds one or more sprites to the abstract group.
    #
    #     ### Arguments
    #         - sprites (``pygame.sprite.Sprite``): The sprite(s) to add to the group
    #     """
    #     for sprite in sprites:
    #         super().add(sprite)
