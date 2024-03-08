import math
import time

import pygame
from pygame.math import Vector2 as vec

import items
import text

import calculations as calc
import classbases as cb
import constants as cst
import groups
import spritesheet
import visuals


class SlotBase(cb.ActorBase):
    def __init__(self, owner, pos_x, pos_y):
        """The base class for all inventory slots.

        Args:
            owner: The owner of the inventory menu (should be the player)
            pos_x: The x-position to spawn the slot at
            pos_y: The y-position to spawn the slot at
        """
        super().__init__(cst.LAYER['ui_1'])
        self.owner = owner

        self.pos = vec(pos_x, pos_y)
        self.start_pos = vec(pos_x, pos_y)

        self.menu_sheet = spritesheet.Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.menu_images = self.menu_sheet.get_images(64, 64, 1)
        self.menu_image = self.menu_images[0]
        self.index = 0

    def hover(self) -> None:
        """Causes the menu slot to oscillate in size when the mouse cursor hovers over it

        Returns:
            None
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

        Args:
            owner: The owner of the inventory to whom the menu slot belongs to
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
            item_held: The item the menu slot will hold. Items are chosen from MATERIALS dictionary.
        """
        super().__init__(owner, pos_x, pos_y)
        groups.all_slots.add(self)

        self.holding = item_held
        self.count = 0

        self.item_sheet = spritesheet.Spritesheet("sprites/textures/item_drops.png", 3)

        self.images = self.create_slot_images()
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)
        self.center_rects()

    def _get_item_images(self) -> list:
        """Returns the images of the item a menu slot is designated to hold.

        Returns:
            list: A list containing the images of the item the slot holds
        """
        if self.holding == items.MATERIALS[0]:
            return self.item_sheet.get_images(32, 32, 3, 0)
        elif self.holding == items.MATERIALS[1]:
            return self.item_sheet.get_images(32, 32, 1, 3)
        elif self.holding == items.MATERIALS[2]:
            return self.item_sheet.get_images(32, 32, 1, 4)
        else:
            return self.item_sheet.get_images(32, 32, 1, 0)

    def create_slot_images(self) -> list:
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that
        item on top.

        Returns:
            list: A list of the created images
        """
        item_images = self._get_item_images()
        final_images = []
        for frame in item_images:
            new_img = calc.combine_images(self.menu_image, frame)

            # Adding the count of the item to its images
            count_surface = text.text_to_image(str(self.count), text.indicator_font)
            new_img.set_colorkey((0, 0, 0))
            center_x = (new_img.get_width() - frame.get_width()) // 2
            center_y = (new_img.get_height() - frame.get_height()) // 2

            # Changing dark gray to light gray
            color_swap_1 = calc.swap_color(count_surface, (44, 44, 44), (156, 156, 156))
            # Changing black to white
            color_swap_2 = calc.swap_color(color_swap_1, (0, 0, 1), (255, 255, 255))

            new_img.blit(color_swap_2, vec(center_x, center_y))
            final_images.append(new_img)

        return final_images

    def update(self):
        self.center_rects()

        self.count = self.owner.my_materials[self.holding]
        self.images = self.create_slot_images()
        self._animate()

        self.hover()

    def _animate(self):
        if self.holding == items.MATERIALS[0] and calc.get_time_diff(self.last_frame) > 1:
            self.image = self.images[self.index]
            self.index += 1
            if self.index > 2:
                self.index = 0
            self.last_frame = time.time()


class ArmorSlot(SlotBase):
    def __init__(self, owner, pos_x, pos_y, armor_held: str):
        super().__init__(owner, pos_x, pos_y)
        groups.all_slots.add(self)

        self.holding = armor_held
        self.armor_sheet = spritesheet.Spritesheet('sprites/textures/armor_items.png', 16)

        self.images = self.create_slot_images()
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)
        self.center_rects()

    def _get_armor_images(self) -> list:
        if self.holding == items.ARMOR[0]:
            return self.armor_sheet.get_images(64, 64, 16, 0)
        elif self.holding == items.ARMOR[1]:
            return self.armor_sheet.get_images(64, 64, 16, 16)
        elif self.holding == items.ARMOR[2]:
            return self.armor_sheet.get_images(64, 64, 16, 32)
        else:
            raise IndexError(f'No armor visual exists with an armor key of {self.holding}.')

    def create_slot_images(self) -> list:
        final_images = []
        armor_images = self._get_armor_images()

        for frame in armor_images:
            menu_image = pygame.Surface(vec(64, 64))

            if self.owner.my_armors[self.holding]:
                menu_image = visuals.stack_images(self.menu_image, frame, 0, 0)

            elif not self.owner.my_armors[self.holding]:
                blanked_frame = pygame.Surface(frame.get_size())
                blanked_frame.fill((0, 0, 1))

                mix_frame: pygame.Surface = frame.copy()
                mix_frame.blit(blanked_frame, vec(0, 0), special_flags=pygame.BLEND_MULT)

                menu_image = visuals.stack_images(self.menu_image, mix_frame, 0, 0)

            menu_image.set_colorkey((0, 0, 0))
            final_images.append(menu_image)

        return final_images

    def update(self):
        self.center_rects()
        self.images = self.create_slot_images()
        self._animate()

        self.hover()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 0.1:
            self.image = self.images[self.index]
            self.index += 1
            if self.index >= 16:
                self.index = 0
            self.last_frame = time.time()
