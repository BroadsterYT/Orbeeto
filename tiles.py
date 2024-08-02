import os
import time

import pygame
from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import calc
import groups
import spritesheet
import visuals


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
        super().__init__(cst.LAYER['wall'])
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
        self.layer = cst.LAYER['wall'] + 1
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


class Wall3D(TileBase):
    def __init__(self, pos_x: float, pos_y: float, block_width: int, block_height: int,
                 image_row: int = 0, style: int = 0, parallax_mult: tuple[float, float] = (1.0, 1.0)):
        """A 3D wall that cannot be passed or obstructed.

        :param pos_x: The x-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param pos_y: The y-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param block_width: The width of the wall (in blocks)
        :param block_height: The height of the wall (in blocks)
        """
        super().__init__(pos_x, pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.show()
        groups.all_walls.add(self)

        self.pos = self.place_top_left(pos_x, pos_y)

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/tiles/wall.png'), 16)
        self.textures = self.spritesheet.get_images(16, 16, 16, image_row * 16)
        self.orig_image = fancy_tile_texture(self.block_width, self.block_height,
                                             self.textures, cst.BLACK, style)
        self.image = self.orig_image

        self.parallax_mult = vec(parallax_mult[0], parallax_mult[1])
        self.p_ratio_x = -(self.pos.x - cst.WINWIDTH // 2) / (cst.WINWIDTH // 2) * self.parallax_mult.x
        self.p_ratio_y = (self.pos.y - cst.WINHEIGHT // 2) / (cst.WINHEIGHT // 2) * self.parallax_mult.y

        self.wall_x = PerspectiveWall(self, 'x')
        self.wall_y = PerspectiveWall(self, 'y')

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def center_rects(self) -> None:
        self.rect.center = vec(self.pos.x - self.p_ratio_x * self.width, self.pos.y - self.p_ratio_y * self.height)
        self.hitbox.center = self.pos

    def update(self):
        self.p_ratio_x = -(self.pos.x - cst.WINWIDTH // 2) / (cst.WINWIDTH // 2) * self.parallax_mult.x
        self.p_ratio_y = -(self.pos.y - cst.WINHEIGHT // 2) / (cst.WINHEIGHT // 2) * self.parallax_mult.y

        if self.p_ratio_x > 0:
            self.wall_x.pos.x = self.pos.x + self.width // 2 - self.wall_x.rect.width // 2
            self.wall_y.pos.x = self.pos.x + self.width // 2 - self.wall_y.rect.width // 2
        else:
            self.wall_x.pos.x = self.pos.x - self.width // 2 + self.wall_x.rect.width // 2
            self.wall_y.pos.x = self.pos.x - self.width // 2 + self.wall_y.rect.width // 2

        if self.p_ratio_y > 0:
            self.wall_x.pos.y = self.pos.y + self.height // 2 - self.wall_x.rect.height // 2
            self.wall_y.pos.y = self.pos.y + self.height // 2 - self.wall_y.rect.height // 2
        else:
            self.wall_x.pos.y = self.pos.y - self.height // 2 + self.wall_x.rect.height // 2
            self.wall_y.pos.y = self.pos.y - self.height // 2 + self.wall_y.rect.height // 2


class PerspectiveWall(cb.ActorBase):
    def __init__(self, wall: Wall3D, axis: str, image_row: int = 0, style: int = 0):
        super().__init__(cst.LAYER['wall'])
        self.show()

        self.wall = wall
        self.axis = axis

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/tiles/wall.png'), 16)
        self.textures = self.spritesheet.get_images(16, 16, 16, image_row * 16)
        self.orig_image = fancy_tile_texture(self.wall.block_width, self.wall.block_height,
                                             self.textures, cst.BLACK, style)
        self.image, self.rect = visuals.warp(self.orig_image, [(0, 0), (0, 64), (64, 64), (64, 0)])

        self.pos = vec(self.wall.pos.x, self.wall.pos.y)
        self.set_rects(self.pos.x, self.pos.y, self.rect.width, self.rect.height, self.rect.width, self.rect.height)

    def update(self):
        if self.axis == 'x':
            self.image, self.rect = visuals.warp(
                self.orig_image,
                [(0, 0),
                 (0, self.wall.height),
                 (self.wall.width * self.wall.p_ratio_x, self.wall.height + self.wall.p_ratio_y * self.wall.height),
                 (self.wall.width * self.wall.p_ratio_x, self.wall.p_ratio_y * self.wall.height)])
        elif self.axis == 'y':
            self.image, self.rect = visuals.warp(
                self.orig_image,
                [(0, 0),
                 (self.wall.p_ratio_x * self.wall.width, self.wall.height * self.wall.p_ratio_y),
                 (self.wall.width + self.wall.p_ratio_x * self.wall.width, self.wall.height * self.wall.p_ratio_y),
                 (self.wall.width, 0)
                 ]
            )

        self.center_rects()


class PerspectiveWallTest(cb.ActorBase):
    def __init__(self, wall: Wall3D, axis: str, image_row: int = 0, style: int = 0):
        super().__init__(cst.LAYER['wall'])
        self.show()

        self.wall = wall
        self.axis = axis

        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/tiles/wall.png'), 16)
        self.textures = self.spritesheet.get_images(16, 16, 16, image_row * 16)
        self.orig_image = fancy_tile_texture(self.wall.block_width, self.wall.block_height,
                                             self.textures, cst.BLACK, style)
        self.image, self.rect = visuals.warp(self.orig_image, [(0, 0), (0, 64), (64, 64), (64, 0)])

        self.image_dict = {}
        if self.axis == 'x':
            for x in range(0, cst.WINWIDTH // 2):
                for y in range(0, cst.WINHEIGHT // 2):
                    print(f'Adding surface for {(x, y)}')
                    self.image_dict.update({
                        (x, y): visuals.warp(self.orig_image,
                                             [(0, 0),
                                              (0, self.wall.height),
                                              (self.wall.width * self.wall.p_ratio_x,
                                               self.wall.height + self.wall.p_ratio_y * self.wall.height),
                                              (self.wall.width * self.wall.p_ratio_x,
                                               self.wall.p_ratio_y * self.wall.height)])
                    })
        elif self.axis == 'y':
            pass

        self.pos = vec(self.wall.pos.x, self.wall.pos.y)
        self.set_rects(self.pos.x, self.pos.y, self.rect.width, self.rect.height, self.rect.width, self.rect.height)

    def update(self):
        self.center_rects()


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
