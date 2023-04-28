#------------------------------ Window ------------------------------#
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

#------------------------------ Directions ------------------------------#
LEFT = 'loc_left'
RIGHT = 'loc_right'
UP = 'loc_up'
DOWN = 'loc_down'

TOP = 'loc_top'
BOTTOM = 'loc_bottom'

#------------------------------ Layers ------------------------------#
LAYERS = {
    'player_layer': 1,
    'enemy_layer': 1,
    'movable_layer': 1,
    'proj_layer': 1,
    'explosion_layer': 1,
    'wall_layer': 10,
    'portal_layer': 11,
    'text_layer': 51,
    'statBar_layer': 100
}

#------------------------------ Object Movement ------------------------------#
# The coefficient of friction for all objects with an acceleration parameter
FRIC = -0.07

#------------------------------ Projectiles ------------------------------#
PROJ_P_STD = 'playerBullet'
PROJ_P_BOUNCE = 'playerBouncy'
PROJ_P_PORTAL = 'playerPortal'

PROJ_E_STD = 'enemyBullet'

# A dictionary that stores all damage constants of all projectile types
PROJ_DICT = {
    PROJ_P_STD: 1,
    PROJ_P_BOUNCE: 1,
    PROJ_P_PORTAL: 15,
    PROJ_E_STD: 1,
}

SHOOT_RIGHT = 'right'
SHOOT_LEFT = 'left'
SHOOT_MIDDLE = 'middle'
SHOOT_BOTH = 'leftright'