"""
Contains the ``TextBox`` class.
"""
import time

import pygame
from pygame.math import Vector2 as vec

import controls.key_trackers as kt
from controls.keybinds import *

from text import dialogue as dg
from text import fontinfo

import calculations as calc
import classbases as cb
import constants as cst
import visuals


# noinspection PyTypeChecker
class TextBox(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, convo: str):
        """A text box that can cycle through dialogue conversations.

        Args:
            pos_x: The x-position to spawn the text box
            pos_y: The y-position to spawn the text box
            convo: The dialogue sequence to initiate upon creation
        """
        super().__init__()
        self.layer = cst.LAYER['textbox']
        self.show(self.layer)

        self.pos = vec((pos_x, pos_y))
        self.last_release_value = kt.key_released[K_DIALOGUE]

        self.convo: dict = dg.all_dialogue_lines[convo]
        self.convo_index = 0
        self.char_index = 0

        self.text_top = vec(8, 8)  # Constant, the point where the first character is drawn
        self.text_cushion = vec(8, 8)

        self.is_generating = True
        self.last_generation = time.time()
        self.generation_count = 1
        self.last_char = ' '

        self.text_speed = 32
        self.text_color = (0, 0, 1)

        self.set_images('sprites/ui/textbox.png', 800, 128, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 800, 128, 800, 128)

    @staticmethod
    def style_character(char: pygame.Surface, style: str):
        if style == dg.RED:
            styled_char = calc.swap_color(char, (69, 40, 60), cst.RED)
        else:
            styled_char = char
        return styled_char

    def _render_text(self) -> None:
        """Draws the text onto the text box and handles the text box key inputs.

        Returns:
            None
        """
        if self.is_generating and self.generation_count <= len(self.convo[self.convo_index]):
            if calc.get_time_diff(self.last_generation) >= (1 / self.text_speed):
                # Drawing each letter onto the text box
                char = self.convo[self.convo_index][self.char_index]
                char_image = calc.text_to_image(char, fontinfo.dialogue_font)
                final_image = self.style_character(char_image, self.last_char)
                self.image = visuals.stack_images(
                    self.image, final_image, self.text_cushion.x, self.text_cushion.y
                )

                if char == ' ' or char not in dg.SKIP:  # Skips typing wait time if char is a special character
                    self.last_generation = time.time()

                # Shifting the following letter's position over
                self.char_index += 1
                self.generation_count += 1

                if char not in dg.SKIP:
                    self.text_cushion.x += fontinfo.dialogue_font.char_width - 10

                if char == '\n':
                    self.text_cushion.x = self.text_top.x
                    self.text_cushion.y += fontinfo.dialogue_font.char_height
                if self.text_cushion.x > self.image.get_width() - 16:
                    self.text_cushion.x = 8
                    self.text_cushion.y += fontinfo.dialogue_font.char_height

                if self.last_release_value != kt.key_released[K_DIALOGUE]:  # Prevents text skip mid-sentence
                    self.last_release_value = kt.key_released[K_DIALOGUE]

                self.last_char = char

        # Disabling text generation after all text is drawn
        if self.generation_count > len(self.convo[self.convo_index]):
            self.is_generating = False
            self.text_cushion = vec(8, 8)
            self.char_index = 0

            # Continues dialogue after input
            if self.last_release_value != kt.key_released[K_DIALOGUE]:
                self.generation_count = 1
                self.image = self.orig_image

                self.convo_index += 1
                # if there is no more dialogue, then the text box is closed.
                try:
                    len(self.convo[self.convo_index])
                except IndexError:
                    self.kill()

                self.is_generating = True
                self.last_release_value = kt.key_released[K_DIALOGUE]

    def update(self):
        self._render_text()


if __name__ == '__main__':
    test = TextBox(50, 50, 'test_text')
    print(test.convo)
