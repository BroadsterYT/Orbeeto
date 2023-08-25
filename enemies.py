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

        self.isShooting = False

        #-------------------- In-game Stats --------------------#
        self.maxHp = None
        self.hp = None
        self.maxAtk = None
        self.atk = None
        self.maxDef = None
        self.defense = None
        self.xpWorth = None

        self.healthBar = HealthBar(self)

    def awardXp(self):
        for a_player in all_players:
            a_player.xp += self.xpWorth
            a_player.updateLevel()
            a_player.updateMaxStats()

    def dropItems(self, tableIndex):
        drops = LTDROPS[tableIndex]
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
        self.show(LAYER['enemy'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((posX, posY))
        self.randPos = vec(rand.randint(64, WINWIDTH - 64), rand.randint(64, WINHEIGHT - 64))

        self.setImages("sprites/enemies/standard_grunt.png", 64, 64, 5, 5, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        self.maxHp = 15
        initStats(self, 15, 10, 10, 40, 0.4)

    def movement(self, canShoot: bool):
        if self.canUpdate and self.hp > 0:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.randPos.x = rand.randint(self.image.get_width() + 64, WINWIDTH - self.image.get_width() - 64)
                self.randPos.y = rand.randint(self.image.get_height() + 64, WINHEIGHT - self.image.get_height() - 64)
                self.lastRelocate = time.time()

            self.accel = self.getAccel()
            
            if canShoot:
                self.shoot(getClosestPlayer(self), 6, rand.uniform(0.4, 0.9))

            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        room = self.getRoom()
        finalAccel = vec(0, 0)

        finalAccel += room.getAccel()

        if self.pos.x != self.randPos.x or self.pos.y != self.randPos.y:
            if self.pos.x < self.randPos.x - self.hitbox.width // 2:
                finalAccel.x += self.cAccel
            if self.pos.x > self.randPos.x + self.hitbox.width // 2:
                finalAccel.x -= self.cAccel

            if self.pos.y < self.randPos.y - self.hitbox.height // 2:
                finalAccel.y += self.cAccel
            if self.pos.y > self.randPos.y + self.hitbox.height // 2:
                finalAccel.y -= self.cAccel

        return finalAccel

    def shoot(self, target, vel, shootTime):
        if getTimeDiff(self.lastShot) > shootTime:
            self.isShooting = True
            try:
                angle = getAngleToSprite(self, target)
            except:
                angle = 0

            vel_x = vel * -sin(rad(angle))
            vel_y = vel * -cos(rad(angle))

            all_projs.add(EnemyStdBullet(self, self.pos.x - (21 * cos(rad(angle))) - (30 * sin(rad(angle))), self.pos.y + (21 * sin(rad(angle))) - (30 * cos(rad(angle))), vel_x, vel_y))
            self.lastShot = time.time()

    def update(self):
        if self.canUpdate and self.visible and self.hp > 0:
            self.collideCheck(all_players, all_walls)
            self.movement(True)
            
            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.isShooting == True:
                    self.index += 1
                    if self.index > 4:
                        self.index = 0
                        self.isShooting = False
                self.lastFrame = time.time()
            self.rotateImage(getAngleToSprite(self, getClosestPlayer(self)))

        if self.hp <= 0:
            self.dropItems(0)
            self.awardXp()
            self.kill()

    def __str__(self):
        return f'StandardGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xpWorth}'

    def __repr__(self):
        return f'StandardGrunt({self.pos}, {self.vel}, {self.accel}, {self.xpWorth})'


class OctoGrunt(EnemyBase):
    def __init__(self, posX, posY):
        super().__init__()
        self.show(LAYER['enemy'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()
        
        self.pos = vec((posX, posY))
        self.randPos = vec(rand.randint(64, WINWIDTH - 64), rand.randint(64, WINHEIGHT - 64))
        
        self.setImages("sprites/enemies/octogrunt.png", 64, 64, 1, 1, 0, 0)
        self.setRects(0, 0, 64, 64, 32, 32)

        #---------------------- Game stats & UI ----------------------#
        self.maxHp = 44
        initStats(self, 44, 10, 10, 90, 0.4)
    
    def movement(self, canShoot):
        if self.canUpdate and self.visible:
            if getTimeDiff(self.lastRelocate) > rand.uniform(2.5, 5.0):
                self.randPos.x = rand.randint(0, WINWIDTH)
                self.randPos.y = rand.randint(0, WINHEIGHT)
                self.lastRelocate = time.time()
            
            self.accel = self.getAccel()
            
            if canShoot == True:
                self.shoot(getClosestPlayer(self), 3, 1)
            
            self.accelMovement()

    def getAccel(self) -> pygame.math.Vector2:
        finalAccel = vec(0, 0)
        if self.pos.x != self.randPos.x or self.pos.y != self.randPos.y:
            if self.pos.x < self.randPos.x - self.hitbox.width:
                finalAccel.x += self.cAccel
            elif self.pos.x > self.randPos.x + self.hitbox.width:
                finalAccel.x -= self.cAccel
            else:
                pass

            if self.pos.y < self.randPos.y - self.hitbox.height:
                finalAccel.y += self.cAccel
            elif self.pos.y > self.randPos.y + self.hitbox.height:
                finalAccel.y -= self.cAccel
            else:
                pass

        return finalAccel

    def shoot(self, target, vel, shoot_time):
        if getTimeDiff(self.lastShot) > shoot_time:
            self.isShooting = True
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
        if self.canUpdate and self.visible and self.hp > 0:
            self.collideCheck(all_players, all_walls)
            self.movement(True)

            # Animation
            if getTimeDiff(self.lastFrame) > ANIMTIME:
                if self.isShooting:
                    self.index += 0
                    if self.index > 4:
                        self.index = 0
                    self.isShooting = False
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

    def __str__(self):
        return f'OctoGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xpWorth}\n'
    
    def __repr__(self):
        return f'OctoGrunt({self.pos}, {self.vel}, {self.accel}, {self.xpWorth})'