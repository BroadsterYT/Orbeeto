import pygame
import math

# ---------------------------------- Aliases --------------------------------- #
vec = pygame.math.Vector2
spriteGroup = pygame.sprite.Group

rad = math.radians
deg = math.degrees

sin = math.sin
cos = math.cos
pi = math.pi

# ---------------------------------- Window ---------------------------------- #
WINWIDTH = 1280
WINHEIGHT = 720
FPS = 60
SPF = 0.0167

ANIMTIME = 0.1

LETTERS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
           'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
           'Z': 25}
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = {'/': 0}

UPPERCASE = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
             'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22,
             'X': 23, 'Y': 24, 'Z': 25}
LOWERCASE = {'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38,
             'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50,
             'z': 51}
NEW_NUMBERS = {'0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61}
NEW_SYMBOLS = {'.': 62, '!': 63, '\'': 64, ',': 65, ';': 66, ':': 67, '/': 68, '\\': 69, '\"': 70, '~': 71}

# ---------------------------------- Colors ---------------------------------- #
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# -------------------------------- Directions -------------------------------- #
WEST = 'loc_west'
EAST = 'loc_east'
NORTH = 'loc_north'
SOUTH = 'loc_south'

# ---------------------------------- Layers ---------------------------------- #
LAYER = {
    'floor': 1,
    'button': 2,
    'player': 3,
    'enemy': 3,
    'trinket': 5,
    'drops': 3,
    'proj': 3,
    'explosion': 5,
    'wall': 5,
    'grapple': 6,
    'portal': 6,

    'text': 50,
    'statbar': 100,
    'textbox': 110,

    'ui_1': 200
}

# ------------------------------ Object Movement ----------------------------- #
# The coefficient of friction for all objects with an acceleration parameter
FRIC = -0.07

# -------------------------------- Projectiles ------------------------------- #
PROJ_STD = 'proj_StdBullet'
PROJ_LASER = 'proj_Laser'

PROJ_PORTAL = 'proj_PortalBullet'
PROJ_GRAPPLE = 'proj_GrappleHook'

# A dictionary that stores all damage constants of all projectile types
PROJ_DAMAGE = {
    PROJ_STD: 7,
    PROJ_LASER: 16,

    PROJ_PORTAL: 0,
    PROJ_GRAPPLE: 0,
}

# ============================================================================ #
#                                  Loot Tables                                 #
# ============================================================================ #

# Dictionary of all materials in the game
MAT = {
    0: 'itemdrop_metalscrap_000',
    1: 'itemdrop_bolt_001',
    2: 'itemdrop_placeholder_002',
    3: 'itemdrop_placeholder_003',
    4: 'itemdrop_placeholder_004',
    5: 'itemdrop_placeholder_005',
    6: 'itemdrop_placeholder_006',
    7: 'itemdrop_placeholder_007',
    8: 'itemdrop_placeholder_008',
    9: 'itemdrop_placeholder_009',
    10: 'itemdrop_placeholder_010',
    11: 'itemdrop_placeholder_011',
    12: 'itemdrop_placeholder_012',
    13: 'itemdrop_placeholder_013',
    14: 'itemdrop_placeholder_014',
    15: 'itemdrop_placeholder_015',
    16: 'itemdrop_placeholder_016',
    17: 'itemdrop_placeholder_017',
    18: 'itemdrop_placeholder_018',
    19: 'itemdrop_placeholder_019',
    20: 'itemdrop_placeholder_020',
    21: 'itemdrop_placeholder_021',
    22: 'itemdrop_placeholder_022',
    23: 'itemdrop_placeholder_023',
    24: 'itemdrop_placeholder_024',
}

# All loot tables and their drops
LOOTDROPS = {
    0: [[(MAT[0],), (MAT[0],), (MAT[0],), ],  # Standard Grunt
        [(MAT[0],), (MAT[0],), (MAT[0], MAT[0]), ],
        [(MAT[0],), (MAT[0], MAT[0],), (MAT[0], MAT[0],), ], ],

    1: [[(MAT[0],), (MAT[0],), (MAT[1],), ],  # Octogrunt
        [(MAT[0],), (MAT[0],), (MAT[1],), ],
        [(MAT[1],), (MAT[0], MAT[1],), (MAT[1], MAT[1],), ], ],

    2: [[(MAT[0],), (MAT[1],), (MAT[1],), ],  # Ambusher
        [(MAT[1],), (MAT[0], MAT[1],), (MAT[0], MAT[1],), ],
        [(MAT[0],), (MAT[1], MAT[1],), (MAT[0], MAT[1], MAT[1]), ], ],
}
