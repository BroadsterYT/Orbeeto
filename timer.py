"""
Module containing the timer class and instance for specific time-independent timing, if that makes sense.
"""
import time


class GameTimer:
    """
    The time system that all aspects of the game operate with
    """
    def __init__(self):
        self.game_start_time = time.time()
        self.time = self.game_start_time

        self._is_idle = False
        self._elapsed_time = 0.0
        self._last_elapse_call = time.time()

    def update_current_time(self) -> None:
        """Updates the game timer's current time. Accounts for all the time elapsed in menus. (This function should be
        called once every frame by the 's_action' game state!)

        :return: None
        """
        if self._is_idle:  # This adjusts the current time to account for the time elapsed in the last menu
            self._elapsed_time += (time.time() - self._last_elapse_call)
        self.time = time.time() - self._elapsed_time
        self._is_idle = False

    def update_elapsed_time(self) -> None:
        """Starts the elapsed time counter to account for time in a game state other than 'action'. (This function
        should be called once every frame by every game state other than 's_action'!)

        :return: None
        """
        if not self._is_idle:
            self._last_elapse_call = time.time()
        self._is_idle = True


g_timer = GameTimer()
