import sys
import copy
import time
import math

import pygame
from pygame.locals import *

import calculations as calc
import constants as cst
import groups
import classbases as cb
import menu_ui as menu

import bullets
import controls as ctrl
import enemies
import statbars
import screen
import tiles
import trinkets

pygame.init()

clock = pygame.time.Clock()

screen.buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
screen.viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED, 0, 0, 2)
pygame.display.set_caption('Orbeeto')

# Aliases
vec = pygame.math.Vector2
rad = math.radians


class Player(cb.ActorBase):
    def __init__(self):
        """A player sprite that can move and shoot.
        """
        super().__init__()
        groups.all_players.add(self)
        self.show(cst.LAYER['player'])

        self.room = cb.get_room()

        self.set_images("sprites/orbeeto/orbeeto.png", 64, 64, 5, 5)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self.pos = vec((cst.WINWIDTH // 2, cst.WINHEIGHT // 2))
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

        self.lastRegen = time.time()            # Used for timing passive regeneration

        self.maxAmmo: int = 40
        self.ammo: int = self.maxAmmo
        self.bulletVel: float = 12.0
        self.gunCooldown: float = 0.12
        self.lastShot: float = time.time()

        self.grappleSpeed: float = 2.0

        self.dodgeTimeCharge = 1200
        self.dodgeTime = 0
        self.lastHit = time.time()

        self.update_level()

        # --------------------------------- Stat Bars -------------------------------- #
        self.healthBar = statbars.HealthBar(self)
        self.dodgeBar = statbars.DodgeBar(self)
        self.ammoBar = statbars.AmmoBar(self)

        self.menu = menu.InventoryMenu(self)

        self.inventory = {}
        for item in cst.MAT.values():
            self.inventory.update({item: 0})

        # ---------------------- Bullets, Portals, and Grapples ---------------------- #
        self.bulletType = cst.PROJ_LASER
        self.canPortal = False
        self.canGrapple = True
        self.grapple = None

    # ----------------------------------- Stats ---------------------------------- #

    def update_max_stats(self):
        """Updates all the player's max stats.
        """
        self.maxHp = math.floor(calc.eerp(50, 650, self.level / self.maxLevel))
        self.maxAtk = math.floor(calc.eerp(10, 1250, self.level / self.maxLevel))
        self.maxDef = math.floor(calc.eerp(15, 800, self.level / self.maxLevel))
        self.maxAmmo = math.floor(calc.eerp(40, 1200, self.level / self.maxLevel))

        self.grappleSpeed = math.floor(calc.eerp(2.0, 4.0, self.level / self.maxLevel))

        self.atk = self.maxAtk
        self.defense = self.maxDef

    def update_level(self):
        if self.xp > 582803:
            self.xp = 582803

        self.level = math.floor((256 * self.xp) / (self.xp + 16384))
        self.update_max_stats()

    def __passive_hp_regen(self) -> None:
        """Regenerates the player's HP after not being attacked for a period of time.
        """
        time_hit = calc.get_time_diff(self.lastHit)
        regens_per_sec = 0
        if time_hit < 5:
            regens_per_sec = 0
        elif time_hit >= 5:
            regens_per_sec = math.ceil(0.12 * math.log(time_hit - 4, math.e))

        if regens_per_sec == 0:
            pass
        elif calc.get_time_diff(self.lastRegen) >= 1 / regens_per_sec:
            if self.hp < self.maxHp:
                self.hp += 1
            self.lastRegen = time.time()

    # --------------------------------- Movement --------------------------------- #
    def movement(self):
        """When called once every frame, it allows the player to receive input from the user and move accordingly
        """
        if self.canUpdate and self.visible:
            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        """Returns the acceleration that the player should undergo given specific conditions.

        Returns:
            pygame.math.Vector2: The acceleration value of the player
        """
        final_accel = vec(0, 0)
        if not self.room.isScrollingX:
            final_accel.x += self.__get_x_axis_output()

        if not self.room.isScrollingY:
            final_accel.y += self.__get_y_axis_output()

        return final_accel

    def __get_x_axis_output(self) -> float:
        output = 0.0
        if ctrl.is_input_held[K_a]:
            output -= self.cAccel
        if ctrl.is_input_held[K_d]:
            output += self.cAccel

        if self.is_swinging():
            angle = calc.get_angle_to_sprite(self, self.grapple)
            output += self.grappleSpeed * -math.sin(rad(angle))

        return output

    def __get_y_axis_output(self) -> float:
        output = 0.0
        if ctrl.is_input_held[K_w]:
            output -= self.cAccel
        if ctrl.is_input_held[K_s]:
            output += self.cAccel

        if self.is_swinging():
            angle = calc.get_angle_to_sprite(self, self.grapple)
            output += self.grappleSpeed * -math.cos(rad(angle))

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
        elif self.grapple.grappledTo not in groups.all_walls:
            return output
        else:
            output = True
            return output

    def shoot(self):
        """Shoots bullets.
        """
        angle = rad(calc.get_angle_to_mouse(self))
        vel_x = self.bulletVel * -math.sin(angle)
        vel_y = self.bulletVel * -math.cos(angle)

        offset = vec((21, 30))

        if (ctrl.is_input_held[1] and
                self.ammo > 0 and
                calc.get_time_diff(self.lastShot) >= self.gunCooldown):
            # Standard bullets
            if self.bulletType == cst.PROJ_STD:
                groups.all_projs.add(
                    bullets.PlayerStdBullet(self,
                                            self.pos.x - (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                            self.pos.y + (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                            vel_x, vel_y, 1
                                            ),

                    bullets.PlayerStdBullet(self,
                                            self.pos.x + (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                            self.pos.y - (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                            vel_x, vel_y, 1
                                            )
                )

            # Laser bullets
            elif self.bulletType == cst.PROJ_LASER:
                groups.all_projs.add(
                    bullets.PlayerLaserBullet(self,
                                              self.pos.x - (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                              self.pos.y + (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                              vel_x * 2, vel_y * 2, 1
                                              ),

                    bullets.PlayerLaserBullet(self,
                                              self.pos.x + (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                              self.pos.y - (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                              vel_x * 2, vel_y * 2, 1
                                              )
                )

            self.ammo -= 1
            self.lastShot = time.time()

        # ------------------------------ Firing Portals ------------------------------ #
        if ctrl.key_released[3] % 2 == 0 and self.canPortal and self.canGrapple:
            groups.all_projs.add(bullets.PortalBullet(self, self.pos.x, self.pos.y, vel_x * 0.75, vel_y * 0.75))
            self.canPortal = False

        elif ctrl.key_released[3] % 2 != 0 and not self.canPortal and self.canGrapple:
            groups.all_projs.add(bullets.PortalBullet(self, self.pos.x, self.pos.y, vel_x * 0.75, vel_y * 0.75))
            self.canPortal = True

        # --------------------------- Firing Grappling Hook -------------------------- #
        if ctrl.key_released[2] % 2 != 0 and self.canGrapple:
            if self.grapple is not None:
                self.grapple.shatter()
            self.grapple = bullets.GrappleBullet(self, self.pos.x, self.pos.y, vel_x, vel_y)
            self.canGrapple = False

        if ctrl.key_released[2] % 2 == 0 and not self.canGrapple:
            self.grapple.returning = True
            self.canGrapple = True

    def __check_for_dash(self) -> None:
        pass

    def update(self):
        if self.canUpdate and self.visible:
            self.movement()
            self.shoot()

            # Animation
            self.__animate()
            self.rotate_image(calc.get_angle_to_mouse(self))

            # Dodge charge up
            if self.dodgeTime < self.dodgeTimeCharge:
                self.dodgeTime += 1

        self.menu.update()
        self.__passive_hp_regen()

        if self.hp <= 0:
            self.kill()

    def __animate(self):
        if calc.get_time_diff(self.lastFrame) > 0.05:
            if ctrl.is_input_held[1]:
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
class Room(cb.AbstractBase):
    def __init__(self, room_x: float, room_y: float):
        """The room where all the current action is taking place

        Args:
            room_x: The room's x-axis location in the grid of the room layout
            room_y: The room's y-axis location in the grid of the room layout
        """
        super().__init__()
        groups.all_rooms.append(self)
        self.room = vec((room_x, room_y))
        self.size = vec((1280, 720))

        self.lastEntranceDir = None

        self.player1: Player = Player()
        self.posCopy = self.player1.pos.copy()
        self.offset = vec(self.player1.pos.x - 608, self.player1.pos.y - cst.WINHEIGHT // 2)

        self.borderSouth = tiles.RoomBorder(0, self.size.y // 16, self.size.x // 16, 1)
        self.borderEast = tiles.RoomBorder(cst.WINWIDTH // 16, 0, 1, self.size.y // 16)
        self.borderNorth = tiles.RoomBorder(0, -1, self.size.x // 16, 1)
        self.borderWest = tiles.RoomBorder(-1, 0, 1, self.size.y // 16)
        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

        self.isScrollingX = True
        self.isScrollingY = True

        self.canSwitchX = True
        self.canSwitchY = True

        self.centeringX = False
        self.centeringY = False
        self.lastRecenterX = time.time()
        self.lastRecenterY = time.time()
        self.offsetX = self.player1.pos.x - cst.WINWIDTH // 2
        self.offsetY = self.player1.pos.y - cst.WINHEIGHT // 2

        # --------------------------------- Movement --------------------------------- #
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cAccel = self.player1.cAccel

        self.dashCooldown = time.time()
        self.dashTimer = time.time()
        self.dashCheck = True
        self.lastPresses = copy.copy(ctrl.key_released)

        self.layout_update()

    # ------------------------------- Room Movement ------------------------------ #
    def accel_movement(self) -> None:
        """Calculates the room's acceleration, velocity, and position
        """
        self.accel.x += self.vel.x * cst.FRIC
        self.accel.y += self.vel.y * cst.FRIC
        self.vel += self.accel
        self.pos = vec(self.borderWest.pos.x + self.borderWest.hitbox.width // 2,
                       self.borderNorth.pos.y + self.borderNorth.height // 2)

    def get_accel(self) -> vec:
        final_accel = vec(0, 0)
        if self.isScrollingX:
            final_accel.x += self.__get_x_axis_output()
        if self.isScrollingY:
            final_accel.y += self.__get_y_axis_output()

        return final_accel

    def __get_x_axis_output(self) -> float:
        """Determines the amount of acceleration the room's x-axis component should have

        Returns:
            float: The room's acceleration's x-axis component
        """
        output: float = 0.0
        if ctrl.is_input_held[K_a]:
            output += self.player1.cAccel
        if ctrl.is_input_held[K_d]:
            output -= self.player1.cAccel

        if self.player1.is_swinging():
            angle = calc.get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * math.sin(rad(angle))

        return output

    def __get_y_axis_output(self) -> float:
        """Determines the amount of acceleration the room's y-axis component should have

        Returns:
            float: The room's acceleration's y-axis component
        """
        output: float = 0.0
        if ctrl.is_input_held[K_w]:
            output += self.player1.cAccel
        if ctrl.is_input_held[K_s]:
            output -= self.player1.cAccel

        if self.player1.is_swinging():
            angle = calc.get_angle_to_sprite(self.player1, self.player1.grapple)
            output += self.player1.grappleSpeed * math.cos(rad(angle))

        return output

    def __check_for_dash(self) -> None:
        """Checks if the player should perform a dash. If all criteria are met, then a dash will be executed.

        Returns:
            None
        """
        if calc.get_time_diff(self.dashCooldown) >= 1:
            global dash_key
            movement_keys = [K_w, K_a, K_s, K_d]

            for a_key in movement_keys:  # Initiating the dash
                if ctrl.key_released[a_key] == self.lastPresses[a_key] + 1 and self.dashCheck:
                    dash_key = a_key
                    print(f'{dash_key} initiated a double-tap.')
                    self.dashTimer = time.time()
                    self.lastPresses = copy.copy(ctrl.key_released)
                    self.dashCheck = False

            if calc.get_time_diff(self.dashTimer) <= 0.4 and not self.dashCheck:
                if ctrl.is_input_held[dash_key]:
                    self.__dash(dash_key)
                    self.dashCheck = True
                    self.dashCooldown = time.time()

            if calc.get_time_diff(self.dashTimer) > 0.4 and not self.dashCheck:
                self.dashCheck = True
        else:
            self.lastPresses = copy.copy(ctrl.key_released)

    def __dash(self, key: int) -> None:
        """Dashes the player in a cardinal direction.

        Args:
            key: The key being used to dash, i.e. [w], [a], [s], or [d]

        Returns:
            None
        """
        if self.isScrollingX:
            if key == K_d:
                self.__set_vel(-15, 0, True)
            if key == K_a:
                self.__set_vel(15, 0, True)
        if not self.isScrollingX:
            if key == K_d:
                self.player1.vel.x += 15
            if key == K_a:
                self.player1.vel.x -= 15

        if self.isScrollingY:
            if key == K_w:
                self.__set_vel(0, 15, True)
            if key == K_s:
                self.__set_vel(0, -15, True)
        if not self.isScrollingY:
            if key == K_w:
                self.player1.vel.y -= 15
            if key == K_s:
                self.player1.vel.y += 15

    def movement(self):
        """Moves the room if the room is currently capable of scrolling with the player.
        """
        if self.canUpdate:
            self.accel = self.get_accel()
            self.accel_movement()

            self.__sprite_collide_check(self.player1, groups.all_walls)
            if self.isScrollingX and self.isScrollingY:
                for sprite in groups.all_movable:
                    self.__sprite_collide_check(sprite, groups.all_walls)

            # Checking for dashing
            self.__check_for_dash()

            # Teleports the player
            for portal in groups.all_portals:
                if self.player1.hitbox.colliderect(portal.hitbox):
                    portal_in = portal
                    portal_out = calc.get_other_portal(portal_in)

                    if len(groups.all_portals) == 2:
                        self.__teleport_player(portal_in, portal_out)

            self.__recenter_player_x()
            self.__recenter_player_y()

            for sprite in self.__get_sprites_to_recenter():
                sprite.movement()

    def __set_vel(self, value_x: int | float, value_y: int | float, is_additive: bool = False) -> None:
        """Sets the velocity components of the room, as well as all the sprites within the room, to zero.

        Args:
            value_x: X-axis component
            value_y: Y-axis component
            is_additive: Should the values be added to the current vel or override it?
        """
        if not is_additive:
            self.vel = vec(value_x, value_y)
            for sprite in self.__get_sprites_to_recenter():
                sprite.vel = vec(value_x, value_y)
        if is_additive:
            self.vel.x += value_x
            self.vel.y += value_y
            for sprite in self.__get_sprites_to_recenter():
                sprite.vel.x += value_x
                sprite.vel.y += value_y

    def __recenter_player_x(self) -> None:
        """Moves all the objects in the room so that the player is centered along the x-axis.
        """
        if self.isScrollingX:
            if not self.centeringX:
                if self.player1.pos.x != cst.WINWIDTH // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetX = self.posCopy.x - cst.WINWIDTH // 2
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterX = time.time()
                    self.centeringX = True

            if self.centeringX:
                weight = calc.get_time_diff(self.lastRecenterX)
                if weight <= 0.25:
                    self.player1.pos.x = calc.cerp(self.posCopy.x, cst.WINWIDTH // 2, weight * 4)
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.pos.x = calc.cerp(sprite.posCopy.x, sprite.posCopy.x - self.offsetX, weight * 4)
                else:
                    self.player1.pos.x = cst.WINWIDTH // 2
                    self.centeringX = False

    def __recenter_player_y(self) -> None:
        """Moves all the objects in the room so that the player is centered along the y-axis.
        """
        if self.isScrollingY:
            if not self.centeringY:
                if self.player1.pos.y != cst.WINHEIGHT // 2:
                    self.posCopy = self.player1.pos.copy()
                    self.offsetY = self.posCopy.y - cst.WINHEIGHT // 2
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.posCopy = sprite.pos.copy()

                    self.lastRecenterY = time.time()
                    self.centeringY = True

            if self.centeringY:
                weight = calc.get_time_diff(self.lastRecenterY)
                if weight <= 0.25:
                    self.player1.pos.y = calc.cerp(self.posCopy.y, cst.WINHEIGHT // 2, weight * 4)
                    for sprite in self.__get_sprites_to_recenter():
                        sprite.pos.y = calc.cerp(sprite.posCopy.y, sprite.posCopy.y - self.offsetY, weight * 4)
                else:
                    self.player1.pos.y = cst.WINHEIGHT // 2
                    self.centeringY = False

    def __get_sprites_to_recenter(self) -> list:
        """Returns a list containing all sprites that should be relocated when the player is centered.

        Returns:
            list: A list containing all sprites that should be relocated when the player is centered
        """
        output_list = []
        for sprite in self.sprites():
            output_list.append(sprite)

        for drop in groups.all_drops:
            if drop.visible:
                output_list.append(drop)

        for container in groups.all_containers:
            if container.room == self.room:
                for sprite in container:
                    output_list.append(sprite)

        return output_list

    # -------------------------------- Teleporting ------------------------------- #
    def __align_player_after_tp(self, offset: float, direction: str, portal_out, width, height) -> None:
        """Sets the player at the proper position after teleporting when the room can scroll.

        Args:
            offset: The distance the player is (on either x or y-axis, not both) from the center of the entering portal
            direction: The direction the exit portal is facing
            portal_out: The exit portal sprite
            width: Half the sum of the player's hitbox width plus the portal's hitbox width
            height: Half the sum of the player's hitbox height plus the portal's hitbox height
        """
        if direction == cst.SOUTH:
            self.player1.pos.x = portal_out.pos.x - offset
            self.player1.pos.y = portal_out.pos.y + height

        elif direction == cst.EAST:
            self.player1.pos.x = portal_out.pos.x + width
            self.player1.pos.y = portal_out.pos.y - offset

        elif direction == cst.NORTH:
            self.player1.pos.x = portal_out.pos.x + offset
            self.player1.pos.y = portal_out.pos.y - height

        elif direction == cst.WEST:
            self.player1.pos.x = portal_out.pos.x - width
            self.player1.pos.y = portal_out.pos.y + offset

    def __teleport_player(self, portal_in, portal_out) -> None:
        """Teleports the player when the room is scrolling.

        Args:
            portal_in: The portal the player is entering
            portal_out: The portal the player is exiting
        """
        combined_width = (portal_out.hitbox.width + self.player1.hitbox.width) // 2
        combined_height = (portal_out.hitbox.height + self.player1.hitbox.height) // 2
        direction_in = portal_in.facing
        direction_out = portal_out.facing
        direction_angles = {cst.SOUTH: 180, cst.EAST: 90, cst.NORTH: 0, cst.WEST: 270}

        # Calculating where player should exit portal relative to the position entered
        distance_offset = 0.0
        if direction_in in [cst.SOUTH, cst.NORTH]:
            distance_offset = self.player1.pos.x - portal_in.pos.x
        elif direction_in in [cst.EAST, cst.WEST]:
            distance_offset = self.player1.pos.y - portal_in.pos.y

        # Setting the player's position (actually teleporting the player)
        self.__align_player_after_tp(distance_offset, direction_out, portal_out, combined_width, combined_height)

        # Scrolling x and y
        if self.isScrollingX and self.isScrollingY:
            if direction_in == cst.EAST:
                direction_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif direction_in == cst.NORTH:
                direction_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif direction_in == cst.WEST:
                direction_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self.__sprites_rotate_trajectory(direction_angles[direction_out])

        # Scrolling x, not scrolling y
        elif self.isScrollingX and not self.isScrollingY:
            if direction_in == cst.SOUTH:
                direction_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == cst.EAST:
                direction_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

            if direction_in == cst.NORTH:
                direction_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.y = 0

            if direction_in == cst.WEST:
                direction_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.x = 0

        # Scrolling y, not scrolling x
        elif not self.isScrollingX and self.isScrollingY:
            if direction_in == cst.SOUTH:
                direction_angles.update({cst.SOUTH: 180, cst.EAST: 270, cst.NORTH: 0, cst.WEST: 90})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == cst.EAST:
                direction_angles.update({cst.SOUTH: 90, cst.EAST: 180, cst.NORTH: 270, cst.WEST: 0})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

            if direction_in == cst.NORTH:
                direction_angles.update({cst.SOUTH: 0, cst.EAST: 90, cst.NORTH: 180, cst.WEST: 270})
                if direction_out == direction_in:
                    self.__sprites_rotate_trajectory(direction_angles[direction_out])
                if direction_out in [cst.EAST, cst.WEST]:
                    self.__translate_trajectory(False, direction_angles[direction_out])
                    self.vel.y = 0

            if direction_in == cst.WEST:
                direction_angles.update({cst.SOUTH: 270, cst.EAST: 0, cst.NORTH: 90, cst.WEST: 180})
                if direction_out == direction_in:
                    self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])
                if direction_out in [cst.SOUTH, cst.NORTH]:
                    self.__translate_trajectory(True, direction_angles[direction_out])
                    self.player1.vel.x = 0

        elif not self.isScrollingX and not self.isScrollingY:
            if direction_in == cst.EAST:
                direction_angles.update({cst.EAST: 180, cst.NORTH: 90, cst.WEST: 0, cst.SOUTH: 270})
            elif direction_in == cst.NORTH:
                direction_angles.update({cst.NORTH: 180, cst.WEST: 90, cst.SOUTH: 0, cst.EAST: 270})
            elif direction_in == cst.WEST:
                direction_angles.update({cst.WEST: 180, cst.SOUTH: 90, cst.EAST: 0, cst.NORTH: 270})
            self.player1.vel = self.player1.vel.rotate(direction_angles[direction_out])

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

            if calc.triangle_collide(instig, sprite) == cst.SOUTH and (
                    instig.vel.y < 0 or sprite.vel.y > 0) and instig.pos.y <= sprite.pos.y + height:
                self.accel.y = 0
                self.vel.y = 0
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if calc.triangle_collide(instig, sprite) == cst.EAST and (
                    instig.vel.x < 0 or sprite.vel.x > 0) and instig.pos.x <= sprite.pos.x + width:
                self.accel.x = 0
                self.vel.x = 0
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if calc.triangle_collide(instig, sprite) == cst.NORTH and (
                    instig.vel.y > 0 or sprite.vel.y < 0) and instig.pos.y >= sprite.pos.y - height:
                self.accel.y = 0
                self.vel.y = 0
                self.player1.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if calc.triangle_collide(instig, sprite) == cst.WEST and (
                    instig.vel.x > 0 or sprite.vel.x < 0) and instig.pos.x >= sprite.pos.x - width:
                self.accel.x = 0
                self.vel.x = 0
                self.player1.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    @staticmethod
    def __sprite_block_from_side(instig, sprite) -> None:
        if instig.hitbox.colliderect(sprite.hitbox):
            width = (instig.hitbox.width + sprite.hitbox.width) // 2
            height = (instig.hitbox.height + sprite.hitbox.height) // 2

            if (calc.triangle_collide(instig, sprite) == cst.SOUTH and
                    instig.pos.y <= sprite.pos.y + height and (
                    instig.vel.y < 0 or sprite.vel.y > 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y + height

            if (calc.triangle_collide(instig, sprite) == cst.EAST and
                    instig.pos.x <= sprite.pos.x + width and (
                    instig.vel.x < 0 or sprite.vel.x > 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x + width

            if (calc.triangle_collide(instig, sprite) == cst.NORTH and
                    instig.pos.y >= sprite.pos.y - height and (
                    instig.vel.y > 0 or sprite.vel.y < 0)):
                instig.vel.y = 0
                instig.pos.y = sprite.pos.y - height

            if (calc.triangle_collide(instig, sprite) == cst.WEST and
                    instig.pos.x >= sprite.pos.x - width and (
                    instig.vel.x > 0 or sprite.vel.x < 0)):
                instig.vel.x = 0
                instig.pos.x = sprite.pos.x - width

    # -------------------------------- Room Layout ------------------------------- #
    def __change_room(self) -> None:
        width = self.player1.hitbox.width // 2
        height = self.player1.hitbox.height // 2

        if self.player1.pos.y >= self.borderSouth.pos.y - height:
            self.room.y -= 1
            self.lastEntranceDir = cst.SOUTH
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.x >= self.borderEast.pos.x - width:
            self.room.x += 1
            self.lastEntranceDir = cst.EAST
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.y <= self.borderNorth.pos.y + height:
            self.room.y += 1
            self.lastEntranceDir = cst.NORTH
            self.layout_update()
            calc.kill_groups(groups.all_projs)

        elif self.player1.pos.x <= self.borderWest.pos.x + width:
            self.room.x -= 1
            self.lastEntranceDir = cst.WEST
            self.layout_update()
            calc.kill_groups(groups.all_projs)

    def __check_room_change(self) -> None:
        """If the player touches a room border, he/she will change rooms.
        """
        if not self.centeringX and not self.centeringY:
            self.__change_room()

    def __set_room_borders(self, room_width: int, room_height: int) -> None:
        """Sets the borders of the room.

        Args:
            room_width: The width of the room (in pixels)
            room_height: The height of the room (in pixels)
        """
        west_coords = vec(-8, room_height // 2)
        north_coords = vec(room_width // 2, -8)
        south_coords = vec(north_coords.x, north_coords.y + room_height + 16)
        east_coords = vec(west_coords.x + room_width + 16, room_height // 2)

        if room_width < cst.WINWIDTH:
            west_coords.x = cst.WINWIDTH / 2 - room_width / 2 - 8
            east_coords.x = west_coords.x + room_width + 16
            south_coords.x = west_coords.x + room_width / 2 + 8
            north_coords.x = south_coords.x

        if room_height < cst.WINHEIGHT:
            north_coords.y = cst.WINHEIGHT / 2 - room_height / 2 - 8
            south_coords.y = north_coords.y + room_height + 16
            east_coords.y = north_coords.y + room_height / 2 + 8
            west_coords.y = east_coords.y

        self.borderSouth = tiles.RoomBorder(south_coords.x, south_coords.y, room_width / 16, 1)
        self.borderEast = tiles.RoomBorder(east_coords.x, east_coords.y, 1, room_height / 16)
        self.borderNorth = tiles.RoomBorder(north_coords.x, north_coords.y, room_width / 16, 1)
        self.borderWest = tiles.RoomBorder(west_coords.x, west_coords.y, 1, room_height / 16)

        self.add(self.borderSouth, self.borderEast, self.borderNorth, self.borderWest)

    def __init_room(self, room_size_x: int, room_size_y: int, can_scroll_x: bool, can_scroll_y: bool) -> None:
        """Initializes a room's properties. This function must be called once for every room iteration.

        Args:
            room_size_x: The width of the room (in pixels).
            room_size_y: The height of the room (in pixels).
            can_scroll_x: Should the room scroll with the player along the x-axis?
            can_scroll_y: Should the room scroll with the player along the y-axis?
        """
        self.__set_room_borders(room_size_x, room_size_y)
        if self.lastEntranceDir == cst.SOUTH:
            self.player1.pos.x = self.borderNorth.pos.x
            self.player1.pos.y = (self.borderNorth.pos.y + self.borderNorth.hitbox.height // 2
                                  + self.player1.hitbox.height // 2)

        elif self.lastEntranceDir == cst.EAST:
            self.player1.pos.x = (self.borderWest.pos.x +
                                  self.borderWest.hitbox.width // 2 + self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderWest.pos.y

        elif self.lastEntranceDir == cst.NORTH:
            self.player1.pos.x = self.borderSouth.pos.x
            self.player1.pos.y = (self.borderSouth.pos.y -
                                  self.borderSouth.hitbox.height // 2 - self.player1.hitbox.height // 2)

        elif self.lastEntranceDir == cst.WEST:
            self.player1.pos.x = (self.borderEast.pos.x -
                                  self.borderEast.hitbox.width // 2 - self.player1.hitbox.width // 2)
            self.player1.pos.y = self.borderEast.pos.y

        player_vel_copy = self.player1.vel.copy()
        self.player1.vel = vec(0, 0)
        self.size = vec((room_size_x, room_size_y))

        scroll_copy_x = copy.copy(self.isScrollingX)
        scroll_copy_y = copy.copy(self.isScrollingY)
        self.isScrollingX = can_scroll_x
        self.isScrollingY = can_scroll_y

        self.__get_room_change_trajectory(scroll_copy_x, scroll_copy_y, self.isScrollingX, self.isScrollingY,
                                          player_vel_copy)

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
        # x-axis
        if prev_room_scroll_x:
            if not new_room_scroll_x:
                self.player1.vel.x = -self.vel.x

        elif not prev_room_scroll_x:
            if new_room_scroll_x:
                self.__set_vel(-player_vel.x, 0)
            # elif not new_room_scroll_x:
            #     self.player1.vel.x = player_vel.x

        # y-axis
        if prev_room_scroll_y:
            if not new_room_scroll_y:
                self.player1.vel.y = -self.vel.y

        elif not prev_room_scroll_y:
            if new_room_scroll_y:
                self.vel.y = -player_vel.y
            elif not new_room_scroll_y:
                self.player1.vel.y = player_vel.y

    def layout_update(self) -> None:
        """Updates the layout of the room
        """
        for sprite in self.sprites():
            sprite.kill()

        container: RoomContainer
        for container in groups.all_containers:
            container.hide_sprites()

        # ------------------------------- Room Layouts ------------------------------- #
        if self.room == vec(0, 0):
            self.add(
                trinkets.Button(1, 14, 38),
            )

            try:
                container: RoomContainer = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        trinkets.Box(cst.WINWIDTH // 2, cst.WINHEIGHT // 2),
                        enemies.StandardGrunt(200, 200),
                        enemies.Ambusher(500, 500),
                    )
                )
            self.__init_room(cst.WINWIDTH, cst.WINHEIGHT * 4, True, True)

        if self.room == vec(0, 1):
            self.add(
                tiles.Wall(cst.WINWIDTH // 4 + 32, cst.WINHEIGHT // 4 + 32, 4, 4)
            )

            try:
                container: RoomContainer = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        # Box(300, 400)
                    )
                )
            self.__init_room(cst.WINWIDTH // 2, cst.WINHEIGHT // 2, False, False)

        if self.room == vec(1, 0):
            self.add(

            )

            try:
                container: RoomContainer = next(c for c in groups.all_containers if c.room == self.room)
                container.show_sprites()

            except StopIteration:
                groups.all_containers.append(
                    RoomContainer(
                        self.room.x, self.room.y,
                        # Box(300, 400)
                    )
                )
            self.__init_room(cst.WINWIDTH, cst.WINHEIGHT, False, False)

    def update(self):
        self.__check_room_change()
        self.movement()

    def __repr__(self):
        return f'Room({self.room}, {self.pos}, {self.vel}, {self.accel})'


class RoomContainer(cb.AbstractBase):
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

    # TODO: Allow sprites to be redrawn back on their original layers
    def show_sprites(self, layer='enemy'):
        for sprite in self.sprites():
            sprite.show(cst.LAYER[layer])
            sprite.accel = vec(0, 0)
            sprite.vel = vec(0, 0)
            sprite.pos = sprite.roomPos


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
def redraw_game_window():
    """Draws all sprites every frame.
    """
    groups.all_sprites.update()
    groups.all_sprites.draw(screen.buffer_screen)
    main_room.update()
    screen.viewport.blit(screen.buffer_screen, calc.screen_shake_queue.run())
    pygame.display.update()

    screen.buffer_screen.fill((255, 255, 255))


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
# Load room
main_room = Room(0, 0)


def check_key_release(is_mouse, *inputs) -> None:
    """Checks if any input(s) has been released. If one has, then its count in key_released will be updated to match.

    Args:
        is_mouse: Are the inputs mouse buttons?
        *inputs: The input(s) to check
    """
    if not is_mouse:
        for input_key in inputs:
            if event.type == pygame.KEYUP and event.key == input_key:
                if input_key in ctrl.is_input_held and input_key in ctrl.key_released:
                    ctrl.key_released[input_key] += 1
    else:
        for button in inputs:
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                if button in ctrl.is_input_held and button in ctrl.key_released:
                    ctrl.key_released[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
running = True
while running:
    for a_player in groups.all_players:
        if a_player.hp <= 0:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()

        if event.type == QUIT or keyPressed[K_ESCAPE]:
            sys.exit()

        ctrl.is_input_held = {
            1: pygame.mouse.get_pressed(5)[0],
            2: pygame.mouse.get_pressed(5)[1],
            3: pygame.mouse.get_pressed(5)[2],

            K_a: keyPressed[K_a],
            K_w: keyPressed[K_w],
            K_s: keyPressed[K_s],
            K_d: keyPressed[K_d],
            K_x: keyPressed[K_x],
            K_e: keyPressed[K_e],
        }

        check_key_release(False, K_a, K_w, K_s, K_d, K_e, K_x)
        check_key_release(True, 1, 2, 3)

        if event.type == pygame.MOUSEWHEEL:
            # Player ammo refill
            if main_room.player1.ammo < main_room.player1.maxAmmo:
                main_room.player1.ammo += 1

    screen.buffer_screen.fill((255, 255, 255))

    calc.draw_text(f'{main_room.player1}', 0, 0)

    # ------------------------------ Game Operation ------------------------------ #
    for portals in groups.all_portals:
        pygame.draw.rect(screen.viewport, cst.RED, portals.hitbox, 3)

    # ------------------------------- Redraw Window ------------------------------ #
    redraw_game_window()
    clock.tick_busy_loop(cst.FPS)
