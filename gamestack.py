import pygame

import screen


class GameState:
    def __init__(self, name: str):
        self.name = name
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.groups = []

    def __repr__(self):
        return f'GameState({self.name}, {self.all_sprites})'


s_action = GameState('action')
s_pause = GameState('pause')
s_inventory = GameState('inventory')


class GameStack:
    def __init__(self):
        self.stack = [
            s_action
        ]

    def push(self, gamestate: GameState) -> None:
        """Push a new gamestate to the top of the gamestack

        :param gamestate: The gamestate to push to the top of the gamestack
        :return: None
        """
        if gamestate in self.stack:
            print(f'{gamestate} cannot be added to stack because it is already in stack')
        else:
            self.stack.append(gamestate)

    def pop(self) -> None:
        if len(self.stack) == 1:
            raise RuntimeError(f'Cannot pop {self.stack[0]} from gamestack')
        self.stack.pop()

    def update(self):
        self.stack[-1].all_sprites.update()
        self.stack[-1].all_sprites.draw(screen.buffer_screen)

        for group in self.stack[-1].groups:
            group.update()

    def __repr__(self):
        return f'GameStack({self.stack})'


gamestack = GameStack()
