## Spritesheet function module
import pygame

class SpriteSheet(object):
    def __init__(self, fileName, isHorizontal=True):
        self.spritesheet = pygame.image.load(fileName).convert()
        self.isHorizontal = isHorizontal

    def getImages(self, x, y, width, height, imageCount, imageOffset=0):
        """Snips specific sprites from the spritesheet
        
        Parameters
        ----------
            x (int): The x-location of the topleft corner of the image
        
            y (int): The y-location of the topleft corner of the image
        
            width (int): The width of each frame in the spritesheet
        
            height (int): The height of each frame in the spritesheet
        
            imageCount (int): The number of sprites in the spritesheet image
        
            imageOffset (int, optional): The sprite image to start the sequence from. Defaults to 0 - the first image.
        
        Returns
        -------
            list: The sequence of desired frames
        
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
    
def textureWall(sprite, texture):
    """Repeats a texture across the surface of a wall sprite.

    Args:
        sprite (pygame.sprite.Sprite): The sprite to repeat the texture over
        texture (pygame.Surface): The texture to repeat across the sprite
    """    
    image_width, image_height = sprite.image.get_size()
    tile_width, tile_height = texture.get_size()

    for x in range(0, image_width, tile_width):
        for y in range(0, image_height, tile_height):
            tile_rect = pygame.Rect(x, y, tile_width, tile_height)
            sprite.image.blit(texture, tile_rect)

    sprite.rect = sprite.image.get_rect()
    sprite.hitbox = sprite.rect