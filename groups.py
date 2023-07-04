import pygame

spriteGroup = pygame.sprite.Group

all_sprites = pygame.sprite.LayeredUpdates()

#--------------------------------- Character groups ---------------------------------#
all_players = spriteGroup()
all_enemies = spriteGroup()

#--------------------------------- Interactible groups ---------------------------------#
all_movable = spriteGroup()
all_invisible = spriteGroup()

all_drops = spriteGroup()
all_slots = spriteGroup()

#--------------------------------- Projectile groups ---------------------------------#
all_projs = spriteGroup()
all_explosions = spriteGroup()
all_portals = spriteGroup()

#--------------------------------- Room groups ---------------------------------#
all_walls = spriteGroup()
all_floors = spriteGroup()
all_rooms = []

all_containers = []

#--------------------------------- UI groups ---------------------------------#
all_font_chars = spriteGroup()
all_stat_bars = spriteGroup()