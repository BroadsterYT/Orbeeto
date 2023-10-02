from class_bases import *
# from tiles import TileBase


class Box(ActorBase):
    def __init__(self, pos_x, pos_y):
        """A box that can be pushed around and activate buttons.

        Args:
            pos_x: The position on the x-axis to spawn the box
            pos_y: The position on the y-axis to spawn the box
        """
        super().__init__()
        self.show(LAYER['trinket'])
        all_movable.add(self)

        self.pos = vec((pos_x, pos_y))
        self.cAccel = 0.58

        room = get_room()
        self.roomPos = vec((self.pos.x - room.pos.x, self.pos.y - room.pos.y))

        self.set_images("sprites/textures/box.png", 64, 64, 5, 1, 0, 0)
        self.set_rects(0, 0, 64, 64, 64, 64, True)

    def movement(self):
        if self.canUpdate and self.visible:
            self.collide_check(all_walls)

            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()

        for a_player in all_players:
            if self.hitbox.colliderect(a_player.hitbox):
                if triangle_collide(self, a_player) == SOUTH:
                    final_accel.y += 0.8
                if triangle_collide(self, a_player) == EAST:
                    final_accel.x += 0.8
                if triangle_collide(self, a_player) == NORTH:
                    final_accel.y -= 0.8
                if triangle_collide(self, a_player) == WEST:
                    final_accel.x -= 0.8

        return final_accel

    def update(self):
        # Teleporting
        for portal in all_portals:
            if self.hitbox.colliderect(portal.hitbox) and len(all_portals) == 2:
                self.teleport(portal)

    def __repr__(self):
        return f'Box({self.pos}, {self.vel}, {self.accel})'


class Button(ActorBase):
    def __init__(self, id_value: int, block_pos_x: int, block_pos_y: int):
        """A button that can be activated and deactivated

        Args:
            id_value: The ID vale of the button. Will activate any trinket with the same ID value.
            block_pos_x: The x-axis position of the button (in blocks)
            block_pos_y: The y-axis position of the button (in blocks)
        """
        super().__init__()
        self.show(LAYER['trinket'])
        all_trinkets.add(self)

        self.idValue = id_value
        self.activated = False

        self.pos = vec((block_pos_x * 16, block_pos_y * 16))
        self.cAccel = 0.58

        self.set_room_pos()

        self.set_images('sprites/trinkets/button.png', 64, 64, 2, 2)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def __active_check(self) -> bool:
        is_active = False
        for box in all_movable:
            if not self.hitbox.colliderect(box.hitbox):
                return is_active
            else:
                is_active = True
                return is_active

    def get_state(self):
        return self.__active_check()

    def movement(self):
        if self.canUpdate and self.visible:
            self.set_room_pos()

            self.accel = self.get_accel()
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = get_room()
        final_accel = vec(0, 0)
        final_accel += room.get_accel()
        return final_accel

    def update(self):
        if self.__active_check():
            self.index = 1
        elif not self.__active_check():
            self.index = 0

        self.render_images()

    def __repr__(self):
        return f'Button({self.idValue}, {self.pos}, {self.__active_check()})'


# class LockedWall(TileBase):
#     def __init__(self, id_value: int, start_block_pos_x: int, start_block_pos_y: int, end_block_pos_x: int,
#                  end_block_pos_y: int, block_width: int, block_height: int):
#         """A wall that will move when activated by a switch or button
#
#         ### Arguments
#             - idValue (``int``): The ID value of the wall. A button with the same ID value must be present in the same room!
#             - sBlockPosX (``int``): The x position where the wall should be placed in "tiles" (0 being the left edge and 80 being the right)
#             - sBlockPosY (``int``): The y position where the wall should be placed in "tiles" (0 being the top edge and 45 being the bottom)
#             - eBlockPosX (``int``): The x position where the wall should relocate after being activated (0 being the left edge and 80 being the right)
#             - eBlockPosY (``int``): The y position where the wall should relocate after being activated (0 being the top edge and 45 being the bottom)
#             - blockWidth (``int``): The width of the wall in "tiles"
#             - blockHeight (``int``): The height of the wall in "tiles"
#         """
#         super().__init__(start_block_pos_x, start_block_pos_y, block_width, block_height)
#         self.show(LAYER['wall'])
#         all_walls.add(self)
#         all_trinkets.add(self)
#         self.idValue = id_value
#
#         self.switch: Button = self.__find_switch()
#         self.lastSwitchState = self.switch.get_state()
#         self.hasActivated = False
#         self.lastChange = time.time()
#
#         self.pos = get_top_left_coords(self.width, self.height, start_block_pos_x * self.tileSize,
#                                        start_block_pos_y * self.tileSize)
#         self.startPos = get_top_left_coords(self.width, self.height, start_block_pos_x * self.tileSize,
#                                             start_block_pos_y * self.tileSize)
#         self.endPos = get_top_left_coords(self.width, self.height, end_block_pos_x * self.tileSize,
#                                           end_block_pos_y * self.tileSize)
#
#         self.spritesheet = Spritesheet('sprites/tiles/wall.png', 1)
#         self.textures = self.spritesheet.get_images(16, 16, 1)
#         self.index = 0
#
#         self.texture = self.textures[self.index]
#         self.image = tile_texture(self.blockWidth, self.blockHeight, self.texture, BLACK)
#
#         self.set_rects(self.pos.x, self.pos.y, self.width, self.height, self.width, self.height)
#
#     def __find_switch(self) -> pygame.sprite.Sprite:
#         try:
#             switch_match = next(s for s in all_trinkets if s.idValue == self.idValue)
#             return switch_match
#         except StopIteration:
#             raise CustomError(f'Error: No switch with idValue of {self.idValue} found')
#
#     def __activate(self):
#         current_switch_state = self.switch.get_state()
#         if current_switch_state != self.lastSwitchState:
#             # Button state has changed, update lastChange and reset position
#             self.lastChange = time.time()
#             self.lastSwitchState = current_switch_state
#
#         weight = get_time_diff(self.lastChange) / 3
#         if not self.switch.get_state() and self.hasActivated:
#             self.pos = cerp(self.pos, self.startPos, weight)
#         elif self.switch.get_state():
#             self.hasActivated = True
#             self.pos = cerp(self.pos, self.endPos, weight)
#
#     def update(self):
#         self.__activate()
#         self.center_rects()
#
#     def __repr__(self):
#         return f'LockedWall({self.idValue}, {self.pos}, {self.switch})'
