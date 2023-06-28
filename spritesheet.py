## Spritesheet function module
import pygame

class Spritesheet(object):
    def __init__(self, fileName, isHorizontal=True):
        """A ``pygame.Surface`` object that can be snipped from to create image sequences/animations.
        
        ### Parameters
            - ``fileName`` ``(_type_)``: _description_
            - ``isHorizontal`` ``(bool, optional)``: _description_. Defaults to True.
        """        
        self.spritesheet = pygame.image.load(fileName).convert()
        self.isHorizontal = isHorizontal

    def get_images(self, x: int, y: int, width: int, height: int, imageCount: int, imageOffset: int = 0):
        """Returns a list of sprite images to utilize in static sprites or animations.
        
        ### Parameters
            - x (``int``): The x-position of the image to snip relative to
            - y (``int``): The y-position of the image to snip relative to
            - width (``int``): The width of each individual frame
            - height (``int``): The height of each individual frame
            - imageCount (``int``): The total number of images to snip
            - imageOffset (``int``, optional): The index of the frame to begin the snip from. Defaults to ``0`` (the first image).
        
        ### Returns
            - ``_type_``: _description_
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