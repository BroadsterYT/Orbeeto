import pygame
import math

import classbases as cb
import calculations as calc
import constants as cst
import groups

# Aliases
vec = pygame.math.Vector2


# TODO: Generate value of bar on-the-fly and overlay UI on top...?
class StatBarBase(cb.ActorBase):
    def __init__(self, owner, order: int):
        """A bar that shows a specific value on-screen

        Args:
            owner: The owner of the value being displayed
            order: The order in which the statbar will be displayed with others
        """
        super().__init__()
        self.show(cst.LAYER['statbar'])
        groups.all_stat_bars.add(self)
        self.owner = owner
        self.order = order  # The order of the stat bars, like which one is on top, which one is below that, etc.

        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)
        self.cAccel = 0.58
        self.set_rects(self.pos.x, self.pos.y, 128, 16, 128, 16)

        self.number = BarNumbers(self)

    def movement(self):
        self.pos = vec(self.owner.pos.x, self.owner.pos.y + 42 + self.order * 18)

        self.rect.center = self.pos
        self.hitbox.center = self.pos


class BarNumbers(cb.ActorBase):
    def __init__(self, bar):
        """A number indicating the value of a statbar

        Args:
            bar: The bar to display next to
        """
        super().__init__()
        self.show(cst.LAYER['statbar'])
        groups.all_stat_bars.add(self)

        self.bar = bar
        self.owner = self.bar.owner

        self.render_images()
        self.set_rects(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height(), self.image.get_width(),
                       self.image.get_height())

        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)

    def render_images(self):
        if isinstance(self.bar, HealthBar):
            self.image = calc.text_to_image(str(self.owner.hp) + '/' + str(self.owner.maxHp),
                                            'sprites/ui/small_font.png', 5,
                                            7, 37)

        elif isinstance(self.bar, DodgeBar):
            self.image = calc.text_to_image(str(self.owner.dodgeTime) + '/' + str(self.owner.dodgeTimeCharge),
                                            'sprites/ui/small_font.png', 5, 7, 37)

        elif isinstance(self.bar, AmmoBar):
            self.image = calc.text_to_image(str(self.owner.ammo) + '/' + str(self.owner.maxAmmo),
                                            'sprites/ui/small_font.png', 5, 7, 37)

        else:
            raise TypeError()

    def movement(self):
        self.pos = vec(self.bar.pos.x + self.bar.rect.width // 2 + self.rect.width // 2, self.bar.pos.y)
        self.center_rects()

    def update(self):
        self.movement()
        if self.owner.hp > 0:
            self.render_images()
        else:
            self.kill()


class HealthBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 0)
        self.set_images('sprites/stat_bars/health_bar.png', 128, 16, 1, 17, 0, 16)

    def update(self):
        self.movement()
        if self.owner.hp > 0:
            self.index = math.floor((16 * self.owner.hp) / self.owner.maxHp)
            self.render_images()
        else:
            self.kill()


class DodgeBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 2)
        self.set_images('sprites/stat_bars/dodge_bar.png', 128, 16, 1, 17, 0, 16)

    def update(self):
        self.movement()
        if self.owner.hp > 0:
            if self.owner.dodgeTime < self.owner.dodgeTimeCharge:
                self.index = math.ceil((16 * self.owner.dodgeTime) / self.owner.dodgeTimeCharge)
                self.render_images()
        else:
            self.kill()


class AmmoBar(StatBarBase):
    def __init__(self, owner):
        super().__init__(owner, 1)
        self.set_images('sprites/stat_bars/ammo_bar.png', 128, 16, 1, 17, 0, 16)

    def update(self):
        self.movement()
        if self.owner.hp > 0:
            self.index = math.floor((16 * self.owner.ammo) / self.owner.maxAmmo)
            self.render_images()
        else:
            self.kill()
