import sys
from math import sin, cos

from bullets import *
from enemies import *
from statbars import *
from tiles import *
from trinkets import *

# Aliases
spriteGroup = pygame.sprite.Group

clock = pygame.time.Clock()

screenSize = (WINWIDTH, WINHEIGHT)
screen = pygame.display.set_mode(screenSize, pygame.SCALED, 0, 0, 1)
pygame.display.set_caption('Orbeeto')


# ============================================================================ #
#                                 Player Class                                 #
# ============================================================================ #
class Player(ActorBase):
    def __init__(self):
        """A player sprite that can move and shoot."""
        super().__init__()
        all_players.add(self)
        self.show(LAYER['player'])

        self.room = get_room()

        self.set_images("sprites/orbeeto/orbeeto.png", 64, 64, 5, 5)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self.pos = vec((WINWIDTH // 2, WINHEIGHT // 2))
        self.cAccel = 0.58

        # -------------------------------- Game Stats -------------------------------- #
        self.xp: int = 0
        self.level: int = 0
        self.maxLevel: int = 249

        self.maxHp: int = 50
        self.hp: int = self.maxHp
        self.maxAtk: int = 10
        self.atk: int = self.maxAtk
        self.maxDef: int = 10
        self.defense: int = self.maxDef

        self.maxAmmo: int = 40
        self.ammo: int = self.maxAmmo
        self.bulletVel: float = 12.0
        self.gunCooldown: float = 0.12
        self.lastShot: float = time.time()

        self.grappleSpeed: float = 2.0

        self.hitTimeCharge = 1200
        self.hitTime = 0
        self.lastHit = time.time()

        self.update_level()

        # --------------------------------- Stat Bars -------------------------------- #
        self.healthBar = HealthBar(self)
        self.dodgeBar = DodgeBar(self)
        self.ammoBar = AmmoBar(self)

        self.menu = InventoryMenu(self)

        self.inventory = {}
        for item in MAT.values():
            self.inventory.update({item: 0})

        # ---------------------- Bullets, Portals, and Grapples ---------------------- #
        self.bulletType = PROJ_STD
        self.canPortal = False
        self.canGrapple = True
        self.grapple = None

    # ----------------------------------- Stats ---------------------------------- #
    def update_max_stats(self):
        """Updates all the player's max stats."""
        self.maxHp = floor(eerp(50, 650, self.level / self.maxLevel))
        self.maxAtk = floor(eerp(10, 1250, self.level / self.maxLevel))
        self.maxDef = floor(eerp(15, 800, self.level / self.maxLevel))
        self.maxAmmo = floor(eerp(40, 1200, self.level / self.maxLevel))

        self.grappleSpeed = floor(eerp(2.0, 4.0, self.level / self.maxLevel))

        self.atk = self.maxAtk
        self.defense = self.maxDef

    def update_level(self):
        if self.xp > 582803:
            self.xp = 582803

        self.level = floor((256 * self.xp) / (self.xp + 16384))
        self.update_max_stats()

    # ------------------------------- Room Changing ------------------------------ #
    def change_room(self, direction: str) -> None:
        """Changes the player's current room
        
        ### Arguments
            - direction (``str``): The direction of the new room the player is traveling to
        
        ### Raises
            - ``ValueError``: Raised if the direction is not `NORTH`, `SOUTH`, `EAST`, or `WEST`
        """
        if direction == SOUTH:
            self.room.room.y -= 1
            self.room.lastEntranceDir = SOUTH
            self.room.layout_update()

        elif direction == EAST:
            self.room.room.x += 1
            self.room.lastEntranceDir = EAST
            self.room.layout_update()

        elif direction == NORTH:
            self.room.room.y += 1
            self.room.lastEntranceDir = NORTH
            self.room.layout_update()

        elif direction == WEST:
            self.room.room.x -= 1
            self.room.lastEntranceDir = WEST
            self.room.layout_update()

        else:
            raise ValueError(f'Error: {direction} is not a valid room-changing direction.')

        kill_groups(all_projs)

    def check_room_change(self) -> None:
        """Checks if the player should change rooms
        """
        if self.hitbox.colliderect(self.room.borderSouth.hitbox):
            self.change_room(SOUTH)

        if self.hitbox.colliderect(self.room.borderEast.hitbox):
            self.change_room(EAST)

        if self.hitbox.colliderect(self.room.borderNorth.hitbox):
            self.change_room(NORTH)

        if self.hitbox.colliderect(self.room.borderWest.hitbox):
            self.change_room(WEST)

    # --------------------------------- Movement --------------------------------- #
    def movement(self):
        """When called once every frame, it allows the player to receive input from the user and move accordingly
        """
        if self.canUpdate and self.visible:
            if not self.room.isScrollingX and not self.room.isScrollingY:
                self.collide_check(all_walls)

            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        """Returns the acceleration that the player should undergo given specific conditions
        
        ### Returns
            - ``pygame.math.Vector2``: The acceleration value of the player
        """
        final_accel = vec(0, 0)
        if not self.room.isScrollingX:
            final_accel.x += self.__get_x_axis_output()

        if not self.room.isScrollingY:
            final_accel.y += self.__get_y_axis_output()

        return final_accel

    def __get_x_axis_output(self) -> float:
        output: float = 0.0
        if isInputHeld[K_a]:
            output -= self.cAccel
        if isInputHeld[K_d]:
            output += self.cAccel

        if self.is_swinging():
            angle = get_angle_to_sprite(self, self.grapple)
            output += self.grappleSpeed * -sin(rad(angle))

        return output

    def __get_y_axis_output(self) -> float:
        output: float = 0.0
        if isInputHeld[K_w]:
            output -= self.cAccel
        if isInputHeld[K_s]:
            output += self.cAccel

        if self.is_swinging():
            angle = get_angle_to_sprite(self, self.grapple)
            output += self.grappleSpeed * -cos(rad(angle))

        return output

    def is_swinging(self) -> bool:
        """Determines if the player should be accelerating towards the grappling hook.

        Returns:
            bool: Whether the player is swinging
        """
        output = False
        if self.grapple is None:
            return output
        elif not self.grapple.returning:
            return output
        elif self.grapple.grappledTo not in all_walls:
            return output
        else:
            output = True
            return output

    def shoot(self):
        """Shoots bullets.
        """
        angle = rad(get_angle_to_mouse(self))
        vel_x = self.bulletVel * -sin(angle)
        vel_y = self.bulletVel * -cos(angle)

        offset = vec((21, 30))

        if (isInputHeld[1] and
                self.ammo > 0 and
                get_time_diff(self.lastShot) >= self.gunCooldown):
            if self.bulletType == PROJ_STD:
                all_projs.add(
                    PlayerStdBullet(self,
                                    self.pos.x - (offset.x * cos(angle)) - (offset.y * sin(angle)),
                                    self.pos.y + (offset.x * sin(angle)) - (offset.y * cos(angle)),
                                    vel_x, vel_y, 1
                                    ),

                    PlayerStdBullet(self,
                                    self.pos.x + (offset.x * cos(angle)) - (offset.y * sin(angle)),
                                    self.pos.y - (offset.x * sin(angle)) - (offset.y * cos(angle)),
                                    vel_x, vel_y, 1
                                    )
                )

            elif self.bulletType == PROJ_LASER:
                all_projs.add(
                    PlayerLaserBullet(self,
                                      self.pos.x - (offset.x * cos(angle)) - (offset.y * sin(angle)),
                                      self.pos.y + (offset.x * sin(angle)) - (offset.y * cos(angle)),
                                      vel_x * 2, vel_y * 2, 1
                                      ),

                    PlayerLaserBullet(self,
                                      self.pos.x + (offset.x * cos(angle)) - (offset.y * sin(angle)),
                                      self.pos.y - (offset.x * sin(angle)) - (offset.y * cos(angle)),
                                      vel_x * 2, vel_y * 2, 1
                                      )
                )

            self.ammo -= 1
            self.lastShot = time.time()

        # ------------------------------ Firing Portals ------------------------------ #
        if keyReleased[3] % 2 == 0 and self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, vel_x * 0.75, vel_y * 0.75))
            self.canPortal = False

        elif keyReleased[3] % 2 != 0 and not self.canPortal and self.canGrapple:
            all_projs.add(PortalBullet(self, self.pos.x, self.pos.y, vel_x * 0.75, vel_y * 0.75))
            self.canPortal = True

        # --------------------------- Firing Grappling Hook -------------------------- #
        if keyReleased[2] % 2 != 0 and self.canGrapple:
            if self.grapple is not None:
                self.grapple.shatter()
            self.grapple = NewGrappleBullet(self, self.pos.x, self.pos.y, vel_x, vel_y)
            self.canGrapple = False

        if keyReleased[2] % 2 == 0 and not self.canGrapple:
            self.grapple.returning = True
            self.canGrapple = True

    def update(self):
        if self.canUpdate and self.visible:
            self.movement()
            self.shoot()
            self.check_room_change()

            # Animation
            self.__animate()
            self.rotate_image(get_angle_to_mouse(self))

            # Teleporting
            if not self.room.isScrollingX and not self.room.isScrollingY:
                for portal in all_portals:
                    if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                        self.teleport(portal)

            # Dodge charge up
            if self.hitTime < self.hitTimeCharge:
                self.hitTime += 1

        self.menu.update()

        if self.hp <= 0:
            self.kill()

    def __animate(self):
        if get_time_diff(self.lastFrame) > 0.05:
            if isInputHeld[1]:
                self.index += 1
                if self.index > 4:
                    self.index = 0
            else:  # Idle animation
                self.index = 0

            self.lastFrame = time.time()

    def __str__(self):
        return (f'Player at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\ncurrent bullet: {self.bulletType}\n'
                f'xp: {self.xp}\nlevel: {self.level}\n')

    def __repr__(self):
        return f'Player({self.pos}, {self.vel}, {self.accel}, {self.bulletType}, {self.xp}, {self.level})'


