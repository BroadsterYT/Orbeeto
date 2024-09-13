import pygame
from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import controls as ctrl
import gamestack as gs
import spritesheet
import text


class ScrollWidget(cb.ActorBase):
    def __init__(self, gamestate: gs.GameState, pos_x, pos_y, vis_width: int, vis_height, entry_height: int):
        """A scroll widget that allows the display of items, settings, checkboxes, and more.

        :param gamestate: The gamestate the object should exist within
        :param pos_x: The x-axis position to spawn the widget
        :param pos_y: The y-axis position to spawn the widget
        :param entry_height: The height of each entry added into the widget
        """
        super().__init__(cst.LAYER['ui_2'], gamestate)
        self.add_to_gamestate()
        self.entries = []
        self.entry_space = 8
        self.width = vis_width
        self.height = vis_height
        self.entry_height = entry_height

        self.pos = vec(pos_x, pos_y)
        self.start_pos = vec(pos_x, pos_y)

        self.last_scroll_up, self.last_scroll_down = ctrl.key_released[4], ctrl.key_released[5]
        self.scroll_value = 0

        self.cover = ScrollWidgetCover(self)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 255))
        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def add_entry(self, *actors) -> None:
        """Adds an actor or list of actors to the entry list"""
        for actor in actors:
            self.entries.append(actor)

    def remove_entry(self, actor) -> None:
        """Removes an actor from the entry list."""
        self.entries.remove(actor)

    def assign_scroll_values(self) -> None:
        """Assigns the correct scroll position to each entry"""
        count = 0
        for entry in self.entries:
            entry.scroll_pos = count
            count += self.entry_height + self.entry_space

    def update(self):
        if self.last_scroll_up != ctrl.key_released[4]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.scroll_value -= 15
            # VVV Prevents widget from scrolling up beyond the last visible entry VVV
            if self.scroll_value < -self.entry_height * (len(self.entries) - 1) - self.entry_space * len(self.entries):
                self.scroll_value = -self.entry_height * (len(self.entries) - 1) - self.entry_space * len(self.entries)
            self.last_scroll_up = ctrl.key_released[4]

        if self.last_scroll_down != ctrl.key_released[5]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.scroll_value += 15
            if self.scroll_value > 0:
                self.scroll_value = 0  # Prevents scrolling down past the first entry
            self.last_scroll_down = ctrl.key_released[5]

        self.center_rects()


class ScrollWidgetCover(cb.ActorBase):
    def __init__(self, owner):
        super().__init__(cst.LAYER['ui_2'] + 2, owner.gamestate)
        self.add_to_gamestate()
        self.owner = owner

        self.pos = self.owner.pos
        self.start_pos = self.owner.start_pos

        self.image = pygame.Surface((self.owner.width, self.owner.height))
        sheet = spritesheet.Spritesheet('sprites/ui/scroll_widget.png', 4)
        tiles = sheet.get_images(32, 32, 4)

        b_width, b_height = self.owner.width // 32, self.owner.height // 32
        for x in range(b_width):
            for y in range(b_height):
                if x == 0 and y == 0:
                    self.image.blit(tiles[1], (x * 32, y * 32))
                elif x == b_width - 1 and y == 0:
                    self.image.blit(pygame.transform.rotate(tiles[1], 270), (x * 32, y * 32))
                elif x == 0 and y == b_height - 1:
                    self.image.blit(pygame.transform.rotate(tiles[1], 90), (x * 32, y * 32))
                elif x == b_width - 1 and y == b_height - 1:
                    self.image.blit(pygame.transform.rotate(tiles[1], 180), (x * 32, y * 32))
                elif y == 0:
                    self.image.blit(pygame.transform.rotate(tiles[3], 180), (x * 32, y * 32))
                elif y == b_height - 1:
                    self.image.blit(tiles[3], (x * 32, y * 32))
                elif x < 1 or x >= b_width - 1:
                    self.image.blit(pygame.transform.rotate(tiles[2], 90), (x * 32, y * 32))
                elif y < self.owner.entry_height // 32 or y >= b_height - self.owner.entry_height // 32:
                    self.image.blit(tiles[0], (x * 32, y * 32))

        self.image.set_colorkey((0, 0, 0))

        self.set_rects(self.pos.x, self.pos.y, self.owner.width, self.owner.height, self.owner.width, self.owner.height)

    def update(self):
        self.center_rects()


class ScrollPullTab(cb.ActorBase):
    def __init__(self, gamestate, owner: ScrollWidget):
        """A pull tab used on a scroll widget to allow scrolling by dragging

        :param gamestate: The gamestate the object should exist within
        :param owner: The scroll widget the pull tab belongs to
        """
        super().__init__(cst.LAYER['ui_2'], gamestate)
        self.add_to_gamestate()
        self.owner = owner


class ScrollWidgetEntry(cb.ActorBase):
    def __init__(self,
                 owner: ScrollWidget,
                 entry_text: str,
                 image_path: None | str = None,
                 sprites_per_row: int = 8,
                 sprite_width: int = 64,
                 sprite_height: int = 64,
                 sprite_count: int = 1,
                 sprite_offset: int = 0,
                 entry_type: int = 0):
        """An entry within a scroll widget

        :param owner: The scroll widget the entry belongs to
        :param entry_text: The text to display within the entry
        :param image_path: The path to use for the image to display in the entry. Defaults to None.
        :param sprites_per_row: The number of sprites in each row of the given spritesheet
        :param sprite_width: The width of each sprite in the given spritesheet
        :param sprite_height: The height of each sprite in the given spritesheet
        :param sprite_count: The number of sprites to pull from the spritesheet
        :param sprite_offset: Which sprite should the "snip" start from? Defaults to the first image in the spritesheet.
        :param entry_type: The interaction type for the entry. 0 for visual, 1 for numeric display, 2 for boolean
        display. Defaults to 0.
        """
        super().__init__(cst.LAYER['ui_2'] + 1, owner.gamestate)
        self.add_to_gamestate()
        self.owner = owner
        self.width, self.height = self.owner.width - 64, self.owner.entry_height

        self.pos = vec(self.owner.pos.x, self.owner.pos.y - self.owner.height // 2 + self.owner.entry_height)
        self.start_pos = self.owner.start_pos.copy()

        self.scroll_pos = 0

        self.entry_text = entry_text
        self.entry_type = entry_type

        # --- Get base entry image(s) --- #
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))

        # ------------------------------- #

        if image_path is not None:
            self.display_sheet = spritesheet.Spritesheet(image_path, sprites_per_row)
            self.display_images = self.display_sheet.get_images(sprite_width,
                                                                sprite_height,
                                                                sprite_count,
                                                                sprite_offset)
        else:
            pass

        if entry_type == 0:
            text_img = text.text_to_image(entry_text, text.dialogue_font)
            self.image.blit(text_img, (0, 0))

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def update(self):
        # VVV The position of an entry that is flush with the top lip of the widget border cover
        flush_top = self.owner.pos.y - self.owner.height // 2 + self.height // 2 + self.owner.entry_height
        self.pos.y = self.scroll_pos + self.owner.scroll_value + flush_top
        if self.pos.y < flush_top - self.owner.entry_height:
            self.pos.y = flush_top - self.owner.entry_height

        if self.pos.y > self.owner.pos.y + self.owner.height // 2 - self.height // 2:
            self.pos.y = self.owner.pos.y + self.owner.height // 2 - self.height // 2

        self.pos.x = self.owner.pos.x

        self.center_rects()

    def __repr__(self):
        return f'ScrollWidgetEntry({self.pos}, {self.scroll_pos})'
    