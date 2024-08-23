import math
import os
import time

import pygame
import pygame.gfxdraw
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
                 image_row: int = 0, style: int = 0, style_3d: int = 0, base_color: tuple = (0, 0, 1),
                 border_color: tuple = (0, 0, 1), color1: tuple = (0, 0, 1), color2: tuple = (0, 0, 1),
                 parallax_mult: tuple[float, float] = (1.0, 1.0)):
        """A 3D wall that cannot be passed or obstructed.

        :param pos_x: The x-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param pos_y: The y-axis position to spawn the wall on the block grid (1 block = 16 pixels)
        :param block_width: The width of the wall (in blocks)
        :param block_height: The height of the wall (in blocks)
        :param image_row: The row from the wall spritesheet to use to build the top of the wall
        :param style: The tiling style to use for the top of the wall
        :param style_3d: The style of wall to draw for the sides
        :param parallax_mult: The strength of the parallax for the x and y axes (affects the height and shape of the
        wall in the z-axis)
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

        self.style_3d = style_3d
        self.base_color = base_color
        self.border_color = border_color
        self.color1 = color1
        self.color2 = color2

        self.parallax_mult = vec(parallax_mult[0], parallax_mult[1])
        self.p_ratio_x = -(self.pos.x - cst.WINWIDTH // 2) / (cst.WINWIDTH // 2) * self.parallax_mult.x
        self.p_ratio_y = (self.pos.y - cst.WINHEIGHT // 2) / (cst.WINHEIGHT // 2) * self.parallax_mult.y

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def center_rects(self) -> None:
        self.rect.center = vec(self.pos.x - self.p_ratio_x * self.width, self.pos.y - self.p_ratio_y * self.height)
        self.hitbox.center = self.pos

    def update(self):
        self.p_ratio_x = -(self.pos.x - cst.WINWIDTH // 2) / (cst.WINWIDTH // 2) * self.parallax_mult.x
        self.p_ratio_y = -(self.pos.y - cst.WINHEIGHT // 2) / (cst.WINHEIGHT // 2) * self.parallax_mult.y


class PerspectiveWall(cb.ActorBase):
    def __init__(self, wall: Wall3D, axis: str):
        super().__init__(cst.LAYER['wall'])
        self.show()

        self.wall = wall
        self.axis = axis

        self.image = pygame.Surface(vec(64, 64))
        self.rect = self.image.get_rect()
        self.style = self.wall.style_3d
        self.base_color = self.wall.base_color
        self.border_color = self.wall.border_color
        self.color1 = self.wall.color1
        self.color2 = self.wall.color2
        self._apply_style()

        self.pos = vec(self.wall.pos.x, self.wall.pos.y)
        self.set_rects(self.pos.x, self.pos.y, self.rect.width, self.rect.height, self.rect.width, self.rect.height)

    def movement(self):
        if self.wall.p_ratio_x > 0:
            self.pos.x = self.wall.pos.x + self.wall.width // 2 - self.rect.width // 2
        else:
            self.pos.x = self.wall.pos.x - self.wall.width // 2 + self.rect.width // 2

        if self.wall.p_ratio_y > 0:
            self.pos.y = self.wall.pos.y + self.wall.height // 2 - self.rect.height // 2
        else:
            self.pos.y = self.wall.pos.y - self.wall.height // 2 + self.rect.height // 2

    def update(self):
        self._apply_style()
        self.center_rects()

    def _apply_style(self) -> None:
        """Draws the image of the wall using ``self.style`` to select the design

        :return: None
        """
        if self.style == 0:
            self._draw_style0(self.base_color)
        elif self.style == 1:
            self._draw_style1(self.base_color, self.border_color)

    def _draw_style0(self, base_color: tuple) -> None:
        """Draws a simple wall with a single solid color

        :param base_color: The base color to apply to the wall
        :return: None
        """
        warp_width: int = abs(math.ceil(self.wall.width * self.wall.p_ratio_x))
        warp_height: int = abs(math.ceil(self.wall.height * self.wall.p_ratio_y))

        if self.axis == 'x':
            self.image = pygame.Surface(
                (self.wall.width * abs(self.wall.p_ratio_x),
                 self.wall.height + abs(self.wall.p_ratio_y) * self.wall.height))
            self.rect = self.image.get_rect()
            self.image.fill((0, 0, 0))

            if self.wall.p_ratio_y > 0:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, 0),
                        (warp_width, warp_height),
                        (warp_width, self.image.get_height()),
                        (0, self.wall.height)
                    ],
                    base_color
                )

            else:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, self.image.get_height() - self.wall.height),
                        (warp_width, 0),
                        (warp_width, self.wall.height),
                        (0, self.image.get_height())
                    ],
                    base_color
                )
            if self.wall.p_ratio_x <= 0:
                self.image = pygame.transform.flip(self.image, False, True)

        elif self.axis == 'y':
            self.image = pygame.Surface(
                (self.wall.width + abs(self.wall.p_ratio_x) * self.wall.width,
                 self.wall.height * abs(self.wall.p_ratio_y)))
            self.rect = self.image.get_rect()
            self.image.fill((0, 0, 0))

            if self.wall.p_ratio_x > 0:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, 0),
                        (self.wall.width, 0),
                        (self.image.get_width(), self.image.get_height()),
                        (self.image.get_width() - self.wall.width, self.image.get_height())
                    ],
                    base_color
                )

            else:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, self.image.get_height()),
                        (self.image.get_width() - self.wall.width, 0),
                        (self.image.get_width(), 0),
                        (self.wall.width, self.image.get_height())
                    ],
                    base_color
                )
            if self.wall.p_ratio_y <= 0:
                self.image = pygame.transform.flip(self.image, False, True)

        self.image.set_colorkey((0, 0, 0))

    def _draw_style1(self, base_color: tuple, border_color: tuple) -> None:
        """Draws a wall of solid color with a border

        :param base_color:
        :param border_color:
        :return: None
        """
        warp_width: int = abs(math.ceil(self.wall.width * self.wall.p_ratio_x))
        warp_height: int = abs(math.ceil(self.wall.height * self.wall.p_ratio_y))

        if self.axis == 'x':
            self.image = pygame.Surface(
                (self.wall.width * abs(self.wall.p_ratio_x),
                 self.wall.height + abs(self.wall.p_ratio_y) * self.wall.height))
            self.rect = self.image.get_rect()
            self.image.fill((0, 0, 0))

            if self.wall.p_ratio_y > 0:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, 0),
                        (warp_width, warp_height),
                        (warp_width, self.image.get_height()),
                        (0, self.wall.height)
                    ],
                    border_color
                )

                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (16, 16),
                        (warp_width, warp_height),
                        (warp_width, self.image.get_height()),
                        (0, self.wall.height)
                    ],
                    base_color
                )

            else:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, self.image.get_height() - self.wall.height),
                        (warp_width, 0),
                        (warp_width, self.wall.height),
                        (0, self.image.get_height())
                    ],
                    border_color
                )
            if self.wall.p_ratio_x <= 0:
                self.image = pygame.transform.flip(self.image, False, True)

        elif self.axis == 'y':
            self.image = pygame.Surface(
                (self.wall.width + abs(self.wall.p_ratio_x) * self.wall.width,
                 self.wall.height * abs(self.wall.p_ratio_y)))
            self.rect = self.image.get_rect()
            self.image.fill((0, 0, 0))

            if self.wall.p_ratio_x > 0:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, 0),
                        (self.wall.width, 0),
                        (self.image.get_width(), self.image.get_height()),
                        (self.image.get_width() - self.wall.width, self.image.get_height())
                    ],
                    border_color
                )

            else:
                pygame.gfxdraw.filled_polygon(
                    self.image,
                    [
                        (0, self.image.get_height()),
                        (self.image.get_width() - self.wall.width, 0),
                        (self.image.get_width(), 0),
                        (self.wall.width, self.image.get_height())
                    ],
                    border_color
                )
            if self.wall.p_ratio_y <= 0:
                self.image = pygame.transform.flip(self.image, False, True)

        self.image.set_colorkey((0, 0, 0))


def spawn_3d_wall(pos_x, pos_y,
                  block_width, block_height,
                  image_row: int = 0,
                  style: int = 0, style_3d: int = 0,
                  base_color: tuple = (0, 0, 1), border_color: tuple = (0, 0, 1),
                  color1: tuple = (0, 0, 1), color2: tuple = (0, 0, 1),
                  parallax_mult=(1.0, 1.0)) -> list[Wall3D | PerspectiveWall]:
    """Returns a list containing a 3D wall with accompanying perspective walls

    :return: A list object containing a 3D wall with accompanying perspective walls
    """
    wall = Wall3D(pos_x, pos_y, block_width, block_height, image_row, style, style_3d,
                  base_color, border_color, color1, color2, parallax_mult)
    return [
        wall,
        PerspectiveWall(wall, 'x'),
        PerspectiveWall(wall, 'y')
    ]


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
