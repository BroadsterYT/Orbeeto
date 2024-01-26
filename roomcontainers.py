"""
Contains the room container class that handles enemies and movable entities in rooms.
"""
import pygame

import classbases as cb


vec = pygame.math.Vector2


class RoomContainer(cb.AbstractBase):
    def __init__(self, room_x: int | float, room_y: int | float, *sprites):
        """A container for sprites within a room. Contains data about all enemies in a room.

        Args:
            room_x: The container's x-location in the room grid
            room_y: The container's y-location in the room grid
            *sprites: The sprite(s) that should be added to the container
        """
        super().__init__()
        self.room = vec((room_x, room_y))

        for sprite in sprites:
            self.add(sprite)

    def hide_sprites(self):
        """Hides all the sprites in the container
        """
        for sprite in self.sprites():
            sprite.hide()

    def show_sprites(self):
        for sprite in self.sprites():
            sprite.show(sprite.layer)
            sprite.accel = vec(0, 0)
            sprite.vel = vec(0, 0)
            sprite.pos = sprite.room_pos
