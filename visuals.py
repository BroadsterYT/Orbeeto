import pygame
import math

import classbases as cb
import constants as cst
import calculations as calc

import spritesheet

vec = pygame.math.Vector2
rad = math.radians


def stack_images(base_image: pygame.Surface, top_image: pygame.Surface, stack_x: int, stack_y: int) -> pygame.Surface:
    """Places an image overtop another image, then returns the new image

    Args:
        base_image: The image being covered over
        top_image: The image being placed on top of the base image
        stack_x: The x-position to put the top image over the base image (top left corner)
        stack_y: The y-position to put the top image over the base image (top left corner)

    Returns:
        pygame.Surface: The resulting image
    """
    output_image = pygame.Surface(vec(base_image.get_width(), base_image.get_height()))
    output_image.blit(base_image, vec(0, 0))
    output_image.blit(top_image, vec(stack_x, stack_y))

    return output_image


class Beam(cb.ActorBase):
    def __init__(self, from_sprite, to_sprite):
        super().__init__()
        self.layer = cst.LAYER['floor']
        self.show(self.layer)

        self.fromSprite, self.toSprite = from_sprite, to_sprite
        self.index = 0
        
        self.length = calc.get_dist(self.fromSprite.pos, self.toSprite.pos)
        self.angle = calc.get_angle(self.fromSprite, self.toSprite)
        self.image = pygame.Surface(vec(1, 1))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def build_setup(self, start_pos: pygame.math.Vector2, end_pos: pygame.math.Vector2):
        self.length = calc.get_dist(start_pos, end_pos)
        self.angle = calc.get_angle(self.fromSprite, self.toSprite)

        opp = (self.length / 2) * math.cos(rad(self.angle + 90))
        adj = (self.length / 2) * math.sin(rad(self.angle + 90))

        self.pos = vec(self.fromSprite.pos.x + opp, self.fromSprite.pos.y - adj)

    def build_image(self, frame_offset: int) -> None:
        """Builds the image of the beam.
        
        ### Arguments
            - frameOffset (``int``): The frame from "beams.png" to build the beam from
        """        
        self.spritesheet = spritesheet.Spritesheet("sprites/textures/beams.png", 1)
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
        self.build_setup(self.fromSprite.pos, self.toSprite.pos)
        self.build_image(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
