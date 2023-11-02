from class_bases import *
from spritesheet import Spritesheet


class RightMenuArrow(ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the right.

        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.image = pygame.transform.scale(self.images[self.index], (64, 64))

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x - 32, pos_y - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it.
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        self.__animate()
        self.hover()

    def __animate(self):
        if get_time_diff(self.lastFrame) > SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.scale(self.images[self.index], (64, 64))
            self.index += 1
            self.lastFrame = time.time()


class LeftMenuArrow(ActorBase):
    def __init__(self, pos_x, pos_y):
        """A UI element that allows players to cycle through menu screens to the left.

        ### Arguments
            - ``posX`` ``(int)``: The x-position the element should be displayed at
            - ``posY`` ``(int)``: The y-position the element should be displayed at
        """
        super().__init__()
        self.pos = vec((pos_x, pos_y))
        self.return_pos = vec((pos_x, pos_y))

        self.spritesheet = Spritesheet("sprites/ui/menu_arrow.png", 8)
        self.images = self.spritesheet.get_images(64, 64, 61)
        self.index = 1

        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(pos_x - 32, pos_y - 32, 64, 64)

        self.rect.center = self.return_pos
        self.hitbox.center = self.return_pos

    def hover(self):
        """Causes the arrow to "hover" in place when the mouse cursor is above it
        """
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.pos.x = 5 * sin(time.time() * 15) + self.return_pos.x
        else:
            self.pos.x = self.return_pos.x

        self.rect.center = self.pos

    def update(self):
        if get_time_diff(self.lastFrame) >= SPF:
            if self.index > 60:
                self.index = 1

            self.image = pygame.transform.flip(pygame.transform.scale(self.images[self.index], (64, 64)), True, False)
            self.index += 1
            self.lastFrame = time.time()

        self.hover()


class MenuSlot(ActorBase):
    def __init__(self, owner, pos_x: float, pos_y: float, item_held: str | None):
        """A menu slot that shows the collected amount of a specific item.

        Args:
            owner: The owner of the inventory to whom the menu slot belongs to
            pos_x: The x-position to spawn at
            pos_y: The y-position to spawn at
            item_held: The item the menu slot will hold. Items are chosen from MATERIALS dictionary.
        """
        super().__init__()
        all_slots.add(self)
        self.owner = owner

        self.pos = vec((pos_x, pos_y))
        self.startPos = vec((pos_x, pos_y))
        self.holding = item_held
        self.count = 0

        self.menuSheet = Spritesheet("sprites/ui/menu_item_slot.png", 1)
        self.itemSheet = Spritesheet("sprites/textures/item_drops.png", 8)
        self.menuImages = self.menuSheet.get_images(64, 64, 1)

        self.index = 0

        self.menuImg = self.menuImages[0]

        self.images = self.create_slot_images()
        self.image: pygame.Surface = self.images[self.index]

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)

        self.center_rects()

    def hover(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            s_time = time.time()
            scale = abs(sin(s_time)) / 2
            self.image = pygame.transform.scale_by(self.images[self.index], 1 + scale)
            self.rect = self.image.get_rect(center=self.rect.center)

        else:
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_item_images(self) -> list:
        if self.holding == MAT[0]:
            return self.itemSheet.get_images(32, 32, 1, 0)
        elif self.holding == MAT[1]:
            return self.itemSheet.get_images(32, 32, 1, 1)
        else:
            return self.itemSheet.get_images(32, 32, 1, 0)

    def create_slot_images(self):
        """Combines the menu slot image with the images of the item and adds the player's collected amount of that
        item on top.

        Returns:
            list: A list of the created images
        """
        item_images = self.get_item_images()
        final_images = []
        if self.holding is not None:
            for frame in item_images:
                new_img = combine_images(self.menuImg, frame)

                # Adding the count of the item to its images
                count_surface = text_to_image(str(self.count), 'sprites/ui/font.png', 9, 14, 36)
                new_img.set_colorkey((0, 0, 0))
                center_x = (new_img.get_width() - frame.get_width()) // 2
                center_y = (new_img.get_height() - frame.get_height()) // 2
                new_img.blit(
                    swap_color(
                        swap_color(count_surface, (44, 44, 44), (156, 156, 156)), (0, 0, 1), (255, 255, 255)),
                    vec(center_x, center_y)
                )
                final_images.append(new_img)

        else:
            final_images.append(self.menuImg)

        return final_images

    def update(self):
        self.center_rects()

        if self.holding is not None:
            self.count = self.owner.inventory[self.holding]

        self.images = self.create_slot_images()
        self.hover()