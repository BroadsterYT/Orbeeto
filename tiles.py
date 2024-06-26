import os
import time

import pygame
from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import calc
import groups
import spritesheet


def fancy_tile_texture(block_width: int, block_height: int, textures: list, color_key: tuple, style: int):
    final_image = pygame.Surface(vec(block_width * 16, block_height * 16))

    image_width, image_height = final_image.get_size()
    texture_width, texture_height = 16, 16

    # No borders
    if style == 0:
        for x in range(0, image_width, texture_width):
            for y in range(0, image_height, texture_height):
                tile_rect = pygame.Rect(x, y, texture_width, texture_height)
                final_image.blit(textures[0], tile_rect)

    final_image.set_colorkey(color_key)
    return final_image


class TileBase(cb.ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, block_width: int, block_height: int,
                 tile_size: int = 16):
        """The base class for all tile sprites

        :param pos_x: The x-axis position of the tile (in pixels)
        :param pos_y: The y-axis position of the tile (in pixels)
        :param block_width: The width of the tile (in tiles)
        :param block_height: The height of the tile (in tiles)
        :param tile_size: The size of each individual tile (in pixels). Default is 16.
        """
        super().__init__()
        self.tile_size = tile_size

        self.block_width, self.block_height = block_width, block_height
        self.width, self.height = self.block_width * self.tile_size, self.block_height * self.tile_size

        self.pos = vec((pos_x, pos_y))

        self.accel_const = 0.58

    def place_top_left(self, top_left_x, top_left_y) -> vec:
        """Returns the position of the tile's center given the position to place its top-left corner

        :param top_left_x: The x-axis position of the top-left corner
        :param top_left_y: The y-axis position of the top-left corner
        :return: The position of the tile's center
        """
        center = vec(0, 0)
        center.x = top_left_x + self.width // 2
        center.y = top_left_y + self.height // 2
        return center

    def movement(self):
        if self.can_update:
            self.set_room_pos()
            self.accel = self.get_accel()
            self.accel_movement()

    def __repr__(self):
        return f'Wall([{self.pos.x - self.hitbox.width // 2},{self.pos.y - self.hitbox.height // 2}])'


class Wall(TileBase):
    def __init__(self, pos_x: float, pos_y: float, block_width: int, block_height: int,
                 image_row: int = 0, style: int = 0):
        """A wall that cannot be passed or obstructed.

        :param pos_x: The x-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param pos_y: The y-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param block_width: The width of the wall (in blocks)
        :param block_height: The height of the wall (in blocks)
        :param image_row: The row of images to use from the sprite sheet
        :param style: The tiling style to use on the wall
        """
        super().__init__(pos_x, pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.show()
        groups.all_walls.add(self)

        self.pos = self.place_top_left(pos_x, pos_y)

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/tiles/wall.png'), 16)
        self.textures = self.spritesheet.get_images(16, 16, 16, image_row * 16)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image: pygame.Surface = fancy_tile_texture(self.block_width, self.block_height,
                                                        self.textures, cst.BLACK, style)

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        pass


class Floor(TileBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, block_width: int, block_height: int):
        super().__init__(pos_x, pos_y, block_width, block_height)
        self.layer = cst.LAYER['floor']
        self.show()
        groups.all_floors.add(self)

        self.pos = self.place_top_left(0, 0)

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/tiles/floor.png'), 4)
        self.textures = self.spritesheet.get_images(16, 16, 4)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image = fancy_tile_texture(self.block_width, self.block_height, self.textures, cst.BLACK, 0)

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        if self.visible:
            # self._animate()
            pass

    def _animate(self):
        if calc.get_time_diff(self.last_frame) >= 0.235:
            self.texture = self.textures[self.index]
            self.image = fancy_tile_texture(self.block_width, self.block_height, self.textures, cst.BLACK, 0)

            self.index += 1
            if self.index > 3:
                self.index = 0

            self.lastFrame = time.time()


class RoomBorder(TileBase):
    def __init__(self, pos_x: float, pos_y: float, block_width: int | float, block_height: int | float):
        super().__init__(pos_x, pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.show()
        groups.all_borders.add(self)

        self.image = pygame.Surface(vec(block_width * 16, block_height * 16))
        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        pass
