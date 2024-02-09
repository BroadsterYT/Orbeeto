import random as rand
import math
import time

import pygame
from pygame.math import Vector2 as vec

import constants as cst
import calculations as calc
import groups
import classbases as cb
import statbars
import itemdrops


class EnemyBase(cb.ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It gives you better control over enemy objects."""
        super().__init__(cst.LAYER['enemy'])
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.is_shooting = False

        # -------------------- In-game Stats --------------------#
        self._max_hp = None
        self._hp = None
        self._max_defense = None
        self._defense = None
        self._xp = None

        self.health_bar = statbars.HealthBar(self)

    def _set_stats(self, hp: int, defense: int, xp: int):
        self.max_hp = hp
        self.hp = hp
        self.max_defense = defense
        self.defense = defense
        self.xp = xp

    @property
    def max_hp(self):
        """The maximum amount of health the enemy can "naturally" have."""
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int):
        self._max_hp = value

    @property
    def hp(self):
        """The amount of health the enemy has. When the enemy's health reaches 0, it dies."""
        return self._hp

    @hp.setter
    def hp(self, value: int):
        if value > self.max_hp:
            self._hp = self.max_hp
        else:
            self._hp = value

    @property
    def max_defense(self):
        """The maximum amount of defense the enemy can "naturally" have."""
        return self._max_defense

    @max_defense.setter
    def max_defense(self, value: int):
        if value < 0:
            self._max_defense = 0
        else:
            self._max_defense = value

    @property
    def defense(self):
        """The amount of defense the enemy has. The higher its defense, the less damage it will take."""
        return self._defense

    @defense.setter
    def defense(self, value: int):
        if value < 0:
            self._defense = 0
        else:
            self._defense = value

    # ------------------------------------------------------------------------------#

    def _award_xp(self):
        for a_player in groups.all_players:
            a_player.xp += self.xp
            a_player.update_level()

    def _drop_items(self, table_index):
        drops = cst.LOOT_DROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)

        for item in drops[row][column]:
            groups.all_drops.add(
                itemdrops.ItemDrop(self, item)
            )

    def _destroy_check(self, amplitude, duration, loot_table_index: int) -> None:
        """Checks if the enemy's health has been fully depleted and will explode.

        Args:
            amplitude: The amplitude of the explosion
            duration: The duration of the explosion
            loot_table_index: Which loot table to select drops from
        """
        if self.hp <= 0:
            calc.screen_shake_queue.add(amplitude, duration)
            self._drop_items(loot_table_index)
            self._award_xp()
            self.kill()
