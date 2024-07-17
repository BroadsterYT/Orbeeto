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
        self.show()
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
    current_clicked = None

    def __init__(self, owner, pos_x: float, pos_y: float, gear_name: str, gear_type: str):
        """An inventory slot that represents a gun, piece of armor, or articles that can be equipped by the player.

        :param owner: The inventory object the slot belongs to
        :param pos_x: The x-axis position to spawn the gear slot
        :param pos_y: The y-axis position to spawn the gear slot
        :param gear_name: The name of the gear the slot is representing
        :param gear_type: The type of gear the slot represents. (``armor`` for armor, ``l_gun`` for left gun, ``r_gun``
        for right gun, and ``article`` for articles)
        """
        super().__init__(gs.s_inventory, owner, pos_x, pos_y)
        self.show()

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

    def _get_gear_images(self) -> list[pygame.Surface]:
        if self.holding == items.ARMOR[0]:
            return self.gear_sheet.get_images(64, 64, 16, 0)
        elif self.holding == items.ARMOR[1]:
            return self.gear_sheet.get_images(64, 64, 16, 16)
        elif self.holding == items.ARMOR[2]:
            return self.gear_sheet.get_images(64, 64, 16, 32)

    def create_slot_images(self) -> list[pygame.Surface]:
        final_images = []
        gear_images = self._get_gear_images()
        for frame in gear_images:
            menu_image = visuals.stack_images(self.menu_image, frame, 0, 0)
            menu_image.set_colorkey((0, 0, 0))
            final_images.append(menu_image)
        return final_images

    def drag(self) -> None:
        if self.holding_type == 'armor':
            if (self.hitbox.collidepoint(pygame.mouse.get_pos()) and ctrl.is_input_held[1]
                    and (GearSlot.current_clicked is self or GearSlot.current_clicked is None)
                    and self.owner.owner.my_armors[self.holding]):
                GearSlot.current_clicked = self

            elif (self.hitbox.collidepoint(pygame.mouse.get_pos()) and not ctrl.is_input_held[1]
                  and GearSlot.current_clicked is not None):
                if self.hitbox.colliderect(self.owner.armor_select.hitbox):
                    # Returns slot that is being replaced back to correct position
                    for slot in [s for s in groups.all_armor_slots if s != GearSlot.current_clicked]:
                        slot.pos = slot.screen_pos
                    self.owner.armor_select.equipped = GearSlot.current_clicked
                    GearSlot.current_clicked.pos = self.owner.armor_select.pos
                else:
                    # Checking if equip slot is empty
                    empty_check = True
                    for slot in groups.all_armor_slots:
                        if slot.hitbox.colliderect(self.owner.armor_select.hitbox):
                            empty_check = False
                    if empty_check:
                        self.owner.armor_select.equipped = None
                    # ----------------------------- #
                    GearSlot.current_clicked.pos = GearSlot.current_clicked.screen_pos
                GearSlot.current_clicked = None
        elif self.holding_type == 'l_gun':
            pass
        elif self.holding_type == 'r_gun':
            pass
        elif self.holding_type == 'article':
            pass

        if GearSlot.current_clicked is self:
            self.pos = vec(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            gs.s_inventory.all_sprites.change_layer(self, cst.LAYER['ui_1'] + 1)
        else:
            gs.s_inventory.all_sprites.change_layer(self, cst.LAYER['ui_1'])

    def update(self):
        self.center_rects()
        self.drag()
        self.hover()


class ArmorSlot(SlotBase):
    current_clicked = None

    def __init__(self, owner, pos_x, pos_y, armor_held: str):
        super().__init__(gs.s_inventory, owner, pos_x, pos_y)
        self.show()
        groups.all_armor_slots.add(self)

        self.screen_pos = vec(pos_x % cst.WINWIDTH, pos_y)

        self.holding = armor_held
        self.armor_sheet = spritesheet.Spritesheet('sprites/textures/armor_items.png', 16)
        self.images = self.create_slot_images()
        self.image = self.images[self.index]

        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def _get_armor_images(self) -> list:
        if self.holding == items.ARMOR[0]:
            return self.armor_sheet.get_images(64, 64, 16, 0)
        elif self.holding == items.ARMOR[1]:
            return self.armor_sheet.get_images(64, 64, 16, 16)
        elif self.holding == items.ARMOR[2]:
            return self.armor_sheet.get_images(64, 64, 16, 32)
        else:
            raise IndexError(f'No armor visual exists with an armor key of {self.holding}.')

    def create_slot_images(self) -> list[pygame.Surface]:
        """Combines the image(s) of the item and the image of the menu slot, returning a list of the final combined
        images.

        :return: A list of the combined images
        """
        final_images = []
        armor_images = self._get_armor_images()

        for frame in armor_images:
            menu_image = visuals.stack_images(self.menu_image, frame, 0, 0)
            menu_image.set_colorkey((0, 0, 0))
            final_images.append(menu_image)

        return final_images

    def drag(self) -> None:
        """Allows the slot to be dragged by the mouse when called once every frame

        :return: None
        """
        if (self.hitbox.collidepoint(pygame.mouse.get_pos()) and ctrl.is_input_held[1]
                and (ArmorSlot.current_clicked is self or ArmorSlot.current_clicked is None)
                and self.owner.owner.my_armors[self.holding]):
            ArmorSlot.current_clicked = self

        elif (self.hitbox.collidepoint(pygame.mouse.get_pos()) and not ctrl.is_input_held[1]
              and ArmorSlot.current_clicked is not None):
            if self.hitbox.colliderect(self.owner.armor_select.hitbox):
                # Returns slot that is being replaced back to correct position
                for slot in [s for s in groups.all_armor_slots if s != ArmorSlot.current_clicked]:
                    slot.pos = slot.screen_pos
                self.owner.armor_select.equipped = ArmorSlot.current_clicked
                ArmorSlot.current_clicked.pos = self.owner.armor_select.pos
            else:
                # Checking if equip slot is empty
                empty_check = True
                for slot in groups.all_armor_slots:
                    if slot.hitbox.colliderect(self.owner.armor_select.hitbox):
                        empty_check = False
                if empty_check:
                    self.owner.armor_select.equipped = None
                # ----------------------------- #
                ArmorSlot.current_clicked.pos = ArmorSlot.current_clicked.screen_pos
            ArmorSlot.current_clicked = None

        if ArmorSlot.current_clicked is self:
            self.pos = vec(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            gs.s_inventory.all_sprites.change_layer(self, cst.LAYER['ui_1'] + 1)
        else:
            gs.s_inventory.all_sprites.change_layer(self, cst.LAYER['ui_1'])

    def update(self):
        self.center_rects()
        self.images = self.create_slot_images()
        self._animate()

        self.hover()
        self.drag()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > 0.1:
            self.image = self.images[self.index]
            self.index += 1
            if self.index >= 16:
                self.index = 0
            self.last_frame = time.time()

    def __repr__(self):
        return f'ArmorSlot({self.holding}, {self.pos}, {self.start_pos}, {self.screen_pos})'


class SelectionSlotA(SlotBase):
    def __init__(self, owner, pos_x, pos_y):
        super().__init__(gs.s_inventory, owner, pos_x, pos_y)
        self.show()
        groups.all_material_slots.add(self)

        self.set_images('sprites/ui/menu_item_slot.png', 64, 64, 3, 1, 1)
        self.set_rects(0, 0, 64, 64, 64, 64)

        self.equipped = None

    def update(self):
        self.center_rects()
