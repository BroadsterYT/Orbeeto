import pygame
from pygame.locals import *

import time

import calculations as calc
import classbases as cb
import constants as cst
import controls as ctrl

import dialogue
import fontinfo
import groups
import visuals

vec = pygame.math.Vector2


# noinspection PyTypeChecker
class TextBox(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, convo: int):
        """A text box that can cycle through dialogue conversations.

        Args:
            pos_x: The x-position to spawn the text box
            pos_y: The y-position to spawn the text box
            convo: The text_trees sequence to initiate upon creation
        """
        super().__init__()
        self.layer = cst.LAYER['textbox']
        self.show(self.layer)
        groups.all_text_boxes.add(self)

        self.pos = vec((pos_x, pos_y))
        self.last_release_value = ctrl.key_released[K_SPACE]

        self.convo = dialogue.text_trees[convo]
        self.convo_index = 0
        self.char_index = 0
        self.text_cushion = vec(128, 8)

        self.is_generating = True  # Is text currently being drawn onto the text box?
        self.last_generation = time.time()
        self.generation_count = 1

        self.text_speed = 20  # Number of characters to draw onto the text box per second
        self.text_color = (0, 0, 1)

        self.set_images('sprites/ui/textbox.png', 800, 128, 1, 1)
        self.set_rects(self.pos.x, self.pos.y, 800, 128, 800, 128)

    def _render_text(self) -> None:
        """Draws the text onto the text box and handles the text box key inputs.

        Returns:
            None
        """
        if (self.is_generating and
                calc.get_time_diff(self.last_generation) >= (1 / self.text_speed) and
                self.generation_count <= len(self.convo[self.convo_index])):
            # Drawing each letter onto the text box
            text = self.convo[self.convo_index][self.char_index]
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

        # Disabling text generation after all text is drawn
        if self.generation_count > len(self.convo[self.convo_index]):
            self.is_generating = False
            self.text_cushion = vec(128, 8)
            self.char_index = 0

            # Continues dialogue after input
            if self.last_release_value != ctrl.key_released[K_SPACE]:
                self.generation_count = 1
                self.image = self.orig_image

                self.convo_index += 1
                # if there is no more dialogue, then the text box is killed.
                try:
                    len(self.convo[self.convo_index])
                except KeyError:
                    self.close()

                self.is_generating = True
                self.last_release_value = ctrl.key_released[K_SPACE]

    def open(self):
        """Opens the dialogue box

        Returns:
            None
        """
        self.show(self)

    def close(self):
        """Closes the dialogue box

        Returns:
            None
        """
        self.hide()

    def update(self):
        if self.visible:
            self._render_text()
