import pygame

# ---------------------------------- Aliases --------------------------------- #
vec = pygame.math.Vector2

# ---------------------------------- Window ---------------------------------- #
WIN_WIDTH = 1280
WIN_HEIGHT = 720
FPS = 60
SPF = 0.0167

ANIMTIME = 0.1

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
    'player_layer': 2,
    'enemy_layer': 2,
    'movable_layer': 2,
    'drops_layer': 2,
    'proj_layer': 2,
    'explosion_layer': 2,
    'wall_layer': 10,
    'grapple': 11,
    'portal_layer': 11,
    'text_layer': 50,
    'statBar_layer': 100,

    'ui_layer_1': 200
}

# ------------------------------ Object Movement ----------------------------- #
# The coefficient of friction for all objects with an acceleration parameter
FRIC = -0.07

# -------------------------------- Projectiles ------------------------------- #
PROJ_STD = 'proj_StdBullet'

PROJ_PORTAL = 'proj_PortalBullet'
PROJ_GRAPPLE = 'proj_GrappleHook'

# A dictionary that stores all damage constants of all projectile types
PROJ_DMG = {
    PROJ_STD: 1,
    
    PROJ_PORTAL: 15,
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
LTDROPS = {
    0: [[(MAT[0],), (MAT[0],), (MAT[0],),], # Standard Grunt
        [(MAT[0],), (MAT[0],), (MAT[0], MAT[0]),],
        [(MAT[0],), (MAT[0], MAT[0],), (MAT[0], MAT[0],),],],
    
    1: [[(MAT[0],), (MAT[0],), (MAT[1],),], # Octogrunt
        [(MAT[0],), (MAT[0],), (MAT[1],),],
        [(MAT[1],), (MAT[0], MAT[1],), (MAT[1], MAT[1],),],],

    2: [[(MAT[0],), (MAT[1],), (MAT[1],),], # Ambusher
        [(MAT[1],), (MAT[0], MAT[1],), (MAT[0], MAT[1],),],
        [(MAT[0],), (MAT[1], MAT[1],), (MAT[0], MAT[1], MAT[1]),],],
}