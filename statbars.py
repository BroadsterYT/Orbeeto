import math
import os

import pygame
from pygame.math import Vector2 as vec

import text

import classbases as cb
import constants as cst
import groups


class StatBar(cb.ActorBase):
    def __init__(self, owner, order: int, value_name: str, max_value_name: str, sheet_file: str):
        """A bar that shows a specific value on-screen

        :param owner: The owner of the value being displayed
        :param order: The order in which the stat bar will be displayed with others
        :param value_name: Name of the field to display the value of
        :param max_value_name: The maximum value of the field to display
        :param sheet_file: The file location of the image to use for the stat bar
        """
        super().__init__(cst.LAYER['statbar'])
        groups.all_stat_bars.add(self)
        self.order = order  # The order of the stat bars, like which one is on top, which one is below that, etc.
        self.order_offset = 42  # Space between sprite and first stat bar
        self.order_space = 18  # Space between each stat bar

        self.owner = owner

        self.value_name = value_name
        self.value = getattr(self.owner, self.value_name)
        self.max_value_name = max_value_name
        self.max_value = getattr(self.owner, self.max_value_name)

        self.set_images(os.path.join(os.getcwd(), sheet_file), 128, 16, 1, 17, 0, 16)

        self.pos = vec(self.owner.pos.x,
                       self.owner.pos.y + self.order_offset + self.order * self.order_space)
        self.accel_const = self.owner.accel_const
        self.set_rects(self.pos.x, self.pos.y, 128, 16, 128, 16)

        self.number = BarNumbers(self)

    def add_to_gamestate(self) -> None:
        self.number.add_to_gamestate()
        super().add_to_gamestate()

    def remove_from_gamestate(self) -> None:
        self.number.remove_from_gamestate()
        super().remove_from_gamestate()

    def movement(self):
        self.pos = vec(self.owner.pos.x,
                       self.owner.pos.y + 42 + self.order * self.order_space)

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.value = getattr(self.owner, self.value_name)
        self.max_value = getattr(self.owner, self.max_value_name)

        self.movement()

        if self.owner.hp > 0:
            self.index = math.floor((16 * self.value) / self.max_value)
            try:
                self.render_images()
            except IndexError:
                raise IndexError(f'No index of {self.index}.\nself.value = {self.value_name}')
        else:
            self.kill()


class StatBarTest(cb.ActorBase):
    def __init__(self, owner):
        super().__init__(cst.LAYER['statbar'])
        groups.all_stat_bars.add(self)
        self.add_to_gamestate()

        self.owner = owner
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 48)

        self.image = pygame.Surface(vec(128, 16))
        self.image.fill((0, 0, 1))

        self.set_rects(self.pos.x, self.pos.y, 128, 16, 128, 16)

        self.heat_numbers = BarNumbersTest(self, 80, 0, 'gun_heat', 'heat_thresh')

    def update(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 48)
        self.center_rects()
        self._animate()

    def _animate(self):
        self.image.fill((0, 0, 1))
        hp_bar = pygame.Surface(vec((self.owner.hp / self.owner.max_hp) * 128, 16))
        hp_bar.fill((255, 0, 0))
        self.image.blit(hp_bar, (0, 0))

        heat_bar_width = math.floor(self.owner.gun_heat / self.owner.heat_thresh * 128)
        if heat_bar_width > 128:
            heat_bar_width = 128

        heat_bar = pygame.Surface(vec(heat_bar_width, 6))
        dim_color = pygame.Color(255, 255, 20)
        bright_color = pygame.Color(250, 250, 250)
        for i in range(heat_bar_width):
            color_strip = pygame.Surface(vec(1, 6))
            color_strip.fill(dim_color.lerp(bright_color, i / 128))
            heat_bar.blit(color_strip, (i, 0))
        self.image.blit(heat_bar, (0, 10))


class BarNumbersTest(cb.ActorBase):
    def __init__(self, bar, pos_x_rel: float, pos_y_rel: float, value_name: str, max_value_name: str):
        super().__init__(cst.LAYER['statbar'])
        self.add_to_gamestate()
        groups.all_stat_bars.add(self)

        self.bar = bar
        self.rel_pos = vec(pos_x_rel, pos_y_rel)
        self.pos = vec(self.bar.pos.x + self.rel_pos.x, self.bar.pos.y + self.rel_pos.y)

        self.value_name = value_name
        self.value = getattr(self.bar.owner, self.value_name)
        self.max_value_name = max_value_name
        self.max_value = getattr(self.bar.owner, self.max_value_name)

        self.image = text.text_to_image(f'{self.value}/{self.max_value}', text.font_small)
        self.set_rects(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height(), self.image.get_width(),
                       self.image.get_height())

    def update(self):
        self.pos = vec(self.bar.pos.x + self.rel_pos.x, self.bar.pos.y + self.rel_pos.y)
        self.center_rects()

        self.value = getattr(self.bar.owner, self.value_name)
        self.max_value = getattr(self.bar.owner, self.max_value_name)

        self.image = text.text_to_image(f'{self.value}/{self.max_value}', text.font_small)


class BarNumbers(cb.ActorBase):
    def __init__(self, bar: StatBar):
        """A number indicating the value of a stat bar

        :param bar: The bar to display next to
        """
        super().__init__(cst.LAYER['statbar'])
        self.add_to_gamestate()
        groups.all_stat_bars.add(self)

        self.bar = bar

        self.render_images()
        self.set_rects(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height(), self.image.get_width(),
                       self.image.get_height())

        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)
        self.center_rects()

    def render_images(self):
        self.image = text.text_to_image(str(self.bar.value) + '/' + str(self.bar.max_value), text.font_small)

    def movement(self):
        self.pos = vec(self.bar.owner.pos.x + self.bar.rect.width // 2 + self.rect.width // 2,
                       self.bar.owner.pos.y + self.bar.order * self.bar.order_space + 42)
        self.center_rects()

    def update(self):
        if self.bar.owner.hp > 0:
            self.movement()
            self.render_images()
        else:
            self.kill()
