"""
Module containing the Button class for menu usage.
"""
import math
import time

import pygame
from pygame.math import Vector2 as vec

import controls as ctrl
import text

import classbases as cb
import constants as cst


class MenuButton(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, width: int, height: int, name: str, func_call,
                 *args, **kwargs):
        """A button to be used in a menu with varying width and height, with customizable functionality.

        Args:
            pos_x: The x-position to place the button
            pos_y: The y-position to place the button
            width: The width of the button (in pixels)
            height: The height of the button (in pixels)
            name: The text to display on the button
            func_call: The function to call when the button is clicked.
        """
        super().__init__(cst.LAYER['ui_2'])
        self.show()

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

        Returns:
            None
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            scale = math.sin(time.time()) / 4
            self.image = pygame.transform.scale_by(self.border_image, 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.border_image
            self.rect = self.image.get_rect(center=self.rect.center)

    def check_for_click(self):
        if self.visible and self.last_release_value != ctrl.key_released[1]:
            if self.hitbox.collidepoint(pygame.mouse.get_pos()):
                self.func(*self.func_args, **self.func_kwargs)
                self.last_release_value = ctrl.key_released[1]
            else:
                self.last_release_value = ctrl.key_released[1]

    def update(self):
        self.check_for_click()
        self.hover()
