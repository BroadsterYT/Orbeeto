import bullets
from itemdrops import *
from statbars import *


class EnemyBase(ActorBase):
    def __init__(self):
        """The base class for all enemy objects. It gives you better control over enemy objects."""
        super().__init__()
        self.pos = vec((0, 0))
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

        self.isShooting = False

        # -------------------- In-game Stats --------------------#
        self.maxHp = None
        self.hp = None
        self.maxAtk = None
        self.atk = None
        self.maxDef = None
        self.defense = None
        self.xpWorth = None

        self.healthBar = HealthBar(self)

    def set_stats(self, hp: int, attack: int, defense: int, xp: int):
        self.maxHp = hp
        self.hp = hp
        self.maxAtk = attack
        self.atk = attack
        self.maxDef = defense
        self.defense = defense
        self.xpWorth = xp

    def award_xp(self):
        for a_player in all_players:
            a_player.xp += self.xpWorth
            a_player.update_level()
            a_player.update_max_stats()

    def drop_items(self, table_index):
        drops = LTDROPS[table_index]
        row = rand.randint(0, 2)
        column = rand.randint(0, 2)
        
        for item in drops[row][column]:
            all_drops.add(
                ItemDrop(self, item)
            )


class StandardGrunt(EnemyBase):
    def __init__(self, pos_x: float, pos_y: float):
        """A simple enemy that moves to random locations and shoots at players.

        Args:
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
        """
        super().__init__()
        self.show(LAYER['enemy'])
        all_enemies.add(self)

        self.lastRelocate = time.time()
        self.lastShot = time.time()

        self.pos = vec((pos_x, pos_y))
        self.randPos = vec(rand.randint(64, WINWIDTH - 64), rand.randint(64, WINHEIGHT - 64))

        self.set_room_pos()

        self.set_images('sprites/enemies/standard_grunt.png', 64, 64, 5, 5, 0, 0)
        self.set_rects(0, 0, 64, 64, 32, 32)

        # ---------------------- Game stats & UI ----------------------#
        self.set_stats(15, 10, 10, 40)

# --------------------------------- Movement --------------------------------- #
    def movement(self, can_shoot: bool = True):
        if self.canUpdate and self.hp > 0:
            self.__set_rand_pos()
            self.accel = self.get_accel()
            self.set_room_pos()
            
            if can_shoot:
                self.shoot(get_closest_player(self), 6, rand.uniform(0.4, 0.9))

            self.accel_movement()

    def __set_rand_pos(self):
        """Assigns a random value within the proper range for the enemy to travel to.
        """
        if get_time_diff(self.lastRelocate) > rand.uniform(2.5, 5.0):
            self.randPos.x = rand.randint(self.image.get_width(), WINWIDTH - self.image.get_width())
            self.randPos.y = rand.randint(self.image.get_height(), WINHEIGHT - self.image.get_height())

            pass_check = True
            # If the assigned random position is within a border or wall, it will run again and assign a new one.
            for border in all_borders:
                if border.hitbox.collidepoint(self.randPos.x, self.randPos.y):
                    pass_check = False

            for wall in all_walls:
                if wall.hitbox.collidepoint(self.randPos.x, self.randPos.y):
                    pass_check = False
            
            if pass_check:
                self.lastRelocate = time.time()

    def get_accel(self) -> pygame.math.Vector2:
        room = get_room()
        final_accel = vec(0, 0)

        final_accel += room.get_accel()

        if self.pos.x != self.randPos.x or self.pos.y != self.randPos.y:
            # Moving to proper x-position
            if self.pos.x < self.randPos.x - self.hitbox.width // 2:
                final_accel.x += self.cAccel
            if self.pos.x > self.randPos.x + self.hitbox.width // 2:
                final_accel.x -= self.cAccel

            # Moving to proper y-position
            if self.pos.y < self.randPos.y - self.hitbox.height // 2:
                final_accel.y += self.cAccel
            if self.pos.y > self.randPos.y + self.hitbox.height // 2:
                final_accel.y -= self.cAccel

        return final_accel

# ---------------------------------- Actions --------------------------------- #
    def shoot(self, target, vel: float, shoot_time: float) -> None:
        """Shoots a bullet at a specific velocity at a specified interval.

        Args:
            target: The target the enemy is firing at
            vel: The velocity of the bullet
            shoot_time: How often the enemy should fire
        """
        if get_time_diff(self.lastShot) > shoot_time:
            self.isShooting = True
            try:
                angle = get_angle_to_sprite(self, target)
            except ValueError:
                angle = 0

            cos_angle = cos(rad(angle))
            sin_angle = sin(rad(angle))

            vel_x = vel * -sin_angle
            vel_y = vel * -cos_angle
            offset = vec(21, 30)

            all_projs.add(
                bullets.EnemyStdBullet(self,
                                       self.pos.x - (offset.x * cos_angle) - (offset.y * sin_angle),
                                       self.pos.y + (offset.x * sin_angle) - (offset.y * cos_angle),
                                       vel_x,
                                       vel_y)
                )
            self.lastShot = time.time()

# --------------------------------- Updating --------------------------------- #
    def update(self):
        if self.canUpdate and self.visible and self.hp > 0:
            self.collide_check(all_players, all_walls)

            # Animation
            self.__animate()
            self.rotate_image(get_angle_to_sprite(self, get_closest_player(self)))

        if self.hp <= 0:
            self.drop_items(0)
            self.award_xp()
            self.kill()

    def __animate(self):
        if get_time_diff(self.lastFrame) > ANIMTIME:
            if self.isShooting:
                self.index += 1
                if self.index > 4:
                    self.index = 0
                    self.isShooting = False
            self.lastFrame = time.time()

    def __str__(self):
        return f'StandardGrunt at {self.pos}\nvel: {self.vel}\naccel: {self.accel}\nxp worth: {self.xpWorth}'

    def __repr__(self):
        return f'StandardGrunt({self.pos}, {self.vel}, {self.accel}, {self.xpWorth})'
