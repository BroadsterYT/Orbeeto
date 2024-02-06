"""
Contains all sprite groups.
"""
import pygame
from pygame.sprite import Group as SpriteGroup

all_sprites = pygame.sprite.LayeredUpdates()

# --------------------------------- Character groups ---------------------------------#
all_players = SpriteGroup()
all_enemies = SpriteGroup()

# --------------------------------- Interactive groups ---------------------------------#
all_movable = SpriteGroup()
all_trinkets = SpriteGroup()
all_invisible = SpriteGroup()

all_drops = SpriteGroup()
all_slots = SpriteGroup()

# --------------------------------- Projectile groups ---------------------------------#
all_projs = SpriteGroup()
all_explosions = SpriteGroup()
all_portals = SpriteGroup()

# --------------------------------- Room groups ---------------------------------#
all_walls = SpriteGroup()
all_floors = SpriteGroup()
all_borders = SpriteGroup()
all_rooms = []

all_containers = []

# --------------------------------- UI groups ---------------------------------#
all_text_boxes = SpriteGroup()
all_font_chars = SpriteGroup()
all_stat_bars = SpriteGroup()
