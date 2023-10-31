from pygame import Vector2

from portals import *
from text import *
from visuals import *


class BulletBase(ActorBase):
    def __init__(self):
        """The base class for all projectiles"""        
        super().__init__()
        self.shotFrom = None
        self.ricCount = 1
        self.startTime = time.time()

        self.hit = None
        self.sideHit = None

    def get_vel(self) -> pygame.math.Vector2:
        room = get_room()
        final_vel = self.cVel + room.vel

        return final_vel

    def land(self, target) -> None:
        self.hit = target
        self.sideHit = triangle_collide(self, self.hit)
        self.ricCount -= 1

        boom_pos_x = 0
        boom_pos_y = 0

        # Bullet explodes
        if self.ricCount <= 0 or self.hit in all_enemies:
            if self.sideHit == SOUTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y + self.hit.hitbox.height // 2
            if self.sideHit == EAST:
                boom_pos_x = self.hit.pos.x + self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y
            if self.sideHit == NORTH:
                boom_pos_x = self.pos.x
                boom_pos_y = self.hit.pos.y - self.hit.hitbox.height // 2
            if self.sideHit == WEST:
                boom_pos_x = self.hit.pos.x - self.hit.hitbox.width // 2
                boom_pos_y = self.pos.y

            all_explosions.add(StdBulletExplode(self, boom_pos_x, boom_pos_y))
            self.kill()
        
        # Bullet ricochets
        else:
            room = get_room()
            room_vel = room.vel

            if self.sideHit == SOUTH:
                self.pos.y = self.hit.pos.y + self.hit.hitbox.height // 2 + self.hitbox.height // 2 + abs(room_vel.y)
                self.cVel.y = -self.cVel.y
                self.vel.y = -self.vel.y
                print(SOUTH)

            elif self.sideHit == EAST:
                self.pos.x = self.hit.pos.x + self.hit.hitbox.width // 2 + self.hitbox.width // 2 + abs(room_vel.x)
                self.cVel.x = -self.cVel.x
                self.vel.x = -self.vel.x
                print(EAST)

            elif self.sideHit == NORTH:
                self.pos.y = self.hit.pos.y - self.hit.hitbox.height // 2 - self.hitbox.height // 2 - abs(room_vel.y)
                self.cVel.y = -self.cVel.y
                self.vel.y = -self.vel.y
                print(NORTH)

            elif self.sideHit == WEST:
                self.pos.x = self.hit.pos.x - self.hit.hitbox.width // 2 - self.hitbox.width // 2 - abs(room_vel.x)
                self.cVel.x = -self.cVel.x
                self.vel.x = -self.vel.x
                print(WEST)

            self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))
    
    def proj_collide(self, sprite_group, can_hurt):
        """Destroys a given projectile upon a collision and renders an explosion

        ### Arguments
            - spriteGroup (``pygame.sprite.Group``): The group of the entity the projectile is colliding with
            - proj (``pygame.sprite.Sprite``): The projectile involved in the collision
            - canHurt (``bool``): Should the projectile calculate damage upon impact?
        """    
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, self.shotFrom, collidingSprite)
                if hasattr(collidingSprite, 'lastHit'):
                    collidingSprite.lastHit = time.time()
                self.land(collidingSprite)

            elif not can_hurt:
                if sprite_group == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)
                                self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))
                        return

                    elif len(all_portals) < 2:
                        self.land(collidingSprite)
                        return

                else:
                    self.land(collidingSprite)

    def inflict_damage(self, sprite_group, sender, receiver) -> None:
        """Executes the subtraction of ``hp`` after a sprite is struck by a projectile

        ### Arguments
            - spriteGroup (``pygame.sprite.Group``): The group that the receiving sprite is a member of
            - sender (``ActorBase``): The sprite that fired the projectile
            - receiver (``ActorBase``): The sprite being hit by the projectile
        """        
        damage = calculate_damage(sender, receiver, self)
        if sprite_group == all_enemies:
            if rand.randint(1, 20) == 1:
                receiver.hp -= damage * 3
                if damage > 0:
                    all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage * 3))
            else:
                receiver.hp -= damage
                if damage > 0:
                    all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage))

        elif sprite_group != all_enemies:
            receiver.hp -= damage
            if damage > 0:
                all_font_chars.add(DamageChar(receiver.pos.x, receiver.pos.y, damage))
            if hasattr(receiver, 'hitTime'):
                receiver.dodgeTime = 0
                receiver.lastHit = time.time()


