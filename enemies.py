import pygame
import random as rand

from bullets import *
from class_bases import *
from itemdrops import *
from statbars import *


class EnemyBase(ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It contains parameters and methods to gain better control over enemy objects."""    
        super().__init__()
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.isGrappled = False

        self.is_shooting = False

        #-------------------- In-game Stats --------------------#
        self.max_hp = None
        self.hp = None
        self.max_attack = None
        self.attack = None
        self.max_defense = None
        self.defense = None
        self.xp_worth = None

        self.healthBar = HealthBar(self)

    def awardXp(self):
        for a_player in all_players:
            a_player.xp += self.xp_worth
            a_player.updateLevel()
            a_player.updateMaxStats()

    def dropItems(self, table_index):
        drops = LTDROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)
        
        for item in drops[row][column]:
            ItemDrop(self, item)


class StandardGrunt(EnemyBase):
    def __init__(self, posX: int, posY: int):
        """A simple enemy that moves to random locations and shoots at players.
        
        ### Arguments
            - posX (``int``): The x-position to spawn at
            - posY (``int``): The y-position to spawn at
        """         
        super().__init__()
        self.show(LAYER['enemy_layer'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WINWIDTH - 64), rand.randint(64, WINHEIGHT - 64))

        self.setImages("sprites/enemies/standard_grunt.png", 64, 64, 5, 5, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 15, 10, 10, 25, 0.4)

    def movement(self, canShoot: bool):
        if self.canUpdate and self.hp > 0:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(self.image.get_width() + 64, WINWIDTH - self.image.get_width() - 64)
                self.rand_pos.y = rand.randint(self.image.get_height() + 64, WINHEIGHT - self.image.get_height() - 64)
                self.lastRelocate = time.time()

            if self.pos.x != (self.rand_pos.x) or self.pos.y != (self.rand_pos.y):
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.ACCELC
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.ACCELC
                else:
                    self.accel.x = 0

                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.ACCELC
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.ACCELC
                else:
                    self.accel.y = 0
            
            if canShoot:
                self.shoot(getClosestPlayer(self), 6, rand.uniform(0.4, 0.9))

            self.accelMovement()

    def shoot(self, target, vel, shoot_time):
        if getTimeDiff(self.lastShot) > shoot_time:
            self.is_shooting = True
            try:
                angle_to_target = getAngleToSprite(self, target)
            except:
                angle_to_target = 0

            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))

            all_projs.add(EnemyStdBullet(self, self.pos.x - (21 * cos(rad(angle_to_target))) - (30 * sin(rad(angle_to_target))), self.pos.y + (21 * sin(rad(angle_to_target))) - (30 * cos(rad(angle_to_target))), vel_x, vel_y))
            self.lastShot = time.time()

    def update(self):
        if can_update and self.visible and self.hp > 0:
            self.collideCheck(all_players, all_walls)
            self.movement(True)
            
            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.is_shooting == True:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                        self.is_shooting = False
                self.lastFrame = time.time()
            self.rotateImage(getAngleToSprite(self, getClosestPlayer(self)))

        if self.hp <= 0:
            self.dropItems(0)
            self.awardXp()
            self.kill()


class OctoGrunt(EnemyBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show(LAYER['enemy_layer'])
        all_enemies.add(self)
        self.lastRelocate = time.time()
        self.lastShot = time.time()
        self.pos = vec((posX, posY))
        self.rand_pos = vec(rand.randint(64, WINWIDTH - 64), rand.randint(64, WINHEIGHT - 64))
        self.setImages("sprites/enemies/octogrunt.png", 64, 64, 1, 1, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        initStats(self, 44, 10, 10, 45, 0.4)
    
    def movement(self, canShoot):
        if self.canUpdate and self.visible:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.rand_pos.x = rand.randint(0, WINWIDTH)
                self.rand_pos.y = rand.randint(0, WINHEIGHT)
                self.lastRelocate = time.time()
            
            if self.pos.x != self.rand_pos.x or self.pos.y != self.rand_pos.y:
                if self.pos.x < self.rand_pos.x - 32:
                    self.accel.x = self.ACCELC
                elif self.pos.x > self.rand_pos.x + 32:
                    self.accel.x = -self.ACCELC
                else:
                    self.accel.x = 0
                if self.pos.y < self.rand_pos.y - 32:
                    self.accel.y = self.ACCELC
                elif self.pos.y > self.rand_pos.y + 32:
                    self.accel.y = -self.ACCELC
                else:
                    self.accel.y = 0
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 3, 1)
            
            self.accelMovement()

    def shoot(self, target, vel, shoot_time):
        if getTimeDiff(self.lastShot) > shoot_time:
            self.is_shooting = True
            angle_to_target = getAngleToSprite(self, target)
            vel_x = vel * -sin(rad(angle_to_target))
            vel_y = vel * -cos(rad(angle_to_target))
            OFFSET = 21
            all_projs.add(
                EnemyStdBullet(self, self.pos.x - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))), vel_x, vel_y),
                EnemyStdBullet(self, self.pos.x + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))), -vel_x, -vel_y),
                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))), self.pos.y + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 90)), vel * -cos(rad(angle_to_target + 90))),
                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))), self.pos.y - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 90)), -vel * -cos(rad(angle_to_target + 90))),
                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target + 45)), vel * -cos(rad(angle_to_target + 45))),
                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target + 45)), -vel * -cos(rad(angle_to_target + 45))),
                EnemyStdBullet(self, self.pos.x + (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), self.pos.y - (OFFSET * cos(rad(angle_to_target))) - (OFFSET * sin(rad(angle_to_target))), vel * -sin(rad(angle_to_target - 45)), vel * -cos(rad(angle_to_target - 45))),
                EnemyStdBullet(self, self.pos.x - (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), self.pos.y + (OFFSET * cos(rad(angle_to_target))) + (OFFSET * sin(rad(angle_to_target))), -vel * -sin(rad(angle_to_target - 45)), -vel * -cos(rad(angle_to_target - 45))),
            )
            self.lastShot = time.time()

    def update(self):
        if can_update and self.visible and self.hp > 0:
            self.collideCheck(all_players, all_walls)
            self.movement(True)

            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.is_shooting:
                    self.index += 0
                    if self.index > 4:
                        self.index = 0
                    self.is_shooting = False
                self.lastFrame = time.time()
            self.image = self.images[self.index]
            self.original_image = self.original_images[self.index]
            
            # Animation rotation
            self.image = pygame.transform.rotate(self.original_image, int(getAngleToSprite(self, getClosestPlayer(self))))
            self.rect = self.image.get_rect(center = self.pos)
        
        if self.hp <= 0:
            self.dropItems(1)
            self.awardXp()
            self.kill()
