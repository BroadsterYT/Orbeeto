from class_bases import *


def fancy_tile_texture(block_width: int, block_height: int, textures: list, color_key: ColorRGB, style: int):
    final_image = pygame.Surface(vec(block_width * 16, block_height * 16))

    image_width, image_height = final_image.get_size()
    texture_width, texture_height = 16, 16

    # No borders
    if style == 0:
        for x in range(0, image_width, texture_width):
            for y in range(0, image_height, texture_height):
                tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                final_image.blit(textures[0], tile_rect)

    # Bottom and right
    elif style == 1:
        for x in range(0, image_width, texture_width):
            for y in range(0, image_height, texture_height):
                if x == image_width - texture_width or y == image_height - texture_height:
                    tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                    final_image.blit(textures[1], tile_rect)
                else:
                    tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                    final_image.blit(textures[0], tile_rect)

    # Top and right
    elif style == 2:
        for x in range(0, image_width, texture_width):
            for y in range(0, image_height, texture_height):
                if x == image_width - texture_width or y == 0:
                    tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                    final_image.blit(textures[1], tile_rect)
                else:
                    tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                    final_image.blit(textures[0], tile_rect)

    # Rest of styles

    final_image.set_colorkey(tuple(color_key))
    return final_image


class TileBase(ActorBase):
    def __init__(self, block_pos_x: int | float, block_pos_y: int | float, block_width: int, block_height: int,
                 tile_size: int = 16):
        """The base class for all tile sprites.

        Args:
            block_pos_x: The x-axis position of the tile (in tiles)
            block_pos_y: The y-axis position of the tile (in tiles)
            block_width: The width of the tile (in tiles)
            block_height: The height of the tile (in tiles)
            tile_size: The size of each individual tile (in pixels)
        """
        super().__init__()
        self.tileSize = tile_size

        self.blockWidth, self.blockHeight = block_width, block_height
        self.width, self.height = self.blockWidth * self.tileSize, self.blockHeight * self.tileSize
        self.pos = get_top_left_coords(self.width, self.height, block_pos_x * self.tileSize,
                                       block_pos_y * self.tileSize)

        self.cAccel = 0.58

    def movement(self):
        if self.canUpdate:
            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()
        return final_accel


class Wall(TileBase):
    def __init__(self, block_pos_x: float, block_pos_y: float, block_width: int, block_height: int,
                 image_row: int = 0, style: int = 0):
        super().__init__(block_pos_x, block_pos_y, block_width, block_height)
        self.show(LAYER['wall'])
        all_walls.add(self)

        self.spritesheet = Spritesheet('sprites/tiles/wall.png', 16)
        self.textures = self.spritesheet.get_images(16, 16, 16, image_row * 16)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image: pygame.Surface = fancy_tile_texture(self.blockWidth, self.blockHeight,
                                                        self.textures, BLACK, style)

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        pass


class Floor(TileBase):
    def __init__(self, block_pos_x: int | float, block_pos_y: int | float, block_width: int, block_height: int):
        super().__init__(block_pos_x, block_pos_y, block_width, block_height)
        self.show(LAYER['floor'])
        all_floors.add(self)

        self.spritesheet = Spritesheet('sprites/tiles/floor.png', 4)
        self.textures = self.spritesheet.get_images(16, 16, 4)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image = fancy_tile_texture(self.blockWidth, self.blockHeight, self.textures, BLACK, 0)

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        # if self.visible:
        #     if get_time_diff(self.lastFrame) >= 0.235:
        #         self.texture = self.textures[self.index]
        #         self.image = self.tile_texture(self.blockWidth, self.blockHeight, self.texture, BLACK)
        #
        #         self.index += 1
        #         if self.index > 3:
        #             self.index = 0
        #
        #         self.lastFrame = time.time()
        pass


class RoomBorder(TileBase):
    def __init__(self, block_pos_x: float, block_pos_y: float, block_width: int | float, block_height: int | float):
        super().__init__(block_pos_x, block_pos_y, block_width, block_height)
        self.show(LAYER['wall'])
        all_borders.add(self)

        self.image = pygame.Surface(vec(block_width * 16, block_height * 16))
        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        pass


if __name__ == '__main__':
    os.system('python main.py')
