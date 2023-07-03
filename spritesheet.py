## Spritesheet function module
import pygame
from constants import vec
    
class Spritesheet(object):
    def __init__(self, fileName, spritesPerRow):
        self.spritesheet = pygame.image.load(fileName).convert()
        self.columns = spritesPerRow

    def get_images(self, width: int, height: int, imageCount: int, imageOffset: int = 0):
        imageList = []
        offset = vec(imageOffset % self.columns, imageOffset // self.columns)
        for i in range(0, imageCount):
            if offset.x >= self.columns:
                offset.x = 0
                offset.y += 1
            image = pygame.Surface(vec(width, height))
            image.blit(self.spritesheet, vec(0, 0), (offset.x * width, offset.y * height, width, height))
            image.set_colorkey((0, 0, 0))
            imageList.append(image)
            offset.x += 1

        return imageList

