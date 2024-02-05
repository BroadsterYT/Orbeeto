"""
Contains all text classes that appear on-screen, as well as all on-screen text operations.
"""

import pygame
import time

from text import fontinfo

import classbases as cb
import constants as cst
import calculations as calc

import groups
import screen

vec = pygame.math.Vector2


def draw_text(text: str, pos_x, pos_y):
    font = pygame.font.SysFont('Arial', 24)
    image = font.render(text, True, (0, 0, 0))
    screen.buffer_screen.blit(image, vec(pos_x, pos_y))


class IndicatorText(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, text, duration=0.6):
        """A number that pops up after a player or enemy is hit that indicates how much damage that entity has taken.

        Args:
            pos_x: The x-position to spawn
            pos_y: The y-position to spawn
            text: The text to display
            duration: The amount of time (in seconds) for the text to last for
        """
        super().__init__()
        self.layer = cst.LAYER['text']
        self.show(self.layer)
        groups.all_font_chars.add(self)
        
        self.start = time.time()
        self.pos = vec((pos_x, pos_y))

        self.duration = duration

        self.image = calc.text_to_image(str(text), fontinfo.font1)
        self.set_rects(self.pos.x, self.pos.y, 9, 14, 9, 14)

    def get_accel(self):
        final_accel = vec(0, 0)
        room = cb.get_room()
        final_accel += room.get_accel()
        if calc.get_time_diff(self.start) < 0.1:
            final_accel.y -= 1

        return final_accel

    def movement(self):
        self.accel = self.get_accel()
        self.accel_movement()

    def update(self):
        self.movement()
        if calc.get_time_diff(self.start) > self.duration:
            self.kill()
