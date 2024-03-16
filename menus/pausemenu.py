"""
Module containing all classes and functions related to the pause menu
"""
import sys

import controls as ctrl
import menus

import classbases as cb
import constants as cst
import groups


class PauseMenu(cb.AbstractBase):
    def __init__(self):
        super().__init__()
        self.is_open = False
        self.last_pause_release = ctrl.key_released[ctrl.K_PAUSE]

        self.resume_button = menus.MenuButton(cst.WINWIDTH // 2, 300, 256, 32, 'Resume', self._force_unpause)
        self.close_button = menus.MenuButton(cst.WINWIDTH // 2, 500, 256, 32, 'Close', sys.exit)

        # noinspection PyTypeChecker
        self.add(
            self.resume_button,
            self.close_button,
        )
        for button in self.sprites():
            button.hide()
        self.trigger()

    def hide(self):
        for sprite in self.sprites():
            sprite.hide()
        self.is_open = False

    def show(self):
        for sprite in self.sprites():
            sprite.show()
        self.is_open = True

    def trigger(self) -> None:
        """Triggers the pause menu to open and close

        Returns:
            None
        """
        if self.last_pause_release != ctrl.key_released[ctrl.K_PAUSE] and not self.is_open:
            self._toggle_pause(True)
            self.show()

        elif self.last_pause_release != ctrl.key_released[ctrl.K_PAUSE] and self.is_open:
            self._toggle_pause(False)
            self.hide()

        self.last_pause_release = ctrl.key_released[ctrl.K_PAUSE]

    def _force_unpause(self) -> None:
        """Used to close the pause menu when the "resume" button is clicked

        Returns:
            None
        """
        self._toggle_pause(False)
        self.hide()
        self.last_pause_release -= 1

    @staticmethod
    def _toggle_pause(state: bool) -> None:
        """Sets the pause state for every object in the active game area

        Args:
            state: The value to give the "is_paused" field for every active object

        Returns:
            None
        """
        room = cb.get_room()
        for container in [c for c in groups.all_containers if c.room == room.room]:
            for sprite in container:
                sprite.is_paused = state
        room.is_paused = state
        room.player1.is_paused = state
