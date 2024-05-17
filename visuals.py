import math
import os

import pygame
from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import calc
import spritesheet


def stack_images(base_image: pygame.Surface, top_image: pygame.Surface, stack_x: int, stack_y: int) -> pygame.Surface:
    """Places an image overtop another image, then returns the new image

    :param base_image: The image being covered over
    :param top_image: The image being placed on top of the base image
    :param stack_x: The x-position to put the top image over the base image (0 -> align left sides)
    :param stack_y: The y-position to put the top image over the base image (0 -> align top edges)
    :return: The stacked image
    """
    output_image = pygame.Surface(vec(base_image.get_width(), base_image.get_height()))
    output_image.blit(base_image, vec(0, 0))
    output_image.blit(top_image, vec(stack_x, stack_y))
    return output_image


class Beam(cb.ActorBase):
    def __init__(self, from_sprite, to_sprite):
        super().__init__(cst.LAYER['floor'])
        self.show()

        self.from_sprite, self.to_sprite = from_sprite, to_sprite
        self.index = 0
        
        self.length = calc.get_dist(self.from_sprite.pos, self.to_sprite.pos)
        self.angle = calc.get_angle(self.from_sprite, self.to_sprite)
        self.image = pygame.Surface(vec(1, 1))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def build_setup(self, start_pos: pygame.math.Vector2, end_pos: pygame.math.Vector2) -> None:
        self.length = calc.get_dist(start_pos, end_pos)
        self.angle = calc.get_angle(self.from_sprite, self.to_sprite)

        opp = (self.length / 2) * math.cos(math.radians(self.angle + 90))
        adj = (self.length / 2) * math.sin(math.radians(self.angle + 90))

        self.pos = vec(self.from_sprite.pos.x + opp, self.from_sprite.pos.y - adj)

    def build_image(self, frame_offset: int) -> None:
        """Builds the image of the beam.
        
        ### Arguments
            - frameOffset (``int``): The frame from "beams.png" to build the beam from
        """        
        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/textures/beams.png'), 1)
        base_images = self.spritesheet.get_images(12, 12, 1, frame_offset)
        base_image: pygame.Surface = base_images[self.index]

        final_image = pygame.Surface(vec(base_image.get_width(), int(self.length)))

        offset = 0
        for i in range(int(self.length / base_image.get_height())):
            final_image.blit(base_image, vec(0, offset))
            offset += base_image.get_height()

        final_image.set_colorkey(cst.BLACK)
        self.image = pygame.transform.rotate(final_image, self.angle)

    def update(self):
        self.build_setup(self.from_sprite.pos, self.to_sprite.pos)
        self.build_image(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
