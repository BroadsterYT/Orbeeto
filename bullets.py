import pygame
import os

from class_bases import *
from portals import *
from text import *
from visuals import *


class BulletBase(ActorBase):
    def __init__(self):
        """The base class for all projectiles
        """        
        super().__init__()
        self.ricCount = 1
        self.startTime = time.time()

    def getVel(self) -> pygame.math.Vector2:
        room = self.getRoom()
        finalVel = self.cVel + room.vel

        return finalVel

    def land(self, target: pygame.sprite.Sprite):
        self.hit = target
        self.sideHit = triangleCollide(self, self.hit)
        self.ricCount -= 1

        # Bullet explodes
        if self.ricCount <= 0 or self.hit in all_enemies:
            if self.sideHit == SOUTH:
                boomPosX = self.pos.x
                boomPosY = self.hit.pos.y + self.hit.hitbox.height // 2
            if self.sideHit == EAST:
                boomPosX = self.hit.pos.x + self.hit.hitbox.width // 2
                boomPosY = self.pos.y
            if self.sideHit == NORTH:
                boomPosX = self.pos.x
                boomPosY = self.hit.pos.y - self.hit.hitbox.height // 2
            if self.sideHit == WEST:
                boomPosX = self.hit.pos.x - self.hit.hitbox.width // 2
                boomPosY = self.pos.y

            all_explosions.add(ProjExplode(self, boomPosX, boomPosY))
            self.kill()
        
        # Bullet ricochets
        else:
            room = self.getRoom()
            roomVel = room.vel

            if self.sideHit == SOUTH:
                self.pos.y = self.hit.pos.y + self.hit.hitbox.height // 2 + self.hitbox.height // 2 + abs(roomVel.y)
                self.cVel.y = -self.cVel.y
                self.vel.y = -self.vel.y
                print(SOUTH)

            elif self.sideHit == EAST:
                self.pos.x = self.hit.pos.x + self.hit.hitbox.width // 2 + self.hitbox.width // 2 + abs(roomVel.x)
                self.cVel.x = -self.cVel.x
                self.vel.x = -self.vel.x
                print(EAST)

            elif self.sideHit == NORTH:
                self.pos.y = self.hit.pos.y - self.hit.hitbox.height // 2 - self.hitbox.height // 2 - abs(roomVel.y)
                self.cVel.y = -self.cVel.y
                self.vel.y = -self.vel.y
                print(NORTH)

            elif self.sideHit == WEST:
                self.pos.x = self.hit.pos.x - self.hit.hitbox.width // 2 - self.hitbox.width // 2 - abs(roomVel.x)
                self.cVel.x = -self.cVel.x
                self.vel.x = -self.vel.x
                print(WEST)

            self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def projCollide(self, spriteGroup, canHurt):
        """Destroys a given projectile upon a collision and renders an explosion

        ### Arguments
            - spriteGroup (``pygame.sprite.Group``): The group of the entity the projectile is colliding with
            - proj (``pygame.sprite.Sprite``): The projectile involved in the collision
            - canHurt (``bool``): Should the projectile calculate damage upon impact?
        """    
        for collidingSprite in spriteGroup:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if canHurt:
                self.inflictDamage(spriteGroup, self.shotFrom, collidingSprite)
                self.land(collidingSprite)

            elif not canHurt:
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
                        return
                    
                    elif len(all_portals) < 2:
                        self.land(collidingSprite)
                        return

                else:
                    self.land(collidingSprite)

    def inflictDamage(self, spriteGroup: pygame.sprite.Group, sender: ActorBase, receiver: ActorBase) -> None:
        """Executes the subtraction of ``hp`` after a sprite is struck by a projectile
        
        ### Arguments
            - spriteGroup (``pygame.sprite.Group``): The group that the receiving sprite is a member of
            - sender (``ActorBase``): The sprite that fired the projectile
            - receiver (``ActorBase``): The sprite being hit by the projectile
        """        
        damage = calculateDamage(sender, receiver, self)
        if spriteGroup == all_enemies:
            if rand.randint(1, 20) == 1:
                receiver.hp -= damage * 3
                if damage > 0:
                    all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage * 3))
            else:
                receiver.hp -= damage
                if damage > 0:
                    all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage))

        elif spriteGroup != all_enemies:
            receiver.hp -= damage
            if damage > 0:
                all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage))
            if hasattr(receiver, 'hitTime'):
                receiver.hitTime = 0
                receiver.lastHit = time.time()


