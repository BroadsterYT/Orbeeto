from class_bases import *
from constants import *


class DamageChar(ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, damage: int):
        """A number that pops up after a player or enemy is hit that indicates how much damage that entity has taken
        
        ### Arguments
            - posX (``float``): _description_
            - posY (``float``): _description_
            - damage (``int``): _description_
        """        
        super().__init__()
        self.show(LAYER['text'])
        all_font_chars.add(self)
        
        self.start = time.time()
        self.pos = vec((pos_x, pos_y))

        self.image = text_to_image(str(damage), "sprites/ui/font.png", 9, 14, 36)
        self.set_rects(self.pos.x, self.pos.y, 9, 14, 9, 14)

    def movement(self):
        self.accel = vec(0, 0)
        if get_time_diff(self.start) < 0.1:
            self.accel = vec(0, -1)

        self.accel_movement()

    def update(self):
        self.movement()

        if get_time_diff(self.start) > 0.6:
            self.kill()
