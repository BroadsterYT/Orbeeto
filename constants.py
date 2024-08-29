"""
Contains all global constants, like the size of the window, sprite layers, materials, loot tables, etc.
"""

# ---------------------------------- Window ---------------------------------- #
WINWIDTH = 1280  # noqa
WINHEIGHT = 720  # noqa

FPS = 480  # The frame rate the game will actually run at
M_FPS = 60  # The frame speed that anything moving will use to calculate velocity and/or acceleration
SPF = 0.0167

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
    'background': 1,
    'floor': 2,
    'button': 3,
    'player': 4,
    'enemy': 4,
    'trinket': 6,
    'drops': 4,
    'proj': 4,
    'explosion': 6,
    'wall': 6,
    'grapple': 7,
    'portal': 7,

    'text': 50,
    'statbar': 100,
    'textbox': 110,

    'ui_1': 200,
    'ui_2': 201,
}

# ------------------------------ Object Movement ----------------------------- #
# The coefficient of friction for all objects with an acceleration parameter
FRIC = -0.07