# ============================================================================ #
#                                  Explosions                                  #
# ============================================================================ #
class StdBulletExplode(ActorBase):
    def __init__(self, proj: BulletBase, pos_x: float, pos_y: float):
        """An explosion that is displayed on-screen when a projectile hits something
        
        ### Arguments
            - proj (``BulletBase``): The projectile that is exploding
        """            
        super().__init__()
        self.show(LAYER['explosion'])
        self.owner = proj

        self.pos = vec((pos_x, pos_y))
        self.posOffset = vec(self.pos.x - self.owner.hit.pos.x, self.pos.y - self.owner.hit.pos.y)
        self.set_images('sprites/bullets/bullets.png', 32, 32, 8, 4, 0, 1)
        self.set_rects(self.pos.x, self.pos.y, 32, 32, 32, 32)

        self.render_images()
        self.randRotation = rand.randint(1, 360)

    def movement(self):
        self.center_rects()
        self.pos = self.owner.hit.hitbox.center + self.posOffset

    def update(self):
        self.movement()

        if get_time_diff(self.lastFrame) >= SPF:
            if self.index > 3:
                self.kill()
            else:
                self.render_images()
                self.index += 1
            self.lastFrame = time.time()

        # Give explosion its random rotation
        self.image = pygame.transform.rotate(self.origImage, self.randRotation)
        self.center_rects()

    def __repr__(self):
        return f'ProjExplode({self.owner}, {self.pos})'


# ============================================================================ #
#                                Player Bullets                                #
# ============================================================================ #
class PlayerStdBullet(BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
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

        self.shotFrom = shot_from

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.cVel = self.vel
        self.ricCount = bounce_count

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))
    
    def movement(self):
        if self.canUpdate:
            self.proj_collide(all_enemies, True)
            self.proj_collide(all_walls, False)
            self.proj_collide(all_portals, False)

            if get_time_diff(self.startTime) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(True)
            else:
                self.kill()

    def update(self):
        self.movement()

    def __repr__(self):
        return f'PlayerStdBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'


class PlayerLaserBullet(BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        super().__init__()
        self.show(LAYER['proj'])
        self.damage = PROJDMG[PROJ_LASER]

        self.shotFrom = shot_from

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.cVel = self.vel
        self.ricCount = bounce_count

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 1, 4)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 10, 10)

        self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))

    def movement(self):
        if self.canUpdate:
            self.proj_collide(all_enemies, True)
            self.proj_collide(all_walls, False)
            self.proj_collide(all_portals, False)

            if get_time_diff(self.startTime) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(True)
            else:
                self.kill()

    def update(self):
        self.movement()


