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
    def __init__(self):
        """A menu used to view collected items and utilize them for various purposes"""
        super().__init__()
        self.cycling_left = False
        self.cycling_right = False

        room = cb.get_room()
        self.owner = room.player1
        self.window = 0

        self.last_release_value = ctrl.key_released[ctrl.K_MENU]
        self.is_open = False
        self.last_cycle = time.time()

        self.right_arrow = menus.MenuArrow(gs.s_inventory, cst.WINWIDTH - 64, cst.WINHEIGHT / 2, cst.EAST,
                                           self.pan_left)
        self.left_arrow = menus.MenuArrow(gs.s_inventory, 64, cst.WINHEIGHT / 2, cst.WEST, self.pan_right)

        # --------------- Gear Selection Slots --------------- #
        self.armor_select = menus.SelectionSlot(self, 'armor', 600 + cst.WINWIDTH, 600)
        self.last_armor_equip = None

        self.l_gun_select = menus.SelectionSlot(self, 'l_gun', 520 + cst.WINWIDTH, 600)
        self.last_l_gun_equip = None

        self.add(
            self.build_materials_slots(),
            self.build_gun_slots(),
            self.build_armor_slots(),  # noqa
            self.armor_select,  # noqa
            self.l_gun_select,  # noqa
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

    def check_equipped(self) -> None:
        """Checks which equipment is locked into each equipment slot and updates the player's stats accordingly"""
        # print(self.l_gun_select.equipped)
        if self.armor_select.equipped != self.last_armor_equip:
            if self.armor_select.equipped is None:
                self.owner.update_armor_buffs(None)
                self.last_armor_equip = self.armor_select.equipped
            else:
                armor_name = self.armor_select.equipped.holding
                self.owner.update_armor_buffs(armor_name)  # player1.update_armor_buffs()
                self.last_armor_equip = self.armor_select.equipped

        if self.l_gun_select.equipped != self.last_l_gun_equip:
            if self.l_gun_select.equipped is None:
                self.owner.update_l_gun_selection(None)
                self.last_l_gun_equip = self.l_gun_select.equipped
            else:
                l_gun_name = self.l_gun_select.equipped.holding
                self.owner.update_l_gun_selection(l_gun_name)
                self.last_l_gun_equip = self.l_gun_select.equipped

    def update(self):
        self.cycle_menu()
        self.check_equipped()
