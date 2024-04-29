"""
Module containing all classes and functions related to the pause menu
"""
import sys

import controls as ctrl
import menus

import classbases as cb
import constants as cst
import gamestack as gs
import groups


class PauseMenu(cb.AbstractBase):
    def __init__(self):
        """The pause menu"""
        super().__init__()
        self.is_open = False

        self.close_button = menus.MenuButton(gs.s_pause, cst.WINWIDTH // 2, 500, 256, 32, 'Close', sys.exit)

        # noinspection PyTypeChecker
        self.add(
            self.close_button,
        )

        # TODO: Add settings button
        # TODO: Add settings menu page

    def update(self):
        # ----- Prevents the buttons in the pause menu from being clicked when pause menu is closed ----- #
        if self.is_open:
            for button in self.sprites():
                button.pos = button.return_pos
        else:
            for button in self.sprites():
                button.pos = (-5000, -5000)
        # ----------------------------------------------------------------------------------------------- #
