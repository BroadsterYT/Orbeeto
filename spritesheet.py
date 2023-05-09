## Spritesheet function module
import pygame

class SpriteSheet(object):
    def __init__(self, fileName, isHorizontal=True):
        """A ``pygame.Surface`` object that can be snipped from to create image sequences/animations.
        
        ### Parameters
            - ``fileName`` ``(_type_)``: _description_
            - ``isHorizontal`` ``(bool, optional)``: _description_. Defaults to True.
        """        
        self.spritesheet = pygame.image.load(fileName).convert()
        self.isHorizontal = isHorizontal

    def getImages(self, x, y, width, height, imageCount, imageOffset=0):
        """Returns a list of sprite images to utilize in static sprites or animations.
        
        ### Parameters
            - ``x`` ``(int)``: The x-position of the image to snip relative to
            - ``y`` ``(int)``: The y-position of the image to snip relative to
            - ``width`` ``(int)``: The width of each individual frame
            - ``height`` ``(int)``: The height of each individual frame
            - ``imageCount`` ``(int)``: The total number of images to snip
            - ``imageOffset`` ``(int, optional)``: The index of the frame to begin the snip from. Defaults to 0 (the first image).
        
        ### Returns
            - ``list``: A list of the desired sprite images
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
    """Tiles a sprite with a given texture.
    
    ### Parameters
        - ``sprite`` ``(pygame.sprite.Sprite)``: The sprite to tile with a texture
        - ``texture`` ``(pygame.Surface)``: The texture to tile the sprite with
    """    
    image_width, image_height = sprite.image.get_size()
    tile_width, tile_height = texture.get_size()

    for x in range(0, image_width, tile_width):
        for y in range(0, image_height, tile_height):
            tile_rect = pygame.Rect(x, y, tile_width, tile_height)
            sprite.image.blit(texture, tile_rect)

    sprite.rect = sprite.image.get_rect()
    sprite.hitbox = sprite.rect