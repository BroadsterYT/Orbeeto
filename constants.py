"""
Contains all global constants, like the size of the window, sprite layers, materials, loot tables, etc.
"""
# ---------------------------------- Window ---------------------------------- #
WINWIDTH = 1280  # noqa
WINHEIGHT = 720  # noqa
FPS = 60
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

    'ui_1': 200,
    'ui_2': 201,
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
