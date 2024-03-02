"""
Contains all global constants, like the size of the window, sprite layers, materials, loot tables, etc.
"""
# ---------------------------------- Window ---------------------------------- #
WINWIDTH = 1280  # noqa
WINHEIGHT = 720  # noqa
FPS = 60
SPF = 0.0167

LETTERS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
           'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
           'Z': 25}
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = {'/': 0}

UPPERCASE = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
             'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22,
             'X': 23, 'Y': 24, 'Z': 25}
LOWERCASE = {'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37,
             'm': 38, 'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49,
             'y': 50, 'z': 51}
NEW_NUMBERS = {'0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61}
NEW_SYMBOLS = {'.': 62, '!': 63, '\'': 64, ',': 65, ';': 66, ':': 67, '/': 68, '\\': 69, '\"': 70, '~': 71, '?': 72,
               '(': 73, ')': 74, '[': 75, ']': 76, '{': 77, '}': 78, '<': 79, '>': 80}

# ---------------------------------- Colors ---------------------------------- #
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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
FRIC = -0.07  # noqa

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
