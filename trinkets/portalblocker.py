import pygame

import constants as cst
import groups
import spritesheet
import tiles


class PortalBlocker(tiles.TileBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, id_value: int, block_width: int, block_height: int):
        super().__init__(pos_x, pos_y, block_width, block_height)
        self.layer = cst.LAYER['wall']
        self.add_to_gamestate()
        groups.all_portal_blockers.add(self)

        self.id_value = id_value
        self.activator = self._get_activator()

        self.pos = self.place_top_left(pos_x, pos_y)

        self.spritesheet = spritesheet.Spritesheet('sprites/tiles/border_trinkets.png', 2)
        self.textures = self.spritesheet.get_images(16, 16, 16, 0)
        self.index = 0

        self.texture = self.textures[self.index]
        self.image: pygame.Surface = tiles.fancy_tile_texture(self.block_width, self.block_height,
                                                              self.textures, cst.BLACK, 0)

        self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)

    def _get_activator(self):
        """Finds the switch/trigger/activator sprite with the same ID value.

        Returns:
            The trinket that activates the locked wall
        """
        try:
            activator = next(t for t in groups.all_trinkets if t.id_value == self.id_value)
            return activator
        except StopIteration:
            raise IndexError

    def update(self):
        if self.activator.get_state() is not True:  # TODO: Reformat so that obj is not added/removed every call
            if self not in groups.all_portal_blockers:
                groups.all_portal_blockers.add(self)
        else:
            if self in groups.all_portal_blockers:
                groups.all_portal_blockers.remove(self)
