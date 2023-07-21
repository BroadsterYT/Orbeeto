import pygame

from class_bases import *
from portals import *
from text import *
from visuals import *
from init import *


class BulletBase(ActorBase):
    def __init__(self):
        """The base class for all projectiles
        """        
        super().__init__()
        self.ricCount = 1

    def land(self):
        self.ricCount -= 1

        if self.ricCount <= 0:
            all_explosions.add(ProjExplode(self))
            self.kill()
        else:
            # Cause the bullet to ricochet
            pass
    
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
                self.land()

            elif not canHurt:
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
                        return
                    
                    elif len(all_portals) < 2:
                        self.land()
                        return

                else:
                    self.land()

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



class PlayerBulletBase(BulletBase):
    def __init__(self):
        """The base class for all projectiles fired by players
        """        
        super().__init__()

    def bindProj(self):
        if self.canUpdate:
            if (
                self.pos.x < WINWIDTH and 
                self.pos.x > 0 and
                self.pos.y < WINHEIGHT and 
                self.pos.y > 0
            ):
                self.velMovement()
            else:
                self.kill()

            self.projCollide(all_enemies, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)


class EnemyBulletBase(BulletBase):
    def __init__(self):
        """The base class for all projectiles fired by enemies
        """        
        super().__init__()

    def bindProj(self):
        if self.canUpdate:
            if (
                self.pos.x < WINWIDTH and 
                self.pos.x > 0 and
                self.pos.y < WINHEIGHT and 
                self.pos.y > 0
            ):
                self.velMovement()
            else:
                self.kill()

            self.projCollide(all_players, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)


class ProjExplode(ActorBase):
    def __init__(self, proj: BulletBase):
        """An explosion that is displayed on-screen when a projectile hits something
        
        ### Arguments
            - proj (``BulletBase``): The projectile that is exploding
        """            
        super().__init__()
        self.show(LAYER['explosion_layer'])
        self.proj = proj
        
        self.spritesheet = Spritesheet("sprites/bullets/bullets.png", 8)
        self.index = 1

        if isinstance(proj, PlayerStdBullet) or isinstance(proj, EnemyStdBullet):
            self.images = self.spritesheet.get_images(32, 32, 4)
            self.original_images = self.spritesheet.get_images(32, 32, 4)

        elif isinstance(proj, PortalBullet):
            self.images = self.spritesheet.get_images(32, 32, 4)
            self.original_images = self.spritesheet.get_images(32, 32, 4)

        self.renderImages()
        self.rect = self.proj.rect
        self.randRotation = rand.randint(1, 360)

        self.pos = self.proj.pos

    def update(self):
        global anim_timer
        if isinstance(self.proj, PlayerStdBullet) or isinstance(self.proj, EnemyStdBullet):
            if anim_timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1

        elif isinstance(self.proj, PortalBullet):
            if anim_timer % 5 == 0:
                if self.index > 3:
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.original_image = self.original_images[self.index]
                    self.index += 1
        
        # Give explosion its random rotation
        self.image = pygame.transform.rotate(self.original_image, self.randRotation)
        self.rect = self.image.get_rect(center = self.rect.center)

    def __repr__(self):
        return f'ProjExplode({self.proj}, {self.pos})'

