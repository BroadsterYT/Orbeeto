import pygame
from pygame.math import Vector2 as vec


class Spritesheet:
    def __init__(self, file_name, sprites_per_row):
        """An object that handles sprite sheets and can extract frames and animations from them

        :param file_name: The file name of the sprite sheet to manipulate
        :param sprites_per_row: The amount of sprites in each row of the sprite sheet image file
        """
        self.spritesheet = pygame.image.load(file_name).convert()
        self.columns = sprites_per_row

    def get_images(self, width: int, height: int, image_count: int, image_offset: int = 0) -> list:
        """Returns the images of the spritesheet as a list of images.

        :param width: The width of each frame (in pixels)
        :param height: The height of each frame (in pixels)
        :param image_count: The number of images to "snip"
        :param image_offset: Which image should the "snip" start from? Defaults to the first image in the spritesheet.
        :return: A list of the desired images
        """
        image_list = []
        offset = vec(image_offset % self.columns, image_offset // self.columns)
        for i in range(0, image_count):
            if offset.x >= self.columns:
                offset.x = 0
                offset.y += 1
            image = pygame.Surface(vec(width, height))
            image.blit(self.spritesheet, vec(0, 0), (offset.x * width, offset.y * height, width, height))
            image.set_colorkey((0, 0, 0))
            image_list.append(image)
            offset.x += 1

        return image_list