# ============================================================================ #
#                                  Room Class                                  #
# ============================================================================ #
# noinspection PyTypeChecker
class Room(AbstractBase):
    def __init__(self, room_x: float, room_y: float):
        """The room where all the current action is taking place

        Args:
            room_x: The room's x-axis location in the grid of the room layout
            room_y: The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        all_rooms.append(self)
        self.room = vec((room_x, room_y))
        self.size = vec((1280, 720))

        # self.roomOffset = vec(0, 0)

        self.lastEntranceDir = None
        self.isChangingRooms = False

        self.player1: Player = Player()
        self.posCopy = self.player1.pos.copy()
        self.offset = vec(self.player1.pos.x - 608, self.player1.pos.y - WINHEIGHT // 2)

        self.borderSouth = RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.borderEast = RoomBorder(WINWIDTH // 16, 0, 1, self.size.y // 16)
        self.borderNorth = RoomBorder(0, -1, self.size.x // 16, 1)
        self.borderWest = RoomBorder(-1, 0, 1, self.size.y // 16)

        self.isScrollingX = True
        self.isScrollingY = True

        self.canSwitchX = True
        self.canSwitchY = True

        self.centeringX = False
        self.centeringY = False
        self.lastRecenterX = time.time()
        self.lastRecenterY = time.time()
        self.offsetX = self.player1.pos.x - WINWIDTH // 2
        self.offsetY = self.player1.pos.y - WINHEIGHT // 2

        # --------------------------------- Movement --------------------------------- #
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cAccel = self.player1.cAccel

        self.layout_update()

    # ------------------------------- Room Movement ------------------------------ #
    def accel_movement(self) -> None:
        """Calculates the room's acceleration, velocity, and position
        """
        self.accel.x += self.vel.x * FRIC
        self.accel.y += self.vel.y * FRIC
        self.vel += self.accel
        self.pos = vec(self.borderWest.pos.x + self.borderWest.hitbox.width // 2,
                       self.borderNorth.pos.y + self.borderNorth.height // 2)

    def get_accel(self) -> pygame.math.Vector2:
        final_accel = vec(0, 0)
        if self.isScrollingX:
            final_accel.x += self.__get_x_axis_output()

        if self.isScrollingY:
            final_accel.y += self.__get_y_axis_output()

        return final_accel

    def __get_x_axis_output(self) -> float:
        """Determines the amount of acceleration the room's x-axis component should have
        
        ### Returns
            - ``float``: The room's acceleration's x-axis component
        """
        output: float = 0.0
        if isInputHeld[K_a]:
            output += self.player1.cAccel
        if isInputHeld[K_d]:
            output -= self.player1.cAccel

        if self.player1.is_swinging():
            angle = get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * sin(rad(angle))

        return output

    def __get_y_axis_output(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have
        
        ### Returns
            - ``float``: The room's acceleration's y-axis component
        """
        output: float = 0.0
        if isInputHeld[K_w]:
            output += self.player1.cAccel
        if isInputHeld[K_s]:
            output -= self.player1.cAccel

        if self.player1.is_swinging():
            angle = get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * cos(rad(angle))

        return output

    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player.
        """
        if self.canUpdate:
            self.accel = self.get_accel()
            self.accel_movement()

            if not (not self.isScrollingX and not self.isScrollingY):
                self.__sprite_collide_check(self.player1, all_walls)

            if self.isScrollingX and self.isScrollingY:
                for sprite in all_movable:
                    self.__sprite_collide_check(sprite, all_walls)

            # Teleports the player
            for portal in all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portal_in: Portal = portal
                    portal_out: Portal = get_other_portal(portal_in)

                    if len(all_portals) == 2:
                        self.__teleport_player(portal_in, portal_out)

            self.__recenter_player_x()
            self.__recenter_player_y()

            for sprite in self.__get_sprites_to_recenter():
                sprite.movement()

    def __recenter_player_x(self) -> None:
        """Moves all the objects in the room so that the player is centered along the x-axis.
        """
        if self.isScrollingX:
            if not self.centeringX:
                if self.player1.pos.x != WINWIDTH // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetX = self.posCopy.x - WINWIDTH // 2
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterX = time.time()
                    self.centeringX = True

            if self.centeringX:
                weight = get_time_diff(self.lastRecenterX)
                if weight <= 0.25:
                    self.player1.pos.x = cerp(self.posCopy.x, WINWIDTH // 2, weight * 4)
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.pos.x = cerp(sprite.posCopy.x, sprite.posCopy.x - self.offsetX, weight * 4)
                else:
                    self.player1.pos.x = WINWIDTH // 2
                    self.centeringX = False

    def __recenter_player_y(self) -> None:
        """Moves all the objects in the room so that the player is centered along the y-axis.
        """
        if self.isScrollingY:
            if not self.centeringY:
                if self.player1.pos.y != WINHEIGHT // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetY = self.posCopy.y - WINHEIGHT // 2
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterY = time.time()
                    self.centeringY = True

            if self.centeringY:
                weight = get_time_diff(self.lastRecenterY)
                if weight <= 0.25:
                    self.player1.pos.y = cerp(self.posCopy.y, WINHEIGHT // 2, weight * 4)
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.pos.y = cerp(sprite.posCopy.y, sprite.posCopy.y - self.offsetY, weight * 4)
                else:
                    self.player1.pos.y = WINHEIGHT // 2
                    self.centeringY = False

    def __get_sprites_to_recenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is centered.

        Returns:
            list: A list containing all sprites that should be relocated when the player is centered
        """
        output_list = []
        for sprite in self.sprites():
            output_list.append(sprite)

        for container in all_containers:
            if container.room == self.room:
                for sprite in container:
                    output_list.append(sprite)

        return output_list

    # -------------------------------- Teleporting ------------------------------- #
    def __align_player_after_tp(self, offset: float, direction: str, portal_out: Portal, width, height) -> None:
        """Sets the player at the proper position after teleporting when the room can scroll.

        Args:
            offset: The distance the player is (on either x or y-axis, not both) from the center of the entering portal
            direction: The direction the exit portal is facing
            portal_out: The exit portal sprite
            width: Half the sum of the player's hitbox width plus the portal's hitbox width
            height: Half the sum of the player's hitbox height plus the portal's hitbox height
        """
        if direction == SOUTH:
            self.player1.pos.x = portal_out.pos.x - offset
            self.player1.pos.y = portal_out.pos.y + height

        elif direction == EAST:
            self.player1.pos.x = portal_out.pos.x + width
            self.player1.pos.y = portal_out.pos.y - offset

        elif direction == NORTH:
            self.player1.pos.x = portal_out.pos.x + offset
            self.player1.pos.y = portal_out.pos.y - height

        elif direction == WEST:
            self.player1.pos.x = portal_out.pos.x - width
            self.player1.pos.y = portal_out.pos.y + offset

    def __teleport_player(self, portal_in: Portal, portal_out: Portal) -> None:
        """Teleports the player when the room is scrolling.

        Args:
            portal_in: The portal the player is entering
            portal_out: The portal the player is exiting
        """
        combined_width = (portal_out.hitbox.width + self.player1.hitbox.width) // 2
        combined_height = (portal_out.hitbox.height + self.player1.hitbox.height) // 2
        direction_in = portal_in.facing
        direction_out = portal_out.facing
        direction_angles = {SOUTH: 180, EAST: 90, NORTH: 0, WEST: 270}

        # Calculating where player should exit portal relative to the position entered
        distance_offset = 0.0
        if direction_in in [SOUTH, NORTH]:
            distance_offset = self.player1.pos.x - portal_in.pos.x
        elif direction_in in [EAST, WEST]:
            distance_offset = self.player1.pos.y - portal_in.pos.y

        # Setting the player's position (actually teleporting the player)
        self.__align_player_after_tp(distance_offset, direction_out, portal_out, combined_width, combined_height)

        # Scrolling x and y
        if self.isScrollingX and self.isScrollingY:
            if direction_in == EAST:
                direction_angles.update({EAST: 180, NORTH: 90, WEST: 0, SOUTH: 270})
            elif direction_in == NORTH:
                direction_angles.update({NORTH: 180, WEST: 90, SOUTH: 0, EAST: 270})
            elif direction_in == WEST:
                direction_angles.update({WEST: 180, SOUTH: 90, EAST: 0, NORTH: 270})
            self.__sprites_rotate_trajectory(direction_angles[direction_out])

        # Scrolling x, not scrolling y
        elif self.isScrollingX and not self.isScrollingY:
            if direction_in == SOUTH:
                direction_angles.update({SOUTH: 180, EAST: 270, NORTH: 0, WEST: 90})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [EAST, WEST]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == EAST:
                direction_angles.update({SOUTH: 90, EAST: 180, NORTH: 270, WEST: 0})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [SOUTH, NORTH]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

            if direction_in == NORTH:
                direction_angles.update({SOUTH: 0, EAST: 90, NORTH: 180, WEST: 270})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [EAST, WEST]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == WEST:
                direction_angles.update({SOUTH: 270, EAST: 0, NORTH: 90, WEST: 180})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [SOUTH, NORTH]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

        # Scrolling y, not scrolling x
        elif not self.isScrollingX and self.isScrollingY:
            if direction_in == SOUTH:
                direction_angles.update({SOUTH: 180, EAST: 270, NORTH: 0, WEST: 90})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [EAST, WEST]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == EAST:
                direction_angles.update({SOUTH: 90, EAST: 180, NORTH: 270, WEST: 0})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [SOUTH, NORTH]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

            if direction_in == NORTH:
                direction_angles.update({SOUTH: 0, EAST: 90, NORTH: 180, WEST: 270})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [EAST, WEST]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == WEST:
                direction_angles.update({SOUTH: 270, EAST: 0, NORTH: 90, WEST: 180})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [SOUTH, NORTH]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

    def __sprites_rotate_trajectory(self, angle: float) -> None:
        """Rotates the velocities and accelerations of all the sprites within the room's sprites
        
        ### Arguments
            - angle (``float``): The angle to rotate the vectors by

        """
        self.accel = self.accel.rotate(angle)
        self.vel = self.vel.rotate(angle)

        for sprite in self.__get_sprites_to_recenter():
            sprite.accel = sprite.accel.rotate(angle)
            sprite.vel = sprite.vel.rotate(angle)

    def __translate_trajectory(self, is_player_to_room: bool, angle: float) -> None:
        """Translates the velocity of the room's sprites to the player, or vice versa.

        Args:
            is_player_to_room: Should velocity be swapped from player to room (True), or from room to player (False)?
            angle: The angle to rotate the trajectory by
        """
        if is_player_to_room:
            for sprite in self.__get_sprites_to_recenter():
                sprite.vel = self.player1.vel.rotate(angle)

        elif not is_player_to_room:
            self.player1.vel = self.vel.rotate(angle)

    # ----------------------------- Sprite Collisions ---------------------------- #
    # noinspection SpellCheckingInspection
    def __sprite_collide_check(self, instig, *contact_list) -> None:
        """Collide check for when the room is scrolling
        
        ### Arguments
            - instig (``ActorBase``): The sprite instigating the collision
            - contactList (``AbstractBase``): The sprite group(s) to check for a collision with
        """
        for group in contact_list:
            for sprite in group:
                if sprite.visible and isinstance(instig, Player):
                    self.__player_block_from_side(instig, sprite)
                elif sprite.visible:
                    self.__sprite_block_from_side(instig, sprite)

    def __player_block_from_side(self, instig, sprite):
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if triangle_collide(instig, sprite) == SOUTH and (
                    instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self.accel.y = 0
                self.vel.y = 0
                # if not self.isScrollingX and self.isScrollingY:
                instig.pos.y = sprite.pos.y + height

            if triangle_collide(instig, sprite) == EAST and (
                    instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self.accel.x = 0
                self.vel.x = 0
                # if self.isScrollingX and not self.isScrollingY:
                instig.pos.x = sprite.pos.x + width

            if triangle_collide(instig, sprite) == NORTH and (
                    instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self.accel.y = 0
                self.vel.y = 0
                # if not self.isScrollingX and self.isScrollingY:
                instig.pos.y = sprite.pos.y - height

            if triangle_collide(instig, sprite) == WEST and (
                    instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self.accel.x = 0
                self.vel.x = 0
                # if self.isScrollingX and not self.isScrollingY:
                instig.pos.x = sprite.pos.x - width

    @staticmethod
    def __sprite_block_from_side(instig, sprite) -> None:
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if (triangle_collide(instig, sprite) == SOUTH and
                    instig.pos.y <= sprite.pos.y + height and (
                    instig.vel.y < 0 or sprite.vel.y > 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if (triangle_collide(instig, sprite) == EAST and
                    instig.pos.x <= sprite.pos.x + width and (
                    instig.vel.x < 0 or sprite.vel.x > 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if (triangle_collide(instig, sprite) == NORTH and
                    instig.pos.y >= sprite.pos.y - height and (
                    instig.vel.y > 0 or sprite.vel.y < 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if (triangle_collide(instig, sprite) == WEST and
                    instig.pos.x >= sprite.pos.x - width and (
                    instig.vel.x > 0 or sprite.vel.x < 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    # -------------------------------- Room Layout ------------------------------- # 
    def __set_room_borders(self, room_width: int, room_height: int) -> None:
        """Sets the borders of the room.

        Args:
            room_width: The width of the room (in pixels)
            room_height: The height of the room (in pixels)
        """
        self.borderSouth = RoomBorder(0, room_height // 16, room_width // 16, 1)
        self.borderEast = RoomBorder(room_width // 16, 0, 1, room_height // 16)
        self.borderNorth = RoomBorder(0, -1, room_width // 16, 1)
        self.borderWest = RoomBorder(-1, 0, 1, room_height // 16)

        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

    def __init_room(self, room_size_x: int, room_size_y: int, can_scroll_x: bool, can_scroll_y: bool) -> None:
        """Initializes a room's properties. This function must be called once for every `self.room` iteration.
        
        ### Arguments
            - roomSizeX (``int``): The width of the room (in pixels).
            - roomSizeY (``int``): The height of the room (in pixels).
            - canScrollX (``bool``): Should the room scroll with the player along the x-axis?
            - canScrollY (``bool``): Should the room scroll with the player along the y-axis?
        """
        player_vel_copy = self.player1.vel.copy()
        self.size = vec((room_size_x, room_size_y))

        scroll_copy_x = copy.copy(self.isScrollingX)
        scroll_copy_y = copy.copy(self.isScrollingY)

        self.isScrollingX = can_scroll_x
        self.isScrollingY = can_scroll_y

        self.__set_room_borders(room_size_x, room_size_y)

        if self.lastEntranceDir == SOUTH:
            self.player1.pos.x = self.borderNorth.pos.x
            self.player1.pos.y = (self.borderNorth.pos.y + self.borderNorth.hitbox.height // 2
                                  + self.player1.hitbox.height // 2)
            self.__get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                              player_vel_copy)

        elif self.lastEntranceDir == EAST:
            self.player1.pos.x = (self.borderWest.pos.x +
                                  self.borderWest.hitbox.width // 2 + self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderWest.pos.y
            self.__get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                              player_vel_copy)

        elif self.lastEntranceDir == NORTH:
            self.player1.pos.x = self.borderSouth.pos.x
            self.player1.pos.y = (self.borderSouth.pos.y -
                                  self.borderSouth.hitbox.height // 2 - self.player1.hitbox.height // 2)
            self.__get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                              player_vel_copy)

        elif self.lastEntranceDir == WEST:
            self.player1.pos.x = (self.borderEast.pos.x -
                                  self.borderEast.hitbox.width // 2 - self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderEast.pos.y
            self.__get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                              player_vel_copy)

        else:
            print('no value')

        self.player1.vel = vec(0, 0)

    def __get_room_change_trajectory(self, prev_room_scroll_x: bool, prev_room_scroll_y: bool, new_room_scroll_x: bool,
                                     new_room_scroll_y: bool, player_vel: pygame.math.Vector2) -> None:
        """Transfers the velocity from the room to the player or vice versa when changing rooms.

        Args:
            prev_room_scroll_x: Did the previous room scroll along the x-axis?
            prev_room_scroll_y: Did the previous room scroll along the y-axis?
            new_room_scroll_x: Does the new room scroll along the x-axis?
            new_room_scroll_y: Does the new room scroll along the y-axis?
            player_vel: The player's velocity
        """
        if prev_room_scroll_x:
            if not new_room_scroll_x:
                self.player1.vel.x = -self.vel.x

        elif not prev_room_scroll_x:
            if new_room_scroll_x:
                self.vel.x = -player_vel.x

        if prev_room_scroll_y:
            if not new_room_scroll_y:
                self.player1.vel.y = -self.vel.y

        elif not prev_room_scroll_y:
            if new_room_scroll_y:
                self.vel.y = -player_vel.y

    def layout_update(self) -> None:
        """Updates the layout of the room
        """
        for sprite in self.sprites():
            sprite.kill()

        container: RoomContainer
        for container in all_containers:
            container.hide_sprites()

        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            self.__init_room(WINWIDTH, WINHEIGHT, True, False)

            self.add(
                Wall(0, 0, 8, 8),
                Wall(0, 37, 8, 8),
                Wall(72, 0, 8, 8),
                Wall(72, 37, 8, 8),
                Button(1, 14, 38),
            )

            try:
                container: RoomContainer = next(c for c in all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        Box(0, WINWIDTH // 2, WINHEIGHT // 2),
                        StandardGrunt(200, 200)
                    )
                )

        if self.room == vec(0, 1):
            self.__init_room(WINWIDTH, WINHEIGHT, False, True)
            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 20, 8, 8)
            )

            try:
                container: RoomContainer = next(c for c in all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

        if self.room == vec(-1, 0):
            self.__init_room(WINWIDTH, WINHEIGHT, False, False)

            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 8, 8, 8)
            )

            try:
                container: RoomContainer = next(c for c in all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

        if self.room == vec(1, 0):
            self.__init_room(WINWIDTH, WINHEIGHT, False, False)

            self.add(
                Wall(8, 0, 4, 4),
                Wall(40, 8, 8, 8)
            )

            try:
                container: RoomContainer = next(c for c in all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        # Box(1, 300, 400)
                    )
                )

    def update(self):
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'


class RoomContainer(AbstractBase):
    def __init__(self, room_x: int | float, room_y: int | float, *sprites):
        """A container for sprites within a room. Contains data about all enemies in a room.

        Args:
            room_x: The container's x-location in the room grid
            room_y: The container's y-location in the room grid
            *sprites: The sprite(s) that should be added to the container
        """
        super().__init__()
        self.room = vec((room_x, room_y))

        for sprite in sprites:
            self.add(sprite)

    def hide_sprites(self):
        """Hides all the sprites in the container
        """
        for sprite in self.sprites():
            sprite.hide()

    def show_sprites(self):
        for sprite in self.sprites():
            sprite.show(LAYER['enemy'])
            sprite.accel = vec(0, 0)
            sprite.vel = vec(0, 0)
            sprite.pos = sprite.roomPos


# ============================================================================ #
#                                 Menu Classes                                 #
# ============================================================================ #
class InventoryMenu(AbstractBase):
    def __init__(self, owner: Player):
        """A menu used to view collected items and utilize them for various purposes
        
        ### Arguments
            - owner ``(pygame.sprite.Sprite)``: The player whom the inventory belongs to
        """
        super().__init__()
        self.cyclingLeft = False
        self.cyclingRight = False

        self.owner = owner

        self.wipeTime = 1
        self.window = 0

        self.lastCycle = time.time()

        self.rightArrow = RightMenuArrow(WINWIDTH - 64, WINHEIGHT / 2)
        self.leftArrow = LeftMenuArrow(64, WINHEIGHT / 2)

        self.add(
            self.build_menu_slots()
        )

    def hide(self):
        """Makes all the elements of the inventory menu invisible (closes the inventory menu)
        """
        for sprite in self.sprites():
            all_sprites.remove(sprite)

    def show(self):
        """Makes all the elements of the inventory menu visible
        """
        for sprite in self.sprites():
            all_sprites.add(sprite, layer=LAYER['ui_1'])

    def cycle_menu(self):
        if (not self.cyclingLeft and
                not self.cyclingRight and
                not self.canUpdate):
            if isInputHeld[1] and self.leftArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window -= 1
                self.lastCycle = time.time()
                self.cyclingLeft = True

            if isInputHeld[1] and self.rightArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window += 1
                self.lastCycle = time.time()
                self.cyclingRight = True

        # Cycling left
        if self.cyclingLeft and not self.cyclingRight:
            weight = get_time_diff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = cerp(sprite.start_pos.x, sprite.start_pos.x - WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cyclingLeft = False

        # Cycling right
        if not self.cyclingLeft and self.cyclingRight:
            weight = get_time_diff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = cerp(sprite.start_pos.x, sprite.start_pos.x + WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cyclingRight = False

    def build_menu_slots(self) -> list:
        """Creates and aligns the inventory slots of the menu.

        Returns:
            list: A list containing the menu slots created
        """
        space = vec(0, 0)
        space_cushion = vec(82, 82)
        menu_slots = []
        slot_count = 0
        offset = 0
        for y in range(5):
            for x in range(5):
                menu_slots.append(MenuSlot(self.owner, 64 + space.x, 64 + space.y, None))
                space.x += space_cushion.x
                offset += 1
                slot_count += 1
            space.y += space_cushion.y
            space.x = 0
        return menu_slots

    def update_menu_slots(self):
        for material in self.owner.inventory:
            if self.owner.inventory[material] > 0:  # Every material in the owner's inventory
                for slot in self.sprites():
                    if slot.holding == material:
                        break
                    if slot.holding is None:
                        slot.holding = material
                        break
            for slot in self.sprites():
                slot.create_slot_images()

    def update(self):
        if keyReleased[K_e] % 2 != 0 and keyReleased[K_e] > 0:
            self.show()
            self.rightArrow.show(LAYER['ui_1'])
            self.leftArrow.show(LAYER['ui_1'])

            self.canUpdate = False
            for sprite in all_sprites:
                sprite.canUpdate = False

        elif keyReleased[K_e] % 2 == 0 and keyReleased[K_e] > 0:
            self.hide()
            self.rightArrow.hide()
            self.leftArrow.hide()

            self.canUpdate = True
            for sprite in all_sprites:
                sprite.canUpdate = True

        self.cycle_menu()


class RightMenuArrow(ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the right.
        
        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.image = pygame.transform.scale(self.images[self.index], (64, 64))

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x - 32, pos_y - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it.
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        if anim_timer % 1 == 0:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            self.index += 1

        self.hover()


class LeftMenuArrow(ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the left.
        
        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x - 32, pos_y - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        if anim_timer % 1 == 0:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)
            self.index += 1

        self.hover()


class MenuSlot(ActorBase):
    def __init__(self, owner: Player, pos_x: float, pos_y: float, item_held: str | None):
        """A menu slot that shows the collected amount of a specific item.

        Args:
            owner: The owner of the inventory to whom the menu slot belongs to
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
            item_held: The item the menu slot will hold. Items are chosen from MATERIALS dictionary.
        """
        super().__init__()
        all_slots.add(self)
        self.owner = owner

        self.pos = vec((pos_x, pos_y))
        self.startPos = vec((pos_x, pos_y))
        self.holding = item_held
        self.count = 0

        self.menuSheet = Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.itemSheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.menuImages = self.menuSheet.get_images(64, 64, 1)

        self.index = 0

        self.menuImg = self.menuImages[0]

        self.images = self.create_slot_images()
        self.image: pygame.Surface = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.center_rects()

    def hover(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            s_time = time.time()
            scale = abs(sin(s_time)) / 2
            self.image = pygame.transform.scale_by(self.images[self.index], 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_item_images(self) -> list:
        if self.holding == MAT[0]:
            return self.itemSheet.get_images(32, 32, 1, 0)
        elif self.holding == MAT[1]:
            return self.itemSheet.get_images(32, 32, 1, 1)
        else:
            return self.itemSheet.get_images(32, 32, 1, 0)

    def create_slot_images(self):
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that
        item on top.

        Returns:
            list: A list of the created images
        """
        item_images = self.get_item_images()
        final_images = []
        if self.holding is not None:
            for frame in item_images:
                new_img = combine_images(self.menuImg, frame)

                # Adding the count of the item to its images
                count_surface = text_to_image(str(self.count), 'sprites/ui/font.png', 9, 14, 36)
                new_img.set_colorkey((0, 0, 0))
                center_x = (new_img.get_width() - frame.get_width()) // 2
                center_y = (new_img.get_height() - frame.get_height()) // 2
                new_img.blit(
                    swap_color(swap_color(count_surface, (44, 44, 44), (156, 156, 156)), (0, 0, 1), (255, 255, 255)),
                    vec(center_x, center_y))
                final_images.append(new_img)

        else:
            final_images.append(self.menuImg)

        return final_images

    def update(self):
        self.center_rects()

        if self.holding is not None:
            self.count = self.owner.inventory[self.holding]

        self.images = self.create_slot_images()
        self.hover()


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
def redraw_game_window():
    """Draws all sprites every frame.
    """
    main_room.update()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
# Load room
main_room = Room(0, 0)


def check_key_release(is_mouse, *inputs) -> None:
    """Checks if any input(s) has been released. If one has, then its count in keyReleased will be updated to match.

    Args:
        is_mouse: Are the inputs mouse buttons?
        *inputs: The input(s) to check
    """
    if not is_mouse:
        for key in inputs:
            if event.type == pygame.KEYUP and event.key == key:
                if key in isInputHeld and key in keyReleased:
                    keyReleased[key] += 1
    else:
        for button in inputs:
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                if button in isInputHeld and button in keyReleased:
                    keyReleased[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
running = True
while running:
    anim_timer += 1

    for a_player in all_players:
        if a_player.hp <= 0:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()

        if event.type == QUIT or keyPressed[K_ESCAPE]:
            sys.exit()

        isInputHeld = {
            1: pygame.mouse.get_pressed(5)[0],
            2: pygame.mouse.get_pressed(5)[1],
            3: pygame.mouse.get_pressed(5)[2],

            K_a: keyPressed[K_a],
            K_w: keyPressed[K_w],
            K_s: keyPressed[K_s],
            K_d: keyPressed[K_d],
            K_x: keyPressed[K_x],
            K_e: keyPressed[K_e]
        }

        check_key_release(False, K_e, K_x)
        check_key_release(True, 1, 2, 3)

        if event.type == pygame.MOUSEWHEEL:
            # Player ammo refill
            if main_room.player1.ammo < main_room.player1.maxAmmo:
                main_room.player1.ammo += 1

    screen.fill((255, 255, 255))

    # ------------------------------ Game Operation ------------------------------ #
    # Regenerate health for testing purposes
    for a_player in all_players:
        # noinspection PyUnboundLocalVariable
        if anim_timer % 5 == 0 and a_player.hp < a_player.maxHp and isInputHeld[K_x]:
            a_player.hp += 1

    for portals in all_portals:
        pygame.draw.rect(screen, RED, portals.hitbox, 3)

    # ------------------------------- Redraw Window ------------------------------ #
    redraw_game_window()
    clock.tick_busy_loop(FPS)
