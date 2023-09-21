## Spritesheet function module
import pygame
from constants import vec
    
class Spritesheet(object):
    def __init__(self, fileName, spritesPerRow):
        self.spritesheet = pygame.image.load(fileName).convert()
        self.columns = spritesPerRow

    def getImages(self, width: int, height: int, imageCount: int, imageOffset: int = 0) -> list:
        """Returns the images of the spritesheet as a list.
        
        ### Arguments
            - width (``int``): The width of each frame
            - height (``int``): The height of each frame
            - imageCount (``int``): The number of images to "snip"
            - imageOffset (``int``, optional): Which image should the "snip" start from? Defaults to ``0`` (the first image in the spritesheet).
        
        ### Returns
            - ``list``: A list of the desired images
        """        
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

