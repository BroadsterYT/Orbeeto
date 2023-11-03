import pygame
from constants import vec


class Spritesheet(object):
    def __init__(self, file_name, sprites_per_row):
        self.spritesheet = pygame.image.load(file_name).convert()
        self.columns = sprites_per_row

    def get_images(self, width: int, height: int, image_count: int, image_offset: int = 0) -> list:
        """Returns the images of the spritesheet as a list of images.

        Args:
            width: The width of each frame (in pixels)
            height: The height of each frame (in pixels)
            image_count: The number of images to "snip"
            image_offset: Which image should the "snip" start from? Defaults to the first image in the spritesheet.

        Returns:
            list: A list of the desired images
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
