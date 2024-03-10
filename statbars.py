import math
import os

from pygame.math import Vector2 as vec

import text

import classbases as cb
import constants as cst
import groups


class StatBar(cb.ActorBase):
    def __init__(self, owner, order: int, value_name: str, max_value_name: str, sheet_file: str):
        """A bar that shows a specific value on-screen

        Args:
            owner: The owner of the value being displayed
            order: The order in which the stat bar will be displayed with others
            value_name: Name of the field to display the value of
            max_value_name: The maximum value of the field to display
            sheet_file: The file location of the image to use for the stat bar
        """
        super().__init__(cst.LAYER['statbar'])
        groups.all_stat_bars.add(self)
        self.order = order  # The order of the stat bars, like which one is on top, which one is below that, etc.

        self.owner = owner

        self.value_name = value_name
        self.value = getattr(self.owner, self.value_name)
        self.max_value_name = max_value_name
        self.max_value = getattr(self.owner, self.max_value_name)

        self.set_images(os.path.join(os.getcwd(), sheet_file), 128, 16, 1, 17, 0, 16)

        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)
        self.accel_const = self.owner.accel_const
        self.set_rects(self.pos.x, self.pos.y, 128, 16, 128, 16)

        self.number = BarNumbers(self)

        self.show()

    def show(self):
        self.number.show()
        super().show()

    def hide(self):
        self.number.hide()
        super().hide()

    def movement(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)

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
                raise IndexError(f'No index of {self.index}')
        else:
            self.kill()


class BarNumbers(cb.ActorBase):
    def __init__(self, bar: StatBar):
        """A number indicating the value of a statbar

        Args:
            bar: The bar to display next to
        """
        super().__init__(cst.LAYER['statbar'])
        self.show()
        groups.all_stat_bars.add(self)

        self.bar = bar

        self.render_images()
        self.set_rects(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height(), self.image.get_width(),
                       self.image.get_height())

        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)

    def render_images(self):
        self.image = text.text_to_image(str(self.bar.value) + '/' + str(self.bar.max_value), text.font_small)

    def movement(self):
        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)
        self.center_rects()

    def update(self):
        self.movement()
        if self.bar.owner.hp > 0:
            self.render_images()
        else:
            self.kill()
