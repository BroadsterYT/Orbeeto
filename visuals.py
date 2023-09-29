from class_bases import *


class InvisObj(ActorBase):
    def __init__(self, pos_x: int | float, pos_y: int | float, width: int, height: int):
        super().__init__()
        self.show(LAYER['floor'])
        all_invisible.add(self)

        self.pos = vec((pos_x, pos_y))
        
        self.image = pygame.Surface(vec(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_rect()

        self.center_rects()

    def update(self):
        pass


class Beam(ActorBase):
    def __init__(self, from_sprite, to_sprite):
        super().__init__()
        self.show(LAYER['floor'])

        self.fromSprite, self.toSprite = from_sprite, to_sprite
        self.index = 0
        
        self.length = get_dist_to_coords(self.fromSprite.pos, self.toSprite.pos)
        self.angle = get_angle_to_sprite(self.fromSprite, self.toSprite)
        self.image = pygame.Surface(vec(1, 1))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def build_setup(self, start_pos: pygame.math.Vector2, end_pos: pygame.math.Vector2):
        self.length = get_dist_to_coords(start_pos, end_pos)
        self.angle = get_angle_to_sprite(self.fromSprite, self.toSprite)

        opp = (self.length / 2) * cos(rad(self.angle + 90))
        adj = (self.length / 2) * sin(rad(self.angle + 90))

        self.pos = vec(self.fromSprite.pos.x + opp, self.fromSprite.pos.y - adj)

    def build_image(self, frame_offset: int) -> None:
        """Builds the image of the beam.
        
        ### Arguments
            - frameOffset (``int``): The frame from "beams.png" to build the beam from
        """        
        self.spritesheet = Spritesheet("sprites/textures/beams.png", 1)
        base_images = self.spritesheet.get_images(12, 12, 1, frame_offset)
        base_image: pygame.Surface = base_images[self.index]

        final_image = pygame.Surface(vec(base_image.get_width(), int(self.length)))

        offset = 0
        for i in range(int(self.length / base_image.get_height())):
            final_image.blit(base_image, vec(0, offset))
            offset += base_image.get_height()

        final_image.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(final_image, self.angle)

    def update(self):
        self.build_setup(self.fromSprite.pos, self.toSprite.pos)
        self.build_image(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
