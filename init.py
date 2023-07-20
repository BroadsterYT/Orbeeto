import pygame
from pygame.locals import *

from class_bases import *
from constants import *
from calculations import *
from groups import *

from trinkets import *

#------------------------------ Initialize globals ------------------------------#
can_update = True

anim_timer: int = 0

keyReleased = {
    1: 0,
    2: 0,
    3: 0,

    K_a: 0,
    K_w: 0,
    K_s: 0,
    K_d: 0,
    K_e: 0,
    K_x: 0,
}
