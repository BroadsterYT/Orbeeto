"""
Contains all sprite groups.
"""
import pygame
from pygame.sprite import Group

all_sprites = pygame.sprite.LayeredUpdates()

# --------------------------------- Character groups ---------------------------------#
all_players = Group()
all_enemies = Group()
all_sentries = Group()

# --------------------------------- Interactive groups ---------------------------------#
all_movable = Group()
all_trinkets = Group()
all_invisible = Group()

all_drops = Group()
all_slots = Group()

# --------------------------------- Projectile groups ---------------------------------#
all_projs = Group()  # noqa
all_explosions = Group()
all_portals = Group()

# --------------------------------- Room groups ---------------------------------#
all_walls = Group()
all_floors = Group()
all_borders = Group()
all_rooms = []

all_containers = []

# --------------------------------- UI groups ---------------------------------#
all_text_boxes = Group()
all_font_chars = Group()
all_stat_bars = Group()