# ------------------------------ Utility Bullets ----------------------------- #
class PortalBullet(BulletBase):
    pos: Vector2

    def __init__(self, shot_from, pos_x, pos_y, vel_x, vel_y):
        super().__init__()
        self.show(LAYER['proj'])
        
        self.shotFrom = shot_from

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.cVel = self.vel

        self.hitbox_adjust = vec(0, 0)
        self.damage = PROJDMG[PROJ_PORTAL]

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 5, 8)
        self.set_rects(-24, -24, 8, 8, 8, 8)

        # Rotate sprite to trajectory
        self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))

    def proj_collide(self, sprite_group, can_hurt: bool):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, self.shotFrom, collidingSprite)
                self.land(collidingSprite)

            elif not can_hurt:
                # If the projectile hits a portal
                if sprite_group == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.teleport(portal)

                elif sprite_group == all_walls:
                    self.land(collidingSprite)
                    self.__spawn_portal(collidingSprite)
                
                else:
                    self.land(collidingSprite)

    def __spawn_portal(self, surface):
        """Spawns a portal on the surface that the portal bullet hit.
        
        ### Arguments
            - wall (``ActorBase``): The sprite that the portal bullet hit
        """        
        side = wall_side_check(surface, self)
        if side == SOUTH:
            all_portals.add(Portal(self, self.pos.x, surface.pos.y + surface.hitbox.height // 2, side))
            portal_count_check()
        if side == NORTH:
            all_portals.add(Portal(self, self.pos.x, surface.pos.y - surface.hitbox.height // 2, side))
            portal_count_check()
        if side == EAST:
            all_portals.add(Portal(self, surface.pos.x + surface.hitbox.width // 2, self.pos.y, side))
            portal_count_check()
        if side == WEST:
            all_portals.add(Portal(self, surface.pos.x - surface.hitbox.width // 2, self.pos.y, side))
            portal_count_check()

    def movement(self):
        if self.canUpdate:
            self.proj_collide(all_walls, False)
            self.proj_collide(all_portals, False)

            if get_time_diff(self.startTime) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(False)
            else:
                self.kill()

    def update(self):
        if get_time_diff(self.lastFrame) > ANIMTIME:
            self.index += 1
            if self.index > 4:
                self.index = 0
            self.lastFrame = time.time()
        
        self.rotate_image(int(get_vec_angle(self.cVel.x, self.cVel.y)))
        self.movement()

    def __repr__(self):
        return f'PortalBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'


class NewGrappleBullet(BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float):
        super().__init__()
        self.show(LAYER['grapple'])
        self.damage = PROJDMG[PROJ_GRAPPLE]
        
        self.shotFrom = shot_from

        self.isHooked = False
        self.grappledTo = None
        self.posOffset = vec(0, 0)
        
        self.returning = False

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.cVel = self.vel
        self.accel = vec(0, 0)
        self.cAccel = 1.5

        self.chain = Beam(self, self.shotFrom)
        self.portalList = []

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 2, 16)
        self.set_rects(0, 0, 32, 32, 16, 16)
        self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))

    def land(self, grappled_to):
        if not self.returning:  # Hook won't scoop thing up on the way back to the player
            self.isHooked = True
            self.grappledTo = grappled_to
            self.grappledTo.grappledBy = self
            if self.grappledTo is not None:
                self.grappledTo.isGrappled = True
                self.posOffset = vec(self.pos.x - self.grappledTo.pos.x, self.pos.y - self.grappledTo.pos.y)

    def shatter(self):
        """Completely destroys the grappling hook.
        """
        self.returning = False
        self.shotFrom.grapple = None
        if self.grappledTo is not None:
            self.grappledTo.isGrappled = False

        self.portalList = []

        self.chain.kill()
        self.kill()

    def proj_collide(self, sprite_group, can_hurt):
        for collidingSprite in sprite_group:
            if not self.hitbox.colliderect(collidingSprite.hitbox):
                continue
            
            if not collidingSprite.visible:
                continue

            if can_hurt:
                self.inflict_damage(sprite_group, self.shotFrom, collidingSprite)
                self.land(collidingSprite)

            elif not can_hurt:
                if sprite_group == all_portals:
                    if len(all_portals) == 2:
                        for portal in all_portals:
                            if self.hitbox.colliderect(portal.hitbox):
                                self.portalList.append(portal); self.portalList.append(get_other_portal(portal))
                                self.teleport(portal)
                                self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))
                        return

                else:
                    self.land(collidingSprite)

    def send_back(self):
        if self.grappledTo not in all_walls:
            # Hook returns to portal it entered
            if len(self.portalList) > 1:
                angle = get_angle_to_sprite(self, self.portalList[1])
                room = get_room()
                room_accel = room.get_accel()
                self.accel.x = self.cAccel * -sin(rad(angle)) + room_accel.x
                self.accel.y = self.cAccel * -cos(rad(angle)) + room_accel.y
                # self.pos = self.grappledTo.pos

                if self.hitbox.colliderect(self.portalList[1]):
                    self.portalList = []
            
            # Hook returns to player
            else:
                angle = get_angle_to_sprite(self, self.shotFrom)
                room = get_room()
                room_accel = room.get_accel()
                self.accel.x = self.cAccel * -sin(rad(angle)) + room_accel.x
                self.accel.y = self.cAccel * -cos(rad(angle)) + room_accel.y

                # Hook disappears once it returns
                if self.hitbox.colliderect(self.shotFrom.hitbox):
                    self.shatter()
            
            self.accel_movement()

            # Hook follows whatever it has grabbed
            if self.grappledTo is not None and self.grappledTo not in all_portals:
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
                self.vel = self.get_vel()
                self.vel_movement(True)

            elif self.isHooked:
                if self.grappledTo is not None and self.grappledTo not in all_walls:
                    self.pos.x = self.grappledTo.pos.x
                    self.pos.y = self.grappledTo.pos.y
                
                elif self.grappledTo is not None and self.grappledTo in all_walls:
                    self.pos = self.grappledTo.pos + self.posOffset
                
                else:
                    self.pos = self.pos
        
        elif self.returning:
            self.send_back()

        self.center_rects()

    def bind_proj(self):
        if self.canUpdate and self.visible:
            if not self.isHooked:
                self.proj_collide(all_enemies, True)
                self.proj_collide(all_movable, False)
                self.proj_collide(all_portals, False)
                self.proj_collide(all_walls, False)
                self.proj_collide(all_drops, False)

            self.movement()

    def update(self):
        self.bind_proj()


# ============================================================================ #
#                                 Enemy Bullets                                #
# ============================================================================ #
class EnemyStdBullet(BulletBase):
    def __init__(self, shot_from, pos_x: float, pos_y: float, vel_x: float, vel_y: float, bounce_count: int = 1):
        """A projectile fired by an enemy that moves at a constant velocity

        ### Arguments
            - shotFrom (``ActorBase``): The player that the bullet was shot from
            - posX (``int``): The x-position where the bullet should be spawned
            - posY (``int``): The y-position where the bullet should be spawned
            - velX (``int``): The x-axis component of the bullet's velocity
            - velY (``int``): The y-axis component of the bullet's velocity
        """        
        super().__init__()
        self.show(LAYER['proj'])
        self.damage = PROJDMG[PROJ_STD]

        self.shotFrom = shot_from

        self.pos = vec((pos_x, pos_y))
        self.vel = vec(vel_x, vel_y)
        self.cVel = self.vel
        self.ricCount = bounce_count

        self.set_images("sprites/bullets/bullets.png", 32, 32, 8, 1)
        self.set_rects(self.pos.x, self.pos.y, 8, 8, 6, 6)

        self.rotate_image(get_vec_angle(self.vel.x, self.vel.y))
    
    def movement(self):
        if self.canUpdate:
            self.proj_collide(all_players, True)
            self.proj_collide(all_walls, False)
            self.proj_collide(all_portals, False)

            if get_time_diff(self.startTime) <= 10:
                self.vel = self.get_vel()
                self.vel_movement(True)
            else:
                self.kill()

    def update(self):
        self.movement()

    def __repr__(self):
        return f'EnemyStdBullet({self.shotFrom}, {self.pos}, {self.vel}, {self.ricCount})'
