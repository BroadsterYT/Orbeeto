import pygame
from pygame.math import Vector2 as vec


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
