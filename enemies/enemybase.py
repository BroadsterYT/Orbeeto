import random as rand

from pygame.math import Vector2 as vec

import items
import visuals

import classbases as cb
import constants as cst
import groups
import itemdrops
import statbars


class EnemyBase(cb.ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It gives you better control over enemy objects."""
        super().__init__(cst.LAYER['enemy'])
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.is_shooting = False

        self.max_hp = 1
        self.hp = 1
        self.max_defense = 1
        self.defense = 1
        self.xp = 1

        self.health_bar = statbars.StatBar(self, 1, 'hp', 'max_hp', 'sprites/stat_bars/health_bar.png')

    def remove_from_gamestate(self) -> None:
        self.health_bar.remove_from_gamestate()
        super().remove_from_gamestate()

    def add_to_gamestate(self) -> None:
        self.health_bar.add_to_gamestate()
        super().add_to_gamestate()

    def _set_stats(self, hp: int, defense: int, xp: int):
        self.max_hp = hp
        self.hp = hp
        self.max_defense = defense
        self.defense = defense
        self.xp = xp

    # ------------------------------------------------------------------------------#
    def _award_xp(self):
        for a_player in groups.all_players:
            a_player.xp += self.xp
            a_player.update_level()

    def _drop_items(self, table_index):
        drops = items.ENEMY_LOOT_TABLES[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)

        for item in drops[row][column]:
            groups.all_drops.add(
                itemdrops.ItemDrop(self.pos.x, self.pos.y, item)
            )

    def _destroy_check(self, amplitude, duration, loot_table_index: int) -> None:
        """Checks if the enemy's health has been fully depleted and will explode.

        :param amplitude: The amplitude of the explosion
        :param duration: The duration of the explosion
        :param loot_table_index: Which loot table to select drops from
        :return: None
        """
        if self.hp <= 0:
            visuals.screen_shake_queue.add(amplitude, duration)
            self._drop_items(loot_table_index)
            self._award_xp()
            self.kill()
