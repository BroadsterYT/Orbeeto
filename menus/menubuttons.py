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
