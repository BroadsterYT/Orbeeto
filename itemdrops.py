from math import degrees, pi

from class_bases import *


class DropBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.cAccel = 0.8


class ItemDrop(DropBase):
    def __init__(self, dropped_from, item_name):
        """An item or material dropped by an enemy that can be collected
        
        ### Arguments
            - droppedFrom (``pygame.sprite.Sprite``): The enemy that the item was dropped from
            - itemName (``str``): The item to drop
        """        
        super().__init__()
        self.show(LAYER['drops'])
        all_drops.add(self)
        
        self.droppedFrom = dropped_from
        self.mat = item_name

        self.startTime = time.time()
        self.pos = vec(self.droppedFrom.pos.x, self.droppedFrom.pos.y)
        self.randAccel = get_rand_components(self.cAccel)
        
        self.spritesheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.index = 0

        if self.mat == MAT[0]:
            self.origImages = self.spritesheet.get_images(32, 32, 1, 0)
            self.images = self.spritesheet.get_images(32, 32, 1, 0)
        elif self.mat == MAT[1]:
            self.origImages = self.spritesheet.get_images(32, 32, 1, 1)
            self.images = self.spritesheet.get_images(32, 32, 1, 1)

        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.period_mult = rand.uniform(0.5, 1.5)

    def movement(self):
        self.accel = vec(0, 0)
        if self.canUpdate:
            exist_time = get_time_diff(self.startTime)
            self.accel = self.get_accel()
            
            if exist_time <= 10:
                self.origImage = self.origImages[self.index]
                self.image = pygame.transform.rotate(self.origImage, int(degrees(sin(self.period_mult * pi * exist_time) * (1 / exist_time))))
                self.rect = self.image.get_rect(center=self.rect.center)
            
            self.accel_movement()

    def get_accel(self) -> pygame.math.Vector2:
        room = get_room()
        final_accel = vec(0, 0)

        final_accel += room.get_accel()

        exist_time = get_time_diff(self.startTime)
        if exist_time <= 0.1:
            final_accel += self.randAccel

        return final_accel

    def update(self):
        self.movement()
        self.collide_check(all_walls)

        for a_player in all_players:
            if self.hitbox.colliderect(a_player):
                a_player.inventory[self.mat] += 1
                a_player.menu.update_menu_slots()
                self.kill()


if __name__ == '__main__':
    os.system('python main.py')
