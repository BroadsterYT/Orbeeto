## Spritesheet function module
import pygame

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
            height (int): The height of each frame of the sprites in the spritesheet
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