# ============================================================================ #
#                                Player Bullets                                #
# ============================================================================ #
class PlayerStdBullet(PlayerBulletBase):
    def __init__(self, shotFrom, posX: int, posY: int, velX: int, velY: int):
        """A projectile fired by a player that moves at a constant velocity

        ### Arguments
            - shotFrom (``Player``): The player that the bullet was shot from
            - posX (``int``): The x-position where the bullet should be spawned
            - posY (``int``): The y-position where the bullet should be spawned
            - velX (``int``): The x-axis component of the bullet's velocity
            - velY (``int``): The y-axis component of the bullet's velocity
        """        
        super().__init__()
        self.show(LAYER['proj_layer'])
        self.damage = PROJDMG[PROJ_STD]

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(-24, -24, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.bindProj()

    def __repr__(self):
        return f'PlayerStdBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'


class PortalBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY): 
        super().__init__()
        self.show(LAYER['proj_layer'])
        
        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.hitbox_adjust = vec(0, 0)
        self.damage = PROJDMG[PROJ_PORTAL]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 5, 4)
        self.setRects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def projCollide(self, spriteGroup, canHurt):
        for collidingSprite in spriteGroup:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if canHurt:
                self.inflictDamage(spriteGroup, self.shotFrom, collidingSprite)
                self.land()

            elif not canHurt:
                # If the projectile hits a portal
                if spriteGroup == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                        return
                    
                    elif len(all_portals) < 2:
                        self.land()
                        return

                elif spriteGroup == all_walls:
                    side = wallSideCheck(collidingSprite, self)
                    if side == SOUTH:
                        all_portals.add(Portal(self.pos.x, collidingSprite.pos.y + (collidingSprite.image.get_height() // 2), side))
                        portalCountCheck()
                    if side == NORTH:
                        all_portals.add(Portal(self.pos.x, collidingSprite.pos.y - (collidingSprite.image.get_height() // 2), side))
                        portalCountCheck()
                    if side == EAST:
                        all_portals.add(Portal(collidingSprite.pos.x + (collidingSprite.image.get_width() // 2), self.pos.y, side))
                        portalCountCheck()
                    if side == WEST:
                        all_portals.add(Portal(collidingSprite.pos.x - (collidingSprite.image.get_width() // 2), self.pos.y, side))
                        portalCountCheck()
                    self.land()
                
                else:
                    self.land()

    def bindProj(self):
        if self.canUpdate:
            if (
                self.pos.x < WINWIDTH and 
                self.pos.x > 0 and
                self.pos.y < WINHEIGHT and 
                self.pos.y > 0
            ):
                self.movement()
            else:
                self.kill()

            self.projCollide(all_enemies, True)
            self.projCollide(all_walls, False)
            self.projCollide(all_portals, False)

    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        if getTimeDiff(self.lastFrame) > ANIMTIME:
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.lastFrame = time.time()
        
        self.rotateImage(int(getVecAngle(self.vel.x, self.vel.y)))
        self.bindProj()

    def __repr__(self):
        return f'PortalBullet({self.shotFrom}, {self.pos}, {self.vel})'

class GrappleBullet(BulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYER['grapple'])
        all_projs.add(self)

        self.shotFrom = shotFrom
        self.damage = PROJDMG[PROJ_GRAPPLE]

        self.isHooked = False
        self.grappledTo: pygame.sprite.Sprite = None
        
        self.returning = False
        self.hasExitedPortal = False

        self.chain1: Beam = Beam(self.shotFrom, self)
        self.chain2: Beam = None

        self.canTp = True
        self.tpPoints = []

        self.enterPoint: InvisObj = None; self.enterPointFace = None
        self.exitPoint: InvisObj = None; self.exitPointFace = None

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)
        self.accel = vec(0, 0)
        self.cAccel = 0.7

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 2, 9)
        self.setRects(0, 0, 32, 32, 16, 16)
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))

    def land(self, grappledTo):
        self.isHooked = True
        self.grappledTo = grappledTo
        if self.grappledTo != None:
            self.grappledTo.isGrappled = True

    def shatter(self):
        """Destroys the grappling hook"""   
        self.shotFrom.grapple = None
        self.returning = False

        self.chain1.kill()
        if isinstance(self.chain2, Beam):
            self.chain2.kill()

        if isinstance(self.enterPoint, InvisObj):
            self.enterPoint.kill()
        if isinstance(self.exitPoint, InvisObj):
            self.exitPoint.kill()

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
                    if len(all_portals) == 2 and self.canTp:
                        self.tpPoints.append(copy.copy(self.pos))
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.canTp = False
                                self.tpPoints.append(copy.copy(self.pos))
                                
                                # Creating invisible objects at teleport points so grapple can return through portals
                                otherPortal: Portal = getOtherPortal(portal)
                                self.enterPointFace = portal.facing
                                self.exitPointFace = otherPortal.facing

                                ret1Pos: pygame.math.Vector2 = copy.copy(self.tpPoints[0])
                                ret2Pos: pygame.math.Vector2 = copy.copy(self.tpPoints[1])
                                self.enterPoint = InvisObj(ret1Pos.x, ret1Pos.y, 8, 8)
                                self.exitPoint = InvisObj(ret2Pos.x, ret2Pos.y, 8, 8)
                                
                                # Correcting chains
                                self.chain1.kill()
                                self.chain1: Beam = Beam(self.shotFrom, self.enterPoint)
                                self.chain2: Beam = Beam(self.exitPoint, self)
                        return
                    
                elif not self.canTp and spriteGroup == all_portals:
                    pass

                else:
                    self.land(collidingSprite)

    def bindProj(self):
        if can_update:
            self.movement()
            if (
                self.pos.x > WINWIDTH or 
                self.pos.x < 0 or
                self.pos.y > WINHEIGHT or 
                self.pos.y < 0
            ):
                self.land(None)

            if not self.isHooked:
                self.projCollide(all_enemies, True)
                self.projCollide(all_walls, False)
                self.projCollide(all_drops, False)
                self.projCollide(all_portals, False)

    def sendBack(self):
        """Sends the grappling hook back to the player"""
        if len(self.tpPoints) == 0:  
            angle = getAngleToSprite(self, self.shotFrom)
            self.accel.x = self.cAccel * -sin(rad(angle))
            self.accel.y = self.cAccel * -cos(rad(angle))

            if self.hitbox.colliderect(self.shotFrom.rect):
                self.shatter()

        if len(self.tpPoints) > 0:
            if not self.hasExitedPortal:
                angle = getAngleToSprite(self, self.exitPoint)
                self.accel.x = self.cAccel * -sin(rad(angle))
                self.accel.y = self.cAccel * -cos(rad(angle))

                if self.hitbox.colliderect(self.exitPoint.hitbox):
                    self.pos = self.enterPoint.pos
                    self.vel = getTpVel(self.exitPointFace, self.enterPointFace, self)
                    self.hasExitedPortal = True
                    self.chain2.kill()
            
            elif self.hasExitedPortal:
                angle = getAngleToSprite(self, self.shotFrom)
                self.accel.x = self.cAccel * -sin(rad(angle))
                self.accel.y = self.cAccel * -cos(rad(angle))
                if self.hitbox.colliderect(self.shotFrom.rect):
                    self.shatter()

        self.accelMovement()

    def movement(self):
        if not self.returning:
            if not self.isHooked:
                self.pos.x += self.vel.x
                self.pos.y += self.vel.y

            else:
                if self.grappledTo != None and self.grappledTo not in all_walls:
                    self.pos.x = self.grappledTo.pos.x
                    self.pos.y = self.grappledTo.pos.y
                
                elif self.grappledTo != None and self.grappledTo in all_walls:
                    side = wallSideCheck(self.grappledTo, self)
                    if side == SOUTH:
                        self.pos.x = self.pos.x
                        self.pos.y = self.grappledTo.pos.y + (self.grappledTo.rect.height // 2)
                    if side == NORTH:
                        self.pos.x = self.pos.x
                        self.pos.y = self.grappledTo.pos.y - (self.grappledTo.rect.height // 2)
                    if side == EAST:
                        self.pos.x = self.grappledTo.pos.x + (self.grappledTo.rect.width // 2)
                        self.pos.y = self.pos.y
                    if side == WEST:
                        self.pos.x = self.grappledTo.pos.x - (self.grappledTo.rect.width // 2)
                        self.pos.y = self.pos.y
                
                else:
                    self.pos = self.pos

        if self.returning:
            if self.grappledTo == None:
                self.sendBack()
            
            # Grapple will move if attached to an enemy or item
            if self.grappledTo != None and self.grappledTo not in all_walls:
                self.sendBack()
                self.grappledTo.pos.x = self.pos.x
                self.grappledTo.pos.y = self.pos.y

            if self.grappledTo != None and self.grappledTo in all_walls:
                if self.shotFrom.hitbox.colliderect(self.hitbox):
                    self.shatter()
                for wall in all_walls:
                    if self.shotFrom.hitbox.colliderect(wall.hitbox):
                        self.shatter()

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        if not self.isHooked and not self.returning:
            self.index = 0
            self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
        else:
            self.index = 1
            self.rotateImage(getAngleToSprite(self, self.shotFrom) + 180)
        
        self.bindProj()


# ============================================================================ #
#                                 Enemy Bullets                                #
# ============================================================================ #
class EnemyStdBullet(EnemyBulletBase):
    def __init__(self, shotFrom, posX, posY, velX, velY):
        super().__init__()
        self.show(LAYER['proj_layer'])

        self.shotFrom = shotFrom

        self.pos = vec((posX, posY))
        self.vel = vec(velX, velY)

        self.damage = PROJDMG[PROJ_STD]

        self.setImages("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.setRects(-24, -24, 8, 8, 6, 6)

        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
    
    def movement(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def update(self):
        self.rotateImage(getVecAngle(self.vel.x, self.vel.y))
        self.bindProj()
