"""
Contains all sprite groups.
"""
from pygame.sprite import Group

# --------------------------------- Character groups ---------------------------------#
all_players = Group()
all_enemies = Group()
all_sentries = Group()

# --------------------------------- Interactive groups ---------------------------------#
all_movable = Group()
all_trinkets = Group()

all_drops = Group()

all_material_slots = Group()
all_armor_slots = Group()
all_l_gun_slots = Group()
all_r_gun_slots = Group()

# --------------------------------- Projectile groups ---------------------------------#
all_projs = Group()  # noqa
all_explosions = Group()
all_portals = Group()

# --------------------------------- Room groups ---------------------------------#
all_walls = Group()
all_portal_blockers = Group()
all_floors = Group()
all_borders = Group()

all_rooms = []
all_containers = []

# --------------------------------- UI groups ---------------------------------#
all_font_chars = Group()
all_stat_bars = Group()
