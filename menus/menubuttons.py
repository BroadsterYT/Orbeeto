"""
Module containing the Button class for menu usage.
"""
import math
import os
import time

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import text

import calc
import classbases as cb
import constants as cst
import gamestack as gs
import spritesheet


class MenuButton(cb.ActorBase):
    def __init__(self, gamestate: gs.GameState, pos_x: float, pos_y: float, width: int, height: int, name: str, func_call,
                 *args, **kwargs):
        """A button to be used in a menu with varying width and height, with customizable functionality.

        :param pos_x: The x-position to place the button
        :param pos_y: The y-position to place the button
        :param width: The width of the button (in pixels)
        :param height: The height of the button (in pixels)
        :param name: The text to display on the button
        :param func_call: The function to call when the button is clicked
        :param args: The arguments to use in the function being called
        :param kwargs: The keyword arguments to use in the function being called
        """
        super().__init__(cst.LAYER['ui_2'], gamestate)
        self.add_to_gamestate()

        self.func = func_call
        self.func_args = args
        self.func_kwargs = kwargs

        self.last_release_value = ctrl.key_released[1]
        self.pos = vec(pos_x, pos_y)

        # Building image
        self.name = text.text_to_image(name, text.dialogue_font)
        self.border_image = pygame.Surface(vec(width, height))
        self.border_image.fill((100, 100, 100))
        self.border_image.blit(self.name, vec(0, 0))
        self.image = self.border_image

        self.set_rects(self.pos.x, self.pos.y, width, height, width, height)

    def hover(self) -> None:
        """Causes the button to oscillate in size when the mouse cursor hovers over it

        :return: None
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            scale = math.sin(time.time()) / 4
            self.image = pygame.transform.scale_by(self.border_image, 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.border_image
            self.rect = self.image.get_rect(center=self.rect.center)

    def check_for_click(self) -> None:
        """Checks if the mouse is clicking the button. If so, the button's designated function will be called.

        :return: None
        """
        if (self.last_release_value == ctrl.key_released[1] - 1 and self.hitbox.collidepoint(pygame.mouse.get_pos())
                and ctrl.last_click_pos[1] == self.gamestate and ctrl.last_release_pos[1] == self.gamestate):
            self.func(*self.func_args, **self.func_kwargs)
            self.last_release_value = ctrl.key_released[1]
        else:
            self.last_release_value = ctrl.key_released[1]

    def update(self):
        self.check_for_click()
        self.hover()


class ScrollWidget(cb.ActorBase):
    def __init__(self, gamestate: gs.GameState, pos_x, pos_y, vis_width: int, vis_height, entry_height: int):
        """A scroll widget that allows the display of items, settings, checkboxes, and more.

        :param gamestate: The gamestate the object should exist within
        :param pos_x: The x-axis position to spawn the widget
        :param pos_y: The y-axis position to spawn the widget
        :param entry_height: The height of each entry added into the widget
        """
        super().__init__(cst.LAYER['ui_2'], gamestate)
        self.add_to_gamestate()
        self.entries = []
        self.width = vis_width
        self.height = vis_height
        self.entry_height = entry_height

        self.pos = vec(pos_x, pos_y)
        self.start_pos = vec(pos_x, pos_y)

        self.last_scroll_up, self.last_scroll_down = ctrl.key_released[4], ctrl.key_released[5]
        self.scroll_value = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 255))

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def add_entry(self, *actors) -> None:
        """Adds an actor or list of actors to the entry list"""
        for actor in actors:
            self.entries.append(actor)

    def remove_entry(self, actor) -> None:
        """Removes an actor from the entry list."""
        self.entries.remove(actor)

    def update(self):
        if self.last_scroll_up != ctrl.key_released[4]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.scroll_value -= 15
            # VVV Prevents widget from scrolling up beyond the last visible entry VVV
            if len(self.entries) > 1 and self.scroll_value < -self.entry_height * (len(self.entries) - 2):
                self.scroll_value = -self.entry_height * (len(self.entries) - 2)
            elif len(self.entries) <= 1 and self.scroll_value < -self.entry_height * (len(self.entries) - 1):
                self.scroll_value = -self.entry_height * (len(self.entries) - 1)

            self.last_scroll_up = ctrl.key_released[4]

        if self.last_scroll_down != ctrl.key_released[5]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.scroll_value += 15
            if self.scroll_value > 0:
                self.scroll_value = 0  # Prevents scrolling down past the first entry
            self.last_scroll_down = ctrl.key_released[5]


class ScrollPullTab(cb.ActorBase):
    def __init__(self, gamestate, owner: ScrollWidget):
        """A pull tab used on a scroll widget to allow scrolling by dragging

        :param gamestate: The gamestate the object should exist within
        :param owner: The scroll widget the pull tab belongs to
        """
        super().__init__(cst.LAYER['ui_2'], gamestate)
        self.add_to_gamestate()
        self.owner = owner


class ScrollWidgetEntry(cb.ActorBase):
    def __init__(self,
                 owner: ScrollWidget,
                 color: tuple,
                 scroll_pos: int,
                 entry_text: str,
                 image_path: None | str = None,
                 sprites_per_row: int = 8,
                 sprite_width: int = 64,
                 sprite_height: int = 64,
                 sprite_count: int = 1,
                 sprite_offset: int = 0,
                 entry_type: int = 0):
        """An entry within a scroll widget

        :param owner: The scroll widget the entry belongs to
        :param scroll_pos: The position at which the entry should be displayed in the widget. Higher values will be
        placed lower in the widget.
        :param entry_text: The text to display within the entry
        :param image_path: The path to use for the image to display in the entry. Defaults to None.
        :param sprites_per_row: The number of sprites in each row of the given spritesheet
        :param sprite_width: The width of each sprite in the given spritesheet
        :param sprite_height: The height of each sprite in the given spritesheet
        :param sprite_count: The number of sprites to pull from the spritesheet
        :param sprite_offset: Which sprite should the "snip" start from? Defaults to the first image in the spritesheet.
        :param entry_type: The interaction type for the entry. 0 for visual, 1 for numeric display, 2 for boolean
        display. Defaults to 0.
        """
        super().__init__(cst.LAYER['ui_2'], owner.gamestate)
        self.add_to_gamestate()
        self.owner = owner
        self.width, self.height = self.owner.width - 64, self.owner.entry_height

        self.pos = vec(self.owner.pos.x, self.owner.pos.y - self.owner.height // 2 + self.owner.entry_height)
        self.start_pos = self.owner.start_pos

        self.scroll_pos = scroll_pos

        self.entry_text = entry_text
        self.entry_type = entry_type

        # --- Get base entry image(s) --- #
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)

        # ------------------------------- #

        if image_path is not None:
            self.display_sheet = spritesheet.Spritesheet(image_path, sprites_per_row)
            self.display_images = self.display_sheet.get_images(sprite_width,
                                                                sprite_height,
                                                                sprite_count,
                                                                sprite_offset)
        else:
            pass

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        # VVV The position of an entry that is flush with the top lip of the widget border cover
        flush_top = self.owner.pos.y - self.owner.height // 2 + self.height // 2 + self.owner.entry_height
        self.pos.y = self.scroll_pos + self.owner.scroll_value + flush_top
        if self.pos.y < flush_top - self.owner.entry_height:
            self.pos.y = flush_top - self.owner.entry_height

        if self.pos.y > self.owner.pos.y + self.owner.height // 2 - self.height // 2:
            self.pos.y = self.owner.pos.y + self.owner.height // 2 - self.height // 2

        self.center_rects()

    def __repr__(self):
        return f'ScrollWidgetEntry({self.pos}, {self.scroll_pos})'


class MenuArrow(cb.ActorBase):
    def __init__(self, gamestate: gs.GameState, pos_x: float, pos_y: float, direction: str, func_call, *args, **kwargs):
        """An arrow that can be clicked to call any function

        :param gamestate: The gamestate the arrow should appear in
        :param pos_x: The x-axis position to create the arrow at
        :param pos_y: The y-axis position to create the arrow at
        :param direction: The direction the arrow should point
        :param func_call: The function to call when the arrow is clicked
        :param args: The arguments to use in the function being called
        :param kwargs: The keyword arguments to use in the function being called
        """
        super().__init__(cst.LAYER['ui_1'], gamestate)
        self.add_to_gamestate()

        self.func = func_call
        self.func_args = args
        self.func_kwargs = kwargs

        self.last_release_value = ctrl.key_released[1]
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/ui/menu_arrow.png'), 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.dir = direction
        if self.dir == cst.EAST:
            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
        elif self.dir == cst.WEST:
            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)

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

    def check_for_click(self) -> None:
        """Checks if the mouse is clicking the button. If so, the button's designated function will be called.

        :return: None
        """
        if self.last_release_value == ctrl.key_released[1] - 1 and self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.func(*self.func_args, **self.func_kwargs)
            self.last_release_value = ctrl.key_released[1]
        else:
            self.last_release_value = ctrl.key_released[1]

    def update(self):
        self._animate()
        self.hover()
        self.check_for_click()

    def _animate(self):
        if calc.get_time_diff(self.last_frame) > cst.SPF:
            if self.index > 60:
                self.index = 1

            if self.dir == cst.EAST:
                self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            elif self.dir == cst.WEST:
                self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True,
                                                   False)

            self.index += 1
            self.last_frame = time.time()


if __name__ == '__main__':
    pass
