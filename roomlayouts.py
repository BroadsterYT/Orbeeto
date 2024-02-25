"""
Module containing the layouts of every room.
"""
from pygame.math import Vector2 as vec

import enemies

import constants as cst
import tiles
import trinkets


room_layouts = {
    vec(0, 0):
        [
            tiles.Wall(32, 512, 4, 64),
            tiles.Floor(cst.WINWIDTH // 2, cst.WINHEIGHT // 2, 80, 80),

            trinkets.Button(1, 14, 16),
            trinkets.Box(cst.WINWIDTH // 2, cst.WINHEIGHT // 2),
            trinkets.LockedWall(128, 64, 256, 100, 1, 4, 4),
            enemies.StandardGrunt(0, 0),
            enemies.Ambusher(600, 600)
        ],

    vec(0, 1):
        [
            enemies.StandardGrunt(0, 0),
        ],
}