class ProjExplode(ActorBase):
    def __init__(self, proj: BulletBase, posX: float, posY: float):
        """An explosion that is displayed on-screen when a projectile hits something
        
        ### Arguments
            - proj (``BulletBase``): The projectile that is exploding
        """            
        super().__init__()
        self.show(LAYER['explosion'])
        self.owner = proj

        self.pos = vec((posX, posY))
        self.posOffset = vec(self.pos.x - self.owner.hit.pos.x, self.pos.y - self.owner.hit.pos.y)

        if isinstance(proj, PlayerStdBullet) or isinstance(proj, EnemyStdBullet):
            self.setImages('sprites/bullets/bullets.png', 32, 32, 8, 4, 0, 1)

        elif isinstance(proj, PortalBullet):
            self.setImages('sprites/bullets/bullets.png', 32, 32, 8, 4, 0, 1)

        elif isinstance(proj, NewGrappleBullet):
            self.setImages('sprites/bullets/bullets.png', 32, 32, 8, 4, 0, 1)

        self.renderImages()
        self.setRects(self.pos.x, self.pos.y, 32, 32, 32, 32)
        self.randRotation = rand.randint(1, 360)

    def movement(self):
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        self.pos = self.owner.hit.hitbox.center + self.posOffset

    def update(self):
        self.movement()

        if isinstance(self.owner, PlayerStdBullet) or isinstance(self.owner, EnemyStdBullet):
            if getTimeDiff(self.lastFrame) >= SPF:
                if self.index > 3:
                    self.kill()
                else:
                    self.renderImages()
                    self.index += 1
                self.lastFrame = time.time()

        elif isinstance(self.owner, PortalBullet):
            if getTimeDiff(self.lastFrame) >= SPF:
                if self.index > 3:
                    self.kill()
                else:
                    self.renderImages()
                    self.index += 1
                self.lastFrame = time.time()

        elif isinstance(self.owner, NewGrappleBullet):
            if getTimeDiff(self.lastFrame) >= SPF:
                if self.index > 3:
                    self.kill()
                else:
                    self.renderImages()
                    self.index += 1
                self.lastFrame = time.time()
        
        # Give explosion its random rotation
        self.image = pygame.transform.rotate(self.origImage, self.randRotation)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def __repr__(self):
        return f'ProjExplode({self.owner}, {self.pos})'


# ============================================================================ #
#                                Player Bullets                                #
# ============================================================================ #
class PlayerStdBullet(BulletBase):
    def __init__(self, shotFrom, posX: int, posY: int, velX: int, velY: int, bounceCount: int = 1):
        """A projectile fired by a player that moves at a constant velocity

        ### Arguments
            - shotFrom (``Player``): The player that the bullet was shot from
            - posX (``int``): The x-position where the bullet should be spawned
            - posY (``int``): The y-position where the bullet should be spawned
            - velX (``int``): The x-axis component of the bullet's velocity
            - velY (``int``): The y-axis component of the bullet's velocity
        """        
        super().__init__()
        self.show(LAYER['proj'])
        self.damage = PROJDMG[PROJ_STD]

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.cVel = self.vel
        self.ricCount = bounceCount

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        if self.canUpdate:
            self.projCollide(all_enemies, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)

            if getTimeDiff(self.startTime) <= 10:
                self.vel = self.getVel()
                self.velMovement(True)
            else:
                self.kill()

    def update(self):
        self.movement()

    def __repr__(self):
        return f'PlayerStdBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'


class PortalBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY): 
        super().__init__()
        self.show(LAYER['proj'])
        
        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.cVel = self.vel

        self.hitbox_adjust = vec(0, 0)
        self.damage = PROJDMG[PROJ_PORTAL]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 5, 4)
        self.setRects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def projCollide(self, spriteGroup, canHurt: bool):
        for collidingSprite in spriteGroup:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if canHurt:
                self.inflictDamage(spriteGroup, self.shotFrom, collidingSprite)
                self.land(collidingSprite)

            elif not canHurt:
                # If the projectile hits a portal
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)

                elif spriteGroup == all_walls:
                    self.land(collidingSprite)
                    self.__spawnPortal(collidingSprite)
                
                else:
                    self.land(collidingSprite)

    def __spawnPortal(self, surface: ActorBase):
        """Spawns a portal on the surface that the portal bullet hit.
        
        ### Arguments
            - wall (``ActorBase``): The sprite that the portal bullet hit
        """        
        side = wallSideCheck(surface, self)
        if side == SOUTH:
            all_portals.add(Portal(self, self.pos.x, surface.pos.y + surface.hitbox.height // 2, side))
            portalCountCheck()
        if side == NORTH:
            all_portals.add(Portal(self, self.pos.x, surface.pos.y - surface.hitbox.height // 2, side))
            portalCountCheck()
        if side == EAST:
            all_portals.add(Portal(self, surface.pos.x + surface.hitbox.width // 2, self.pos.y, side))
            portalCountCheck()
        if side == WEST:
            all_portals.add(Portal(self, surface.pos.x - surface.hitbox.width // 2, self.pos.y, side))
            portalCountCheck()

    def movement(self):
        if self.canUpdate:
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)

            if getTimeDiff(self.startTime) <= 10:
                self.vel = self.getVel()
                self.velMovement(False)
            else:
                self.kill()

    def update(self):
        if getTimeDiff(self.lastFrame) > ANIMTIME:
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.lastFrame = time.time()
        
        self.rotateImage(int(getVecAngle(self.vel.x, self.vel.y)))
        self.movement()

    def __repr__(self):
        return f'PortalBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'


class NewGrappleBullet(BulletBase):
    def __init__(self, shotFrom, posX: float, posY: float, velX: float, velY: float):
        super().__init__()
        self.show(LAYER['grapple'])
        self.damage = PROJDMG[PROJ_GRAPPLE]
        
        self.shotFrom = shotFrom

        self.isHooked = False
        self.grappledTo = None
        self.posOffset = vec(0, 0)
        
        self.returning = False

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.accel = vec(0, 0)
        self.cAccel = 1.5

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 2, 9)
        self.setRects(0, 0, 32, 32, 16, 16)
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def land(self, grappledTo):
        self.isHooked = True
        self.grappledTo = grappledTo
        if self.grappledTo != None:
            self.grappledTo.isGrappled = True
            self.posOffset = vec(self.pos.x - self.grappledTo.pos.x, self.pos.y - self.grappledTo.pos.y)

    def shatter(self):
        """Completely destroys the grappling hook"""        
        self.returning = False
        self.shotFrom.grapple = None
        self.kill()

    def projCollide(self, spriteGroup, canHurt):
        for collidingSprite in spriteGroup:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if canHurt:
                self.inflictDamage(spriteGroup, self.shotFrom, collidingSprite)
                self.land(collidingSprite)

            elif not canHurt:
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
                        return

                else:
                    self.land(collidingSprite)

    def sendBack(self):
        if self.grappledTo not in all_walls:
            # Hook returns to player
            angle = getAngleToSprite(self, self.shotFrom)
            room = self.getRoom()
            roomAccel = room.getAccel()
            self.accel.x = self.cAccel * -sin(rad(angle)) + roomAccel.x
            self.accel.y = self.cAccel * -cos(rad(angle)) + roomAccel.y

            # Hook disappears once it returns
            if self.hitbox.colliderect(self.shotFrom.hitbox):
                self.shatter()
            
            self.accelMovement()

            # Hook follows whatever it has grabbed
            if self.grappledTo != None and self.grappledTo not in all_portals:
                if self.grappledTo not in all_walls:
                    self.grappledTo.pos = self.pos

        # Player should accelerate to the hook
        else:
            self.pos = self.grappledTo.pos + self.posOffset
            if self.hitbox.colliderect(self.shotFrom.hitbox):
                self.shatter()

    def movement(self):
        if not self.returning:
            if not self.isHooked:
                self.pos.x += self.vel.x
                self.pos.y += self.vel.y

            elif self.isHooked:
                if self.grappledTo != None and self.grappledTo not in all_walls:
                    self.pos.x = self.grappledTo.pos.x
                    self.pos.y = self.grappledTo.pos.y
                
                elif self.grappledTo != None and self.grappledTo in all_walls:
                    self.pos = self.grappledTo.pos + self.posOffset
                
                else:
                    self.pos = self.pos
        
        elif self.returning:
            self.sendBack()

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def bindProj(self):
        if self.canUpdate and self.visible:
            if not self.isHooked:
                self.projCollide(all_enemies, True)
                self.projCollide(all_movable, False)
                self.projCollide(all_portals, False)
                self.projCollide(all_walls, False)
                self.projCollide(all_drops, False)

            self.movement()

    def update(self):
        self.bindProj()


# ============================================================================ #
#                                 Enemy Bullets                                #
# ============================================================================ #
class EnemyStdBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYER['proj'])

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.cVel = self.vel

        self.damage = PROJDMG[PROJ_STD]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(-24, -24, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        if getTimeDiff(self.startTime) <= 10:
            self.vel = self.getVel()
            self.velMovement(True)
        else:
            self.kill()

    def bindProj(self):
        if self.canUpdate:
            self.projCollide(all_players, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)

            self.movement()

    def update(self):
        self.bindProj()

    def __repr__(self):
        return f'EnemyStdBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'
    

if __name__ == '__main__':
    os.system('python main.py')