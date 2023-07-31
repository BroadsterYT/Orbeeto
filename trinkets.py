import pygame

from class_bases import *

class ButtonBase(ActorBase):
    def __init__(self):
        super().__init__()
        self.activated = False


class Button(ButtonBase):
    def __init__(self, idValue: int, blockPosX: int, blockPosY: int):
        """A button that can be activated and deactivated
        
        ### Arguments
            - idValue (``int``): _description_
            - blockPosX (``int``): _description_
            - blockPosY (``int``): _description_
        """        
        super().__init__()
        self.show(LAYER['movable_layer'])
        all_trinkets.add(self)

        self.idValue = idValue
        self.pos = vec((blockPosX * 16, blockPosY * 16))

        self.setImages('sprites/trinkets/button.png', 64, 64, 2, 2)
        self.setRects(self.pos.x, self.pos.y, 64, 64, 64, 64)

    def __activeCheck(self) -> bool:
        isActive = False
        for box in all_movable:
            if not self.hitbox.colliderect(box.hitbox):
                return isActive
            else:
                isActive = True
                return isActive
    
    def getState(self):
        return self.__activeCheck()

    def update(self):
        if self.__activeCheck():
            self.index = 1
        elif not self.__activeCheck():
            self.index = 0
        
        self.renderImages()

    def __repr__(self):
        return f'Button({self.idValue}, {self.pos}, {self.__activeCheck()})'
