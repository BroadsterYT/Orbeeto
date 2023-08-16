import pygame

from class_bases import *

class TileBase(ActorBase):
    def __init__(self, blockPosX: int, blockPosY: int, blockWidth: int, blockHeight: int, tileSize: int = 16):
        """The base class for all tile sprites
        
        ### Arguments
            - blockPosX (``int``): The x-position of the tile's topleft corner in the 45x80 tile grid
            - blockPosY (``int``): The y-position of the tile's topleft corner in the 45x80 tile grid
            - blockWidth (``int``): The width of the sprite (in tiles)
            - blockHeight (``int``): The height of the sprite (in tiles)
        """        
        super().__init__()
        self.tileSize = tileSize

        self.blockWidth, self.blockHeight = blockWidth, blockHeight
        self.width, self.height = self.blockWidth * self.tileSize, self.blockHeight * self.tileSize
        self.pos = getTopLeftCoords(self.width, self.height, blockPosX * self.tileSize, blockPosY * self.tileSize)

        room = self.getRoom()
        self.cAccel = room.player1.cAccel

    def tileTexture(self, blockWidth: int, blockHeight: int, texture: pygame.Surface, colorkey: ColorRGB) -> pygame.Surface:
        """Tiles a texture across an image
        
        ### Arguments
            - blockWidth (``int``): The width of the final image in "blocks"
            - blockHeight (``int``): The height of the final image in "blocks"
            - texture (``pygame.Surface``): The texture that should be repeated across the final image
            - colorkey (``tuple``): The color to set as the colorkey on the final image
        
        ### Returns
            - ``pygame.Surface``: The final image with the repeated texture
        """        
        finalImage = pygame.Surface(vec(blockWidth * 16, blockHeight * 16))

        imageWidth, imageHeight = finalImage.get_size()
        textureWidth, textureHeight = texture.get_size()

        for x in range(0, imageWidth, textureWidth):
            for y in range(0, imageHeight, textureHeight):
                tile_rect = pygame.Rect(x, y, textureWidth, textureHeight)
                finalImage.blit(texture, tile_rect)

        finalImage.set_colorkey(tuple(colorkey))
        return finalImage

    def movement(self):
        room = self.getRoom()
        self.cAccel = room.player1.cAccel

        if self.canUpdate:
            self.vel = room.vel
            self.velMovement(True)


class Wall(TileBase):
    def __init__(self, blockPosX: float, blockPosY: float, blockWidth: float, blockHeight: float):
        super().__init__(blockPosX, blockPosY, blockWidth, blockHeight)
        self.show(LAYER['wall'])
        all_walls.add(self) 

        self.texture = pygame.image.load("sprites/tiles/wall.png").convert()
        self.image: pygame.Surface = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, ColorRGB(25, 0, 0))

        self.setRects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        self.rect.center = self.pos
        self.hitbox.center = self.pos

class Floor(TileBase):
    def __init__(self, blockPosX: float, blockPosY: float, blockWidth: float, blockHeight: float):
        super().__init__(blockPosX, blockPosY, blockWidth, blockHeight)
        self.show(LAYER['floor'])
        all_floors.add(self)

        self.spritesheet = Spritesheet('sprites/tiles/floor.png', 4)
        self.textures = self.spritesheet.get_images(16, 16, 4)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, BLACK)

        self.setRects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)
    
    def update(self):
        if self.visible:
            if getTimeDiff(self.lastFrame) >= 0.235:
                self.texture = self.textures[self.index]
                self.image = self.tileTexture(self.blockWidth, self.blockHeight, self.texture, BLACK)

                self.index += 1
                if self.index > 3:
                    self.index = 0
                
                self.lastFrame = time.time()
