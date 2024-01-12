import pygame
from pygame.locals import *
import time
import math

import classbases as cb
import controls
from spritesheet import Spritesheet
import groups
import constants as cst
import calculations as calc

vec = pygame.math.Vector2


class InventoryMenu(cb.AbstractBase):
    def __init__(self, owner):
        """A menu used to view collected items and utilize them for various purposes

        Args:
            owner: The player whom the inventory belongs to
        """
        super().__init__()
        self.cyclingLeft = False
        self.cyclingRight = False

        self.owner = owner

        self.wipeTime = 1
        self.window = 0

        self.lastCycle = time.time()

        self.rightArrow = RightMenuArrow(cst.WINWIDTH - 64, cst.WINHEIGHT / 2)
        self.leftArrow = LeftMenuArrow(64, cst.WINHEIGHT / 2)

        self.add(
            self.build_inventory_slots()
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
            groups.all_sprites.add(sprite, layer=cst.LAYER['ui_1'])

    def cycle_menu(self):
        if (not self.cyclingLeft and
                not self.cyclingRight and
                not self.canUpdate):
            if controls.is_input_held[1] and self.leftArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window -= 1
                self.lastCycle = time.time()
                self.cyclingLeft = True

            if controls.is_input_held[1] and self.rightArrow.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.window += 1
                self.lastCycle = time.time()
                self.cyclingRight = True

        # Cycling left
        if self.cyclingLeft and not self.cyclingRight:
            weight = calc.get_time_diff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.startPos.x, sprite.startPos.x - cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.startPos.x = sprite.pos.x
                self.cyclingLeft = False

        # Cycling right
        if not self.cyclingLeft and self.cyclingRight:
            weight = calc.get_time_diff(self.lastCycle)
            if weight <= 1:
                for sprite in self.sprites():
                    sprite.pos.x = calc.cerp(sprite.startPos.x, sprite.startPos.x + cst.WINWIDTH, weight)
            else:
                for sprite in self.sprites():
                    sprite.startPos.x = sprite.pos.x
                self.cyclingRight = False

    def build_inventory_slots(self) -> list:
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
        if controls.key_released[K_e] % 2 != 0 and controls.key_released[K_e] > 0:
            self.show()
            self.rightArrow.show(cst.LAYER['ui_1'])
            self.leftArrow.show(cst.LAYER['ui_1'])

            self.canUpdate = False
            for sprite in groups.all_sprites:
                sprite.canUpdate = False

        elif controls.key_released[K_e] % 2 == 0 and controls.key_released[K_e] > 0:
            self.hide()
            self.rightArrow.hide()
            self.leftArrow.hide()

            self.canUpdate = True
            for sprite in groups.all_sprites:
                sprite.canUpdate = True

        self.cycle_menu()


class RightMenuArrow(cb.ActorBase):
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
            self.pos.x = 5 * math.sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        self.__animate()
        self.hover()

    def __animate(self):
        if calc.get_time_diff(self.lastFrame) > cst.SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            self.index += 1
            self.lastFrame = time.time()


class LeftMenuArrow(cb.ActorBase):
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
            self.pos.x = 5 * math.sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        if calc.get_time_diff(self.lastFrame) >= cst.SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)
            self.index += 1
            self.lastFrame = time.time()

        self.hover()


class MenuSlot(cb.ActorBase):
    def __init__(self, owner, pos_x: float, pos_y: float, item_held: str | None):
        """A menu slot that shows the collected amount of a specific item.

        Args:
            owner: The owner of the inventory to whom the menu slot belongs to
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
            item_held: The item the menu slot will hold. Items are chosen from MATERIALS dictionary.
        """
        super().__init__()
        groups.all_slots.add(self)
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
            scale = abs(math.sin(s_time)) / 2
            self.image = pygame.transform.scale_by(self.images[self.index], 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_item_images(self) -> list:
        if self.holding == cst.MAT[0]:
            return self.itemSheet.get_images(32, 32, 1, 0)
        elif self.holding == cst.MAT[1]:
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
                new_img = calc.combine_images(self.menuImg, frame)

                # Adding the count of the item to its images
                count_surface = calc.text_to_image(str(self.count), 'sprites/ui/font.png', 9, 14, 36)
                new_img.set_colorkey((0, 0, 0))
                center_x = (new_img.get_width() - frame.get_width()) // 2
                center_y = (new_img.get_height() - frame.get_height()) // 2

                # Changing dark gray to light gray
                color_swap_1 = calc.swap_color(count_surface, (44, 44, 44), (156, 156, 156))
                # Changing black to white
                color_swap_2 = calc.swap_color(color_swap_1, (0, 0, 1), (255, 255, 255))

                new_img.blit(color_swap_2, vec(center_x, center_y))
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
