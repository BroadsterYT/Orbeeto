import math
import os
import time

import pygame
from pygame.math import Vector2 as vec

import classbases as cb
import constants as cst
import calc
import spritesheet


class Beam(cb.ActorBase):
    def __init__(self, from_sprite, to_sprite):
        super().__init__(cst.LAYER['floor'])
        self.add_to_gamestate()

        self.from_sprite, self.to_sprite = from_sprite, to_sprite
        self.index = 0
        
        self.length = calc.get_dist(self.from_sprite.pos, self.to_sprite.pos)
        self.angle = calc.get_angle(self.from_sprite.pos, self.to_sprite.pos)
        self.image = pygame.Surface(vec(1, 1))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def build_setup(self, start_pos: pygame.math.Vector2, end_pos: pygame.math.Vector2) -> None:
        self.length = calc.get_dist(start_pos, end_pos)
        self.angle = calc.get_angle(self.from_sprite.pos, self.to_sprite.pos)

        opp = (self.length / 2) * math.cos(math.radians(self.angle + 90))
        adj = (self.length / 2) * math.sin(math.radians(self.angle + 90))

        self.pos = vec(self.from_sprite.pos.x + opp, self.from_sprite.pos.y - adj)

    def build_image(self, frame_offset: int) -> None:
        """Builds the image of the beam.
        
        ### Arguments
            - frameOffset (``int``): The frame from "beams.png" to build the beam from
        """        
        self.spritesheet = spritesheet.Spritesheet(os.path.join(os.getcwd(), 'sprites/textures/beams.png'), 1)
        base_images = self.spritesheet.get_images(12, 12, 1, frame_offset)
        base_image: pygame.Surface = base_images[self.index]

        final_image = pygame.Surface(vec(base_image.get_width(), int(self.length)))

        offset = 0
        for i in range(int(self.length / base_image.get_height())):
            final_image.blit(base_image, vec(0, offset))
            offset += base_image.get_height()

        final_image.set_colorkey(cst.BLACK)
        self.image = pygame.transform.rotate(final_image, self.angle)

    def update(self):
        self.build_setup(self.from_sprite.pos, self.to_sprite.pos)
        self.build_image(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Background(cb.ActorBase):
    def __init__(self, image_folder: str):
        super().__init__(cst.LAYER['background'])
        self.add_to_gamestate()

        self.pos = vec(cst.WINWIDTH // 2, cst.WINHEIGHT // 2)

        image_names = os.listdir(image_folder)
        image_paths = []

        for name in image_names:
            image_paths.append(os.path.join(image_folder, name))

        for path in image_paths:
            self.orig_images.append(pygame.image.load(path).convert())
        self.images = self.orig_images

        print(self.images)
        self.set_rects(self.pos.x, self.pos.y, 1280, 720, 1280, 720)

    def movement(self):
        pass

    def update(self):
        if calc.get_time_diff(self.last_frame) >= cst.SPF / 2:
            self.index += 1
            if self.index > 358:
                self.index = 0
            self.last_frame = time.time()
        self.render_images()


class RotateTest(cb.ActorBase):
    def __init__(self):
        super().__init__(4)
        self.add_to_gamestate()

        self.pos = vec(0, 0)
        self.pivot = vec(cst.WINWIDTH // 2, cst.WINHEIGHT // 2)
        self.angle = 0
        self.radius = 128

        self.set_images('sprites/orbeeto/orbeeto.png', 64, 64, 5, 5)
        self.set_rects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def movement(self):
        self.pos = vec(self.pivot.x + self.radius * math.cos(math.radians(self.angle)), self.pivot.y - self.radius * math.sin(math.radians(self.angle)))
        self.angle += 1

    def update(self):
        self.rotate_image(self.angle)
        self.center_rects()


if __name__ == '__main__':
    test = Background('sprites/backgrounds/him_bg/')
