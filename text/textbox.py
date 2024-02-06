"""
Contains the ``TextBox`` class.
"""
import json
import time

import pygame
from pygame.math import Vector2 as vec

import controls.key_trackers as kt
from controls.keybinds import *

from text import fontinfo

import calculations as calc
import classbases as cb
import constants as cst

import visuals


# noinspection PyTypeChecker
class TextBox(cb.ActorBase):
    raw_dialogue: dict = json.load(open('text/dialogue.json', 'r'))

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

        self.convo: dict = self.raw_dialogue[convo]
        self.convo_index = 0  # This should always be referenced as a string when used as an index bc of json format
        self.char_index = 0
        self.text_cushion = vec(128, 8)

        self.is_generating = True
        self.last_generation = time.time()
        self.generation_count = 1

        self.text_speed = 32
        self.text_color = (0, 0, 1)

        self.set_images('sprites/ui/textbox.png', 800, 128, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 800, 128, 800, 128)

    def _render_text(self) -> None:
        """Draws the text onto the text box and handles the text box key inputs.

        Returns:
            None
        """
        if self.is_generating and self.generation_count <= len(self.convo[str(self.convo_index)]):
            if calc.get_time_diff(self.last_generation) >= (1 / self.text_speed):
                # Drawing each letter onto the text box
                text = self.convo[str(self.convo_index)][self.char_index]
                text_image = calc.text_to_image(text, fontinfo.dialogue_font)
                self.image = visuals.stack_images(self.image, text_image, self.text_cushion.x, self.text_cushion.y)

                # Shifting the following letter's position over
                self.char_index += 1
                self.generation_count += 1
                self.text_cushion.x += fontinfo.dialogue_font.char_width - 8
                if self.text_cushion.x > self.image.get_width() - 16:
                    self.text_cushion.x = 128
                    self.text_cushion.y += fontinfo.dialogue_font.char_height

                self.last_generation = time.time()
                if self.last_release_value != kt.key_released[K_DIALOGUE]:  # Prevents text skip mid-sentence
                    self.last_release_value = kt.key_released[K_DIALOGUE]

        # Disabling text generation after all text is drawn
        if self.generation_count > len(self.convo[str(self.convo_index)]):
            self.is_generating = False
            self.text_cushion = vec(128, 8)
            self.char_index = 0

            # Continues dialogue after input
            if self.last_release_value != kt.key_released[K_DIALOGUE]:
                self.generation_count = 1
                self.image = self.orig_image

                self.convo_index += 1
                # if there is no more dialogue, then the text box is closed.
                try:
                    len(self.convo[str(self.convo_index)])
                except KeyError:
                    self.kill()

                self.is_generating = True
                self.last_release_value = kt.key_released[K_DIALOGUE]

    def update(self):
        self._render_text()


if __name__ == '__main__':
    test = TextBox(50, 50, 'test_text')
    print(test.convo)
