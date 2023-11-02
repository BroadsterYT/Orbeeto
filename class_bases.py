import copy

from calculations import *
from constants import *
from groups import *
from spritesheet import Spritesheet


def get_room():
    """Returns the room object being used

    Returns:
        Room: The central room object
    """
    return all_rooms[0]


class ActorBase(pygame.sprite.Sprite):
    def __init__(self):
        """The base class for all actors in the game.
        """
        super().__init__()
        self.visible = True
        self.canUpdate = True
        self.lastFrame = time.time()

        self.pos = vec((0, 0))
        self.posCopy = self.pos.copy()  # For adjusting sprites within the scrolling rooms
        
        self.roomPos = vec(0, 0)  # For maintaining position within a moving room
        
        self.vel = vec(0, 0)
        self.cVel = vec(0, 0)  # Only for bullets; otherwise this will stay (0, 0)
        self.accel = vec(0, 0)
        self.cAccel = 0.3

        self.spritesheet = None
        self.origImages = None
        self.origImage = None
        self.images = None
        self.image = None
        self.index = None

        self.rect = None
        self.hitbox = None

        self.isGrappled = False
        self.grappledBy = None
        self.grappleHurtTime = time.time()
    
    # -------------------------------- Visibility -------------------------------- #
    def hide(self) -> None:
        """Makes the sprite invisible. The sprite's ``update()`` method will not be called.
        """
        self.visible = False
        if hasattr(self, 'healthBar'):
            self.healthBar.hide()
            self.healthBar.number.hide()
        all_sprites.remove(self)

    def show(self, layer_send: str) -> None:
        """Makes the sprite visible. The sprite's ``update()`` method will be called.
        
        ### Parameters
            - layer_send (``str``): The layer the sprite should be added to
        """        
        self.visible = True
        if hasattr(self, 'healthBar'):
            self.healthBar.show(LAYER['statbar'])
        all_sprites.add(self, layer=layer_send)

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
            None:

        """
        self.spritesheet = Spritesheet(image_file, sprites_per_row)
        self.origImages = self.spritesheet.get_images(frame_width, frame_height, image_count, image_offset)
        self.images = self.spritesheet.get_images(frame_width, frame_height, image_count, image_offset)
        self.index = index

        self.render_images()

    def render_images(self):
        self.image = self.images[self.index]
        self.origImage = self.origImages[self.index]

    def set_rects(self, rect_pos_x: float, rect_pos_y: float, rect_width: int, rect_height: int,
                  hitbox_width: int, hitbox_height: int, set_pos: bool = True):
        """Defines the rect and hitbox of a sprite
        
        ### Parameters
            - rectPosX (``int``): The x-axis position to spawn the rect and hitbox
            - rectPosY (``int``): The y-axis position to spawn the rect and hitbox
            - rectWidth (``int``): The width of the rect
            - rectHeight (``int``): The height of the rect
            - hitboxWidth (``int``): The width of the hitbox
            - hitboxHeight (``int``): The height of the hitbox
            - setPos (``bool``, optional): Should the rect and hitbox be snapped to the position of the sprite?.
              Defaults to ``True``.
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
        self.origImage = self.origImages[self.index]
        self.image = pygame.transform.rotate(self.origImage, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    # ---------------------------------- Physics --------------------------------- # 
    def center_rects(self):
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def set_room_pos(self):
        """Calculates the position of the sprite within its current room and assigns that value to self.roomPos
        """        
        room = get_room()
        self.roomPos = vec((self.pos.x - room.pos.x, self.pos.y - room.pos.y))

    def vel_movement(self, adjust_centers_first: bool) -> None:
        """Makes a sprite move according to its velocity (self.vel)

        Args:
            adjust_centers_first: Should rect and hitbox be snapped to its position before or after the vel calculation?

        Returns:
            None:

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
        """Makes a sprite move according to its acceleration (self.accel and self.cAccel).
        """
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel
        self.pos += self.vel + self.cAccel * self.accel

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
        
        ### Arguments
            - contactLists (``list``): The sprite group(s) to check for a collision with
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
            if triangle_collide(self, sprite) == EAST:
                self.vel.x = 0
                self.pos.x = sprite.pos.x + width

            # Hitting bottom side
            if triangle_collide(self, sprite) == SOUTH:
                self.vel.y = 0
                self.pos.y = sprite.pos.y + height

            # Hitting left side
            if triangle_collide(self, sprite) == WEST:
                self.vel.x = 0
                self.pos.x = sprite.pos.x - width

            # Hitting top side
            if triangle_collide(self, sprite) == NORTH:
                self.vel.y = 0
                self.pos.y = sprite.pos.y - height

    def teleport(self, portal_in):
        portal_out = get_other_portal(portal_in)
        width = (portal_out.hitbox.width + self.hitbox.width) // 2
        height = (portal_out.hitbox.height + self.hitbox.height) // 2

        dir_in = portal_in.facing
        dir_out = portal_out.facing

        def align_sprite(offset: float, direction: str) -> None:
            """Places the sprite in the correct spot after teleporting.
            
            ### Arguments
                - offset (``float``): The difference between the sprite's position and the entering portal's center
                - direction (``str``): The direction the exiting portal is facing
            """            
            if direction == SOUTH:
                self.pos.x = portal_out.pos.x - offset
                self.pos.y = portal_out.pos.y + height + abs(vel_adjust.y)

            elif direction == EAST:
                self.pos.x = portal_out.pos.x + width + abs(vel_adjust.x)
                self.pos.y = portal_out.pos.y - offset

            elif direction == NORTH:
                self.pos.x = portal_out.pos.x + offset
                self.pos.y = portal_out.pos.y - height - abs(vel_adjust.y)

            elif direction == WEST:
                self.pos.x = portal_out.pos.x - width - abs(vel_adjust.x)
                self.pos.y = portal_out.pos.y + offset

        def rotate_vel() -> None:
            align_sprite(dist_offset, dir_out)
            self.cVel = self.cVel.rotate(dir_list[dir_out])
            self.vel = self.vel.rotate(dir_list[dir_out])

        # Makes sure that sprites don't repeatedly get thrown back into the portals b/c of room velocity
        room = get_room()
        vel_adjust: vec = room.vel.copy()

        dir_list = {SOUTH: 180, EAST: 90, NORTH: 0, WEST: 270}

        if dir_in == SOUTH:
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            rotate_vel()

        elif dir_in == EAST:
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            dir_list.update({EAST: 180, NORTH: 90, WEST: 0, SOUTH: 270})
            rotate_vel()

        elif dir_in == NORTH:
            dist_offset = copy.copy(self.pos.x) - copy.copy(portal_in.pos.x)
            dir_list.update({NORTH: 180, WEST: 90, SOUTH: 0, EAST: 270})
            rotate_vel()

        elif dir_in == WEST:
            dist_offset = copy.copy(self.pos.y) - copy.copy(portal_in.pos.y)
            dir_list.update({WEST: 180, SOUTH: 90, EAST: 0, NORTH: 270})
            rotate_vel()

    def __animate(self) -> None:
        """Runs the animation sequence of the sprite.
        """
        pass


class AbstractBase(pygame.sprite.AbstractGroup):
    def __init__(self):
        """The base class for all standard abstract groups. Contains methods to help manipulate the abstract group.
        """
        super().__init__()
        self.canUpdate = True
    
    # def add(self, *sprites):
    #     """Adds one or more sprites to the abstract group.
    #
    #     ### Arguments
    #         - sprites (``pygame.sprite.Sprite``): The sprite(s) to add to the group
    #     """
    #     for sprite in sprites:
    #         super().add(sprite)
