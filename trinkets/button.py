import os

from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import groups


class Button(cb.ActorBase):
    def __init__(self, id_value: int, block_pos_x: int, block_pos_y: int):
        """A button that can be activated and deactivated

        :param id_value: The ID vale of the button. Will activate any trinket with the same ID value.
        :param block_pos_x: The x-axis position of the button (in blocks)
        :param block_pos_y: The y-axis position of the button (in blocks)
        """
        super().__init__(cst.LAYER['button'])
        self.add_to_gamestate()
        groups.all_trinkets.add(self)

        self.id_value = id_value
        self.activated = False

        self.pos = vec((block_pos_x * 16, block_pos_y * 16))
        self.accel_const = 0.58

        self.set_room_pos()

        self.set_images(os.path.join(os.getcwd(), 'sprites/trinkets/button.png'), 64, 64, 2, 2)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def get_state(self) -> bool:
        """Checks if the button is being pressed by a box. Returns true if yes and false if no.

        Returns:
            bool: If button is activated (true/false)
        """
        is_active = False
        for box in groups.all_movable:
            if not self.hitbox.colliderect(box.hitbox):
                return is_active
            else:
                is_active = True
                return is_active

    def movement(self):
        if self.in_gamestate:
            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def update(self):
        if self.get_state():
            self.index = 1
        elif not self.get_state():
            self.index = 0
        self.render_images()

    def __repr__(self):
        return f'Button({self.id_value}, {self.pos}, {self.get_state()})'
