import math
import os
import time

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import items
import menus

import calculations as calc
import classbases as cb
import constants as cst
import groups
import spritesheet


class InventoryMenu(cb.AbstractBase):
    def __init__(self):
        """A menu used to view collected items and utilize them for various purposes
        """
        super().__init__()
        self.cycling_left = False
        self.cycling_right = False

        room = cb.get_room()
        self.owner = room.player1
        self.window = 0

        self.last_release_value = ctrl.key_released[ctrl.K_MENU]
        self.is_open = False

        self.last_cycle = time.time()

        self.right_arrow = RightMenuArrow(cst.WINWIDTH - 64, cst.WINHEIGHT / 2)
        self.left_arrow = LeftMenuArrow(64, cst.WINHEIGHT / 2)

        self.add(
            self.build_materials_slots(),
            self.build_armor_slots()  # noqa
        )

    def hide(self):
        """Makes all the elements of the inventory menu invisible (closes the inventory menu).
        """
        for sprite in self.sprites():
            groups.all_sprites.remove(sprite)

    def show(self):
        """Makes all the elements of the inventory menu visible.
        """
        for sprite in self.sprites():
            groups.all_sprites.add(sprite, layer=sprite.layer)

    def cycle_menu(self):
        if (not self.cycling_left and
                not self.cycling_right and
                not self.can_update):
            if ctrl.is_input_held[1] and self.left_arrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window += 1
                self.last_cycle = time.time()
                self.cycling_right = True

            if ctrl.is_input_held[1] and self.right_arrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window -= 1
                self.last_cycle = time.time()
                self.cycling_left = True

        # Cycling left
        if self.cycling_left and not self.cycling_right:
            weight = calc.get_time_diff(self.last_cycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.start_pos.x, sprite.start_pos.x - cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cycling_left = False

        # Cycling right
        if not self.cycling_left and self.cycling_right:
            weight = calc.get_time_diff(self.last_cycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.start_pos.x, sprite.start_pos.x + cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x = sprite.pos.x
                self.cycling_right = False

    def build_materials_slots(self) -> list:
        """Creates and aligns the materials slots of the menu.

        Returns:
            list: A list containing the materials slots created
        """
        count = 0
        space = vec(64, 64)
        space_cushion = vec(82, 82)
        menu_slots = []
        offset = 0
        for y in range(5):
            for x in range(5):
                menu_slots.append(
                    menus.MaterialSlot(self.owner, space.x, space.y, items.MATERIALS[count])
                )
                space.x += space_cushion.x
                offset += 1
                count += 1
            space.y += space_cushion.y
            space.x = 64
        return menu_slots

    def build_armor_slots(self) -> list:
        count = 0
        space = vec(512, 64)
        space_cushion = vec(82, 82)
        menu_slots = []
        offset = 0
        for y in range(1):
            for x in range(3):
                menu_slots.append(
                    menus.ArmorSlot(self.owner, space.x, space.y, items.ARMOR[count])
                )
                space.x += space_cushion.x
                offset += 1
                count += 1
            space.y += space_cushion.y
            space.x = 512
        return menu_slots

    def update(self):
        if self.last_release_value != ctrl.key_released[ctrl.K_MENU] and not self.is_open:
            self.show()
            self.right_arrow.show()
            self.left_arrow.show()

            self.can_update = False
            for sprite in groups.all_sprites:
                sprite.can_update = False
            room = cb.get_room()
            room.can_update = False

            self.last_release_value = ctrl.key_released[ctrl.K_MENU]
            self.is_open = True

        elif self.last_release_value != ctrl.key_released[ctrl.K_MENU] and self.is_open:
            self.hide()
            self.right_arrow.hide()
            self.left_arrow.hide()

            self.can_update = True
            for sprite in groups.all_sprites:
                sprite.can_update = True
            room = cb.get_room()
            room.can_update = True

            self.last_release_value = ctrl.key_released[ctrl.K_MENU]
            self.is_open = False

        self.cycle_menu()


class RightMenuArrow(cb.ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the right.

        Args:
            pos_x: The x-position the element should be displayed at
            pos_y: The y-position the element should be displayed at
        """
        super().__init__(cst.LAYER['ui_1'])
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/ui/menu_arrow.png'), 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.image = pygame.transform.scale(self.images[self.index], (64, 64))

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x - 32, pos_y - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it."""
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * math.sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        self._animate()
        self.hover()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > cst.SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            self.index += 1
            self.lastFrame = time.time()


class LeftMenuArrow(cb.ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the right.

        Args:
            pos_x: The x-position the element should be displayed at
            pos_y: The y-position the element should be displayed at
        """
        super().__init__(cst.LAYER['ui_1'])
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = spritesheet.Spritesheet("sprites/ui/menu_arrow.png", 8)
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
            self.pos.x = 5 * math.sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        if calc.get_time_diff(self.last_frame) >= cst.SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)
            self.index += 1
            self.last_frame = time.time()

        self.hover()
