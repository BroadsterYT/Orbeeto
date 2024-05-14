"""
Contains the player class.
"""
import os
import time
import math

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import items
import projectiles as proj
import text

import calc
import classbases as cb
import constants as cst
import groups
import statbars
import timer


class Player(cb.ActorBase):
    """A player sprite that can move and shoot.
    """
    def __init__(self):
        super().__init__(cst.LAYER['player'])
        self.show()
        groups.all_players.add(self)
        self.room = cb.get_room()

        self.last_textbox_release = ctrl.key_released[ctrl.K_DIALOGUE]

        self.set_images(os.path.join(os.getcwd(), 'sprites/orbeeto/orbeeto.png'), 64, 64, 5, 5)
        self.set_rects(0, 0, 64, 64, 32, 32)

        self.pos = vec((cst.WINWIDTH // 2, cst.WINHEIGHT // 2))
        self.accel_const = 0.58

        # -------------------------------- Game Stats -------------------------------- #
        self._xp = 0
        self.level = 0
        self.max_level = 249

        self.max_hp = 50
        self.hp = 50
        self.max_defense = 10
        self.defense = 10

        self.last_regen = timer.g_timer.time  # Used for timing passive regeneration

        self.max_ammo = 40
        self.ammo = self.max_ammo
        self.bullet_vel = 10
        self.gun_cooldown = 0.12
        self.last_shot_time = time.time()

        self.grapple_speed = 2.0

        self.last_hit = timer.g_timer.time

        self.update_level()

        # --------------------------------- Stat Bars -------------------------------- #
        self.health_bar = statbars.StatBar(self, 0, 'hp', 'max_hp', 'sprites/stat_bars/health_bar.png')
        self.ammo_bar = statbars.StatBar(self, 1, 'ammo', 'max_ammo', 'sprites/stat_bars/ammo_bar.png')

        # ---------------------------- Menu and Inventory ---------------------------- #
        self.my_materials = {}
        for item in items.MATERIALS:
            self.my_materials.update({item: 0})

        self.my_armors = {}
        for armor in items.ARMOR.values():
            self.my_armors.update({armor: False})
        self.my_armors.update({items.ARMOR[0]: True})

        self.my_weapons = {}
        for weapon in items.WEAPONS.values():
            self.my_weapons.update({weapon: False})
        self.my_weapons.update({items.WEAPONS[0]: True, items.WEAPONS[1]: True})\

        # ---------------------- Bullets, Portals, and Grapples ---------------------- #
        self.bullet_type = cst.PROJ_STD
        self.can_portal = False

        self.grapple = None
        self.can_grapple = True
        self.grapple_input_copy = ctrl.key_released[ctrl.K_GRAPPLE]

    @property
    def xp(self):
        """The amount of experience points the player has collected. The more xp the player has, the higher their
        level will be."""
        return self._xp

    @xp.setter
    def xp(self, value: int):
        if value > 582803:
            self._xp = 582803
        else:
            self._xp = value

    # ----------------------------------- Stats ---------------------------------- #
    def update_max_stats(self):
        """Updates all the player's max stats.
        """
        self.max_hp = math.floor(calc.eerp(50, 650, self.level / self.max_level))
        self.max_defense = math.floor(calc.eerp(15, 800, self.level / self.max_level))
        self.max_ammo = math.floor(calc.eerp(40, 500, self.level / self.max_level))

        self.grapple_speed = math.floor(calc.eerp(2.0, 4.0, self.level / self.max_level))

        self.defense = self.max_defense

    def update_level(self) -> None:
        """Updates the level of the player using the amount of xp collected.

        Returns:
            None
        """
        self.level = math.floor((256 * self.xp) / (self.xp + 16384))
        self.update_max_stats()

    def _passive_hp_regen(self) -> None:
        """Regenerates the player's HP after not being attacked for a period of time.
        """
        time_hit = calc.get_game_tdiff(self.last_hit)
        regen_delay = 5
        regens_per_sec = 0

        if time_hit < regen_delay:
            regens_per_sec = 0
        elif time_hit >= regen_delay:
            regens_per_sec = pow(0.95, -(time_hit - regen_delay + 1)) - (1 / regen_delay)

        if regens_per_sec == 0:
            pass
        elif calc.get_game_tdiff(self.last_regen) >= 1 / regens_per_sec:
            if self.hp < self.max_hp:
                self.hp += 1
            self.last_regen = timer.g_timer.time

    # --------------------------------- Movement --------------------------------- #
    @cb.check_update_state
    def movement(self):
        """When called once every frame, it allows the player to receive input from the user and move accordingly
        """
        self.accel = self.get_accel()
        self.accel_movement()

        self.shoot()

    def get_accel(self) -> pygame.math.Vector2:
        """Returns the acceleration that the player should undergo given specific conditions.

        Returns:
            pygame.math.Vector2: The acceleration value of the player
        """
        final_accel = vec(0, 0)
        if not self.room.is_scrolling_x:
            final_accel.x += self._get_x_axis_output()
        if not self.room.is_scrolling_y:
            final_accel.y += self._get_y_axis_output()

        # Centering player in scrolling room
        scroll_weight = calc.get_scroll_weight(self)
        if self.room.is_scrolling_x:
            if self.pos.x != cst.WINWIDTH // 2:
                final_accel.x += scroll_weight.x
        if self.room.is_scrolling_y:
            if self.pos.y != cst.WINHEIGHT // 2:
                final_accel.y += scroll_weight.y

        return final_accel

    def _get_x_axis_output(self) -> float:
        output = 0.0
        if ctrl.is_input_held[ctrl.K_MOVE_LEFT]:
            output -= self.accel_const
        if ctrl.is_input_held[ctrl.K_MOVE_RIGHT]:
            output += self.accel_const

        if self.is_swinging():
            angle = calc.get_angle(self, self.grapple)
            output += self.grapple_speed * -math.sin(math.radians(angle))

        return output

    def _get_y_axis_output(self) -> float:
        output = 0.0
        if ctrl.is_input_held[ctrl.K_MOVE_UP]:
            output -= self.accel_const
        if ctrl.is_input_held[ctrl.K_MOVE_DOWN]:
            output += self.accel_const

        if self.is_swinging():
            angle = calc.get_angle(self, self.grapple)
            output += self.grapple_speed * -math.cos(math.radians(angle))

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
        elif self.grapple.grappled_to not in groups.all_walls:
            return output
        else:
            output = True
            return output

    def shoot(self):
        """Shoots bullets.
        """
        angle = math.radians(calc.get_angle_to_mouse(self))
        vel_x = self.bullet_vel * -math.sin(angle)
        vel_y = self.bullet_vel * -math.cos(angle)

        offset = vec((21, 30))

        if (ctrl.is_input_held[1] and
                self.ammo > 0 and
                calc.get_game_tdiff(self.last_shot_time) >= self.gun_cooldown):
            # Standard bullets
            if self.bullet_type == cst.PROJ_STD:
                groups.all_projs.add(
                    proj.PlayerStdBullet(self.pos.x - (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                         self.pos.y + (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                         vel_x, vel_y),
                    proj.PlayerStdBullet(self.pos.x + (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                         self.pos.y - (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                         vel_x, vel_y)
                )

            # Laser bullets
            elif self.bullet_type == cst.PROJ_LASER:
                groups.all_projs.add(
                    proj.PlayerLaserBullet(self.pos.x - (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                           self.pos.y + (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                           vel_x * 2, vel_y * 2),
                    proj.PlayerLaserBullet(self.pos.x + (offset.x * math.cos(angle)) - (offset.y * math.sin(angle)),
                                           self.pos.y - (offset.x * math.sin(angle)) - (offset.y * math.cos(angle)),
                                           vel_x * 2, vel_y * 2)
                )

            self.ammo -= 1
            self.last_shot_time = timer.g_timer.time

        # ------------------------------ Firing Portals ------------------------------ #
        if ctrl.key_released[3] % 2 == 0 and self.can_portal:
            groups.all_projs.add(proj.PortalBullet(self.pos.x, self.pos.y, vel_x, vel_y))
            self.can_portal = False

        elif ctrl.key_released[3] % 2 != 0 and not self.can_portal:
            groups.all_projs.add(proj.PortalBullet(self.pos.x, self.pos.y, vel_x, vel_y))
            self.can_portal = True

        # --------------------------- Firing Grappling Hook -------------------------- #
        if self.grapple_input_copy < ctrl.key_released[ctrl.K_GRAPPLE] and self.can_grapple:
            self.grapple = proj.GrappleBullet(self, self.pos.x, self.pos.y, vel_x, vel_y)
            self.can_grapple = False
            self.grapple_input_copy = ctrl.key_released[ctrl.K_GRAPPLE]

        elif (ctrl.key_released[ctrl.K_GRAPPLE] - 1 <= self.grapple_input_copy < ctrl.key_released[ctrl.K_GRAPPLE]
              and not self.can_grapple):
            if self.grapple is not None:
                self.grapple.returning = True
            else:
                self.can_grapple = True
                self.grapple_input_copy = ctrl.key_released[ctrl.K_GRAPPLE]

        # Double-click to destroy grapple immediately
        if self.grapple_input_copy < ctrl.key_released[ctrl.K_GRAPPLE] - 1:
            try:
                self.grapple.shatter()
            except AttributeError:
                pass
            self.can_grapple = True
            self.grapple_input_copy = ctrl.key_released[ctrl.K_GRAPPLE]

    # TODO: Player object should not have control over textbox handling. Move to either room or separate object.
    # def _get_closest_interact(self):
    #     sprite_dists = {}
    #     for sprite in [s for s in itertools.chain(groups.all_movable, groups.all_trinkets) if s.visible]:
    #         sprite_dists.update({sprite: calc.get_dist(self, sprite)})
    #     try:
    #         shortest_dist = min(sprite_dists.values())
    #         closest_sprites = [key for key in sprite_dists if sprite_dists[key] == shortest_dist]
    #         if shortest_dist <= 128:  # TODO: Calculate proper radius to activate
    #             return closest_sprites[0]
    #         else:
    #             return None
    #
    #     except ValueError:
    #         return None
    #
    # def _get_dialogue(self) -> str:
    #     """Returns the proper dialogue to show when in proximity to a sprite.
    #
    #     Returns:
    #         str: The correct dialogue from ``dialogue.all_dialogue_lines``
    #     """
    #     closest_sprite = self._get_closest_interact()
    #     print(closest_sprite.__class__.__name__)
    #     if closest_sprite is None:
    #         return 'default'
    #     elif isinstance(closest_sprite, trinkets.Box):
    #         return 'box_test'
    #     elif isinstance(closest_sprite, trinkets.Button):
    #         return 'error'
    #     else:
    #         return 'error'
    #
    # def generate_text_box(self) -> None:
    #     """Generates dialogue based on specific conditions."""
    #     if self.last_textbox_release != ctrl.key_released[ctrl.K_DIALOGUE]:
    #         if len(groups.all_text_boxes) < 1:
    #             groups.all_text_boxes.add(
    #                 text.TextBox(cst.WINWIDTH // 2, cst.WINHEIGHT - 90, self._get_dialogue())
    #             )
    #         self.last_textbox_release = ctrl.key_released[ctrl.K_DIALOGUE]

    @cb.check_update_state
    def update(self):
        self.movement()

        # Animation
        self._animate()
        self.rotate_image(calc.get_angle_to_mouse(self))

        self._passive_hp_regen()

        # TODO: Move textbox handling out of player object
        # self.generate_text_box()

        if self.hp <= 0:
            self.kill()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 0.05:
            if ctrl.is_input_held[1]:
                self.index += 1
                if self.index > 4:
                    self.index = 0
            else:  # Idle animation
                self.index = 0

            self.last_frame = time.time()

    def __str__(self):
        return (f'Player at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\ncurrent bullet: {self.bullet_type}\n'
                f'xp: {self.xp}\nlevel: {self.level}\n room: {self.room.room}')

    def __repr__(self):
        return f'Player({self.pos}, {self.vel}, {self.accel}, {self.bullet_type}, {self.xp}, {self.level})'
