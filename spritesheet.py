## Spritesheet function module

import pygame
import constants as cst

class SpriteSheet(object):
    def __init__(self, fileName, isHorizontal=True):
        self.spritesheet = pygame.image.load(fileName).convert()
        self.isHorizontal = isHorizontal

    def getImages(self, x, y, width, height, imageCount, imageOffset=0):
        """Snips specific sprites from a spritesheet

        Args:
            x (int): The x-location of the topleft corner of the sprite
            y (int): The x-location of the topleft corner of the sprite
            width (int): The width of each frame of the sprites in the spritesheet
            height (int): The width of each frame of the sprites in the spritesheet
            imageCount (_type_): _description_
            imageOffset (int, optional): _description_. Defaults to 0.

        Returns:
            list: A list of the desired sprites/sprite animation
        """        
        imageList = []
        offset = 0
        if self.isHorizontal == True:
            for i in range (0, imageCount):
                image = pygame.Surface([width, height]).convert()
                image.blit(self.spritesheet, (0, 0), (x + (imageOffset * width) + offset, y, width, height))
                image.set_colorkey((0, 0, 0))
                imageList.append(image)
                offset += width
        else:
            for i in range (0, imageCount):
                image = pygame.Surface([width, height]).convert()
                image.blit(self.spritesheet, (0, 0), (x, y + (imageOffset * height) + offset, width, height))
                image.set_colorkey((0, 0, 0))
                imageList.append(image)
                offset += height
        
        return imageList