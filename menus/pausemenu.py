"""
Module containing all classes and functions related to the pause menu
"""
import sys

import menus

import classbases as cb
import constants as cst
import gamestack as gs


class PauseMenu(cb.AbstractBase):
    def __init__(self):
        """The pause menu"""
        super().__init__()
        self.is_open = False

        self.settings_button = menus.MenuButton(gs.s_pause, cst.WINWIDTH // 2, 450, 256, 32, 'Settings', gs.gamestack.push, gs.s_settings)
        self.close_button = menus.MenuButton(gs.s_pause, cst.WINWIDTH // 2, 500, 256, 32, 'Close', sys.exit)

        # noinspection PyTypeChecker
        self.add(
            self.settings_button,
            self.close_button,
        )

        # TODO: Add settings menu page

    def update(self):
        pass
