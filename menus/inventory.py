import time

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import items
import menus

import calc
import classbases as cb
import constants as cst
import gamestack as gs


class InventoryMenu(cb.AbstractBase):
    def __init__(self, owner):
        """A menu used to view collected items and utilize them for various purposes"""
        super().__init__()
        self.cycling_left = False
        self.cycling_right = False
        self.owner = owner

        self.is_open = False

        self.window = 0

        self.last_release_value = ctrl.key_released[ctrl.K_MENU]
        self.last_cycle = time.time()

        self.right_arrow = menus.MenuArrow(gs.s_inventory, cst.WINWIDTH - 64, cst.WINHEIGHT / 2, cst.EAST,
                                           self.pan_left)
        self.left_arrow = menus.MenuArrow(gs.s_inventory, 64, cst.WINHEIGHT / 2, cst.WEST, self.pan_right)

        self.widget_test = menus.ScrollWidget(gs.s_inventory, 300, 300, 320, 416 + 32*7, 64)
        self.widget_test.add_entry(
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
            menus.ScrollWidgetEntry(self.widget_test, 'hello'),
        )
        self.widget_test.assign_scroll_values()

        self.add(
            self.build_materials_slots(),
            self.build_gun_slots(),
            self.build_armor_slots(),
            self.widget_test
        )

    def pan_left(self):
        if not self.cycling_left and not self.cycling_right:
            self.window += 1
            self.last_cycle = time.time()
            self.cycling_right = True
            for sprite in self.sprites():
                sprite.is_panning = True

    def pan_right(self):
        if not self.cycling_left and not self.cycling_right:
            self.window -= 1
            self.last_cycle = time.time()
            self.cycling_left = True
            for sprite in self.sprites():
                sprite.is_panning = True

    def cycle_menu(self) -> None:
        """Pans the menu from screen to screen

        :return: None
        """
        # Cycling left
        if self.cycling_left and not self.cycling_right:
            weight = calc.get_time_diff(self.last_cycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.start_pos.x, sprite.start_pos.x - cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x -= cst.WINWIDTH
                    sprite.is_panning = False
                self.cycling_left = False

        # Cycling right
        if not self.cycling_left and self.cycling_right:
            weight = calc.get_time_diff(self.last_cycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.start_pos.x, sprite.start_pos.x + cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.start_pos.x += cst.WINWIDTH
                    sprite.is_panning = False
                self.cycling_right = False

    def build_materials_slots(self) -> list:
        """Creates and aligns the materials slots of the menu.

        :return: A list containing the materials slots created
        """
        count = 0
        space = vec(64, 64)
        space_cushion = vec(82, 82)
        menu_slots = []
        offset = 0
        for y in range(5):
            for x in range(5):
                menu_slots.append(
                    menus.MaterialSlot(self, space.x, space.y, items.MATERIALS[count])
                )
                space.x += space_cushion.x
                offset += 1
                count += 1
            space.y += space_cushion.y
            space.x = 64
        return menu_slots

    def build_armor_slots(self) -> list:
        """Creates and aligns the armor slots of the menu.

        :return: A list containing the armor slots created
        """
        count = 0
        space = vec(512 + cst.WINWIDTH, 64)
        space_cushion = vec(82, 82)
        menu_slots = []
        offset = 0
        for y in range(1):
            for x in range(3):
                menu_slots.append(
                    menus.GearSlot(self, space.x, space.y, items.ARMOR[count], 'armor')
                )
                space.x += space_cushion.x
                offset += 1
                count += 1
            space.y += space_cushion.y
            space.x = 512
        return menu_slots

    def build_gun_slots(self) -> list:
        count = 0
        space = vec(200 + cst.WINWIDTH, 64)
        space_cushion = vec(82, 82)
        menu_slots = []
        offset = 0
        for y in range(1):
            for x in range(2):
                menu_slots.append(
                    menus.GearSlot(self, space.x, space.y, items.WEAPONS[count], 'l_gun')
                )
                space.x += space_cushion.x
                offset += 1
                count += 2
            space.y += space_cushion.y
            space.x = 512
        return menu_slots

    def update(self):
        self.cycle_menu()
