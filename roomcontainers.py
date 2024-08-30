"""
Contains the room container class that handles enemies and movable entities in rooms.
"""
from pygame.math import Vector2 as vec

import classbases as cb


class RoomContainer(cb.AbstractBase):
    def __init__(self, room_x: int, room_y: int, *sprites):
        """A container for sprites within a room. Contains data about all enemies in a room.

        :param room_x: The container's x-location in the room grid
        :param room_y: The container's y-location in the room grid
        :param sprites: The sprite(s) that should be added to the container
        """
        super().__init__()
        self.room = vec((room_x, room_y))

        for sprite in sprites:
            self.add(sprite)

    def deactivate_sprites(self) -> None:
        """Removes all the sprites within the container from their game states

        :return: None
        """
        for sprite in self.sprites():
            sprite.remove_from_gamestate()

    def activate_sprites(self) -> None:
        """Adds all the sprites within the container to their game states

        :return: None
        """
        for sprite in self.sprites():
            sprite.add_to_gamestate()
            sprite.accel = vec(0, 0)
            sprite.vel = vec(0, 0)

            sprite.pos = sprite.room_pos

    def __repr__(self):
        return f'RoomContainer({self.room}, {self.sprites()})'
