import math
import time

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import items
import text
import visuals

import calc
import classbases as cb
import constants as cst
import gamestack as gs
import groups
import spritesheet


class SlotBase(cb.ActorBase):
    def __init__(self, gamestate: gs.GameState, owner, pos_x, pos_y):
        """The base class for all inventory slots.

        :param gamestate: The gamestate the slot should be displayed in
        :param owner: The owner of the slot (should be the inventory menu)
        :param pos_x: The x-position to spawn the slot at
        :param pos_y: The y-position to spawn the slot at
        """
        super().__init__(cst.LAYER['ui_1'], gamestate)
        self.owner = owner

        self.pos = vec(pos_x, pos_y)
        self.start_pos = vec(pos_x, pos_y)
        self.is_panning = False

        self.menu_sheet = spritesheet.Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.menu_images = self.menu_sheet.get_images(64, 64, 1)
        self.menu_image = self.menu_images[0]
        self.index = 0

    def hover(self) -> None:
        """Causes the menu slot to oscillate in size when the mouse cursor hovers over it

        :return: None
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            s_time = time.time()
            scale = abs(math.sin(s_time)) / 2
            self.image = pygame.transform.scale_by(self.images[self.index], 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)


class MaterialSlot(SlotBase):
    def __init__(self, owner, pos_x: int | float, pos_y: int | float, item_held: str | None):
        """A menu slot that shows the collected amount of a specific item.

        :param owner: The inventory the slot belongs to
        :param pos_x: The x-position to spawn at
        :param pos_y: The y-position to spawn at
        :param item_held: The item the menu slot will hold. Items are chosen from MATERIALS dictionary.
        """
        super().__init__(gs.s_inventory, owner, pos_x, pos_y)
        self.add_to_gamestate()
        groups.all_material_slots.add(self)

        self.holding = item_held
        self.count = 0
        self.last_count = 0

        self.item_sheet = spritesheet.Spritesheet("sprites/textures/item_drops.png", 3)

        self.images = self.create_slot_images()
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)
        self.center_rects()

    def _get_item_images(self) -> list:
        """Returns the images of the item a menu slot is designated to hold.

        :return: A list containing the images of the item the slot holds
        """
        if self.holding == items.MATERIALS[0]:
            return self.item_sheet.get_images(32, 32, 1, 0)
        elif self.holding == items.MATERIALS[1]:
            return self.item_sheet.get_images(32, 32, 1, 3)
        elif self.holding == items.MATERIALS[2]:
            return self.item_sheet.get_images(32, 32, 1, 4)
        else:
            return self.item_sheet.get_images(32, 32, 1, 0)

    def create_slot_images(self) -> list:
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that
        item on top.

        :return: A list of the created slot images
        """
        item_images = self._get_item_images()
        final_images = []
        for frame in item_images:
            # new_img = calc.combine_images(self.menu_image, frame)
            new_img: pygame.Surface = self.menu_image.copy()
            center_x = (new_img.get_width() - frame.get_width()) // 2
            center_y = (new_img.get_height() - frame.get_height()) // 2
            new_img.blit(frame, (center_x, center_y))

            # Adding the count of the item to its images
            count_surface = text.text_to_image(str(self.count), text.indicator_font)
            new_img.set_colorkey((0, 0, 0))

            # Changing dark gray to light gray
            color_swap_1 = calc.swap_color(count_surface, (44, 44, 44), (156, 156, 156))
            # Changing black to white
            color_swap_2 = calc.swap_color(color_swap_1, (0, 0, 1), (255, 255, 255))

            new_img.blit(color_swap_2, vec(center_x, center_y))
            final_images.append(new_img)

        return final_images

    def update(self):
        self.center_rects()

        self.count = self.owner.owner.my_materials[self.holding]
        if self.last_count != self.count:
            self.images = self.create_slot_images()
            self.last_count = self.count

        self._animate()
        self.hover()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 1:
            if self.holding == items.MATERIALS[0]:
                pass

            self.last_frame = time.time()


class GearSlot(SlotBase):
    def __init__(self, owner, pos_x, pos_y, gear_name, gear_type):
        super().__init__(gs.s_inventory, owner, pos_x, pos_y)
        self.add_to_gamestate()

        self.screen_pos = vec(pos_x % cst.WINWIDTH, pos_y)

        self.holding = gear_name
        self.holding_type = gear_type

        self.gear_sheet = None
        if self.holding_type == 'armor':
            groups.all_armor_slots.add(self)
            self.gear_sheet = spritesheet.Spritesheet('sprites/textures/armor_items.png', 16)
        elif self.holding_type == 'l_gun':
            groups.all_l_gun_slots.add(self)
            self.gear_sheet = spritesheet.Spritesheet('sprites/orbeeto/guns.png', 5)
        elif self.holding_type == 'r_gun':
            groups.all_r_gun_slots.add(self)
            self.gear_sheet = spritesheet.Spritesheet('sprites/orbeeto/guns.png', 5)
        elif self.holding_type == 'article':
            # Add to article group here
            self.gear_sheet = spritesheet.Spritesheet('sprites/textures/armor_items.png', 16)
        else:
            raise ValueError(f'self.holding must be \'armor\', \'l_gun\', \'r_gun\', or \'article\', '
                             f'not \'{self.holding_type}\')')

        self.images = self.create_slot_images()
        self.image = self.images[self.index]
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

        self.last_release_value = ctrl.key_released[1]

    def _get_gear_images(self) -> list[pygame.Surface]:
        if self.holding == items.ARMOR[0]:
            return self.gear_sheet.get_images(64, 64, 16, 0)
        elif self.holding == items.ARMOR[1]:
            return self.gear_sheet.get_images(64, 64, 16, 16)
        elif self.holding == items.ARMOR[2]:
            return self.gear_sheet.get_images(64, 64, 16, 32)

        elif self.holding == items.WEAPONS[0]:
            return self.gear_sheet.get_images(64, 64, 5, 0)
        elif self.holding == items.WEAPONS[2]:
            return self.gear_sheet.get_images(64, 64, 5, 10)
        else:
            raise ValueError(f'holding field must be acceptable value, not \"{self.holding}\"')

    def create_slot_images(self) -> list[pygame.Surface]:
        """Combines the item's image(s) with the menu slot image, returning the results within a list

        :return: A list of the completed slot images
        """
        final_images = []
        gear_images = self._get_gear_images()
        for frame in gear_images:
            menu_image = visuals.stack_images(self.menu_image, frame, 0, 0)
            menu_image.set_colorkey((0, 0, 0))
            final_images.append(menu_image)
        return final_images

    def check_select(self) -> None:
        """Checks if the gear slot is clicked and updates the player's gear accordingly.

        :return: None
        """
        if (self.last_release_value == ctrl.key_released[1] - 1 and self.hitbox.collidepoint(pygame.mouse.get_pos())
                and ctrl.last_click_pos[1] == self.gamestate and ctrl.last_release_pos[1] == self.gamestate
                and self.owner.owner.my_equipment[self.holding]):
            player = self.owner.owner
            if self.holding_type == 'armor':
                player.update_armor_selection(self.holding)
                print(f'New armor: {self.holding}')

            elif self.holding_type == 'l_gun':
                player.update_l_gun_selection(self.holding)
                print(f'New l gun: {self.holding}')

            self.last_release_value = ctrl.key_released[1]
        else:
            self.last_release_value = ctrl.key_released[1]

    def update(self):
        self.center_rects()
        self.check_select()
        self.hover()
