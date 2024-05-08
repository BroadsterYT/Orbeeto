import pygame

import screen
import timer


class GameState:
    def __init__(self, name: str, update_call=None, *args, **kwargs):
        """A mode of gameplay that is placed into the game stack

        :param name: The mane of the game state
        :param update_call: A function to call every frame when the game state is at the top of the stack
        :param args: The arguments to pass into the update call
        :param kwargs: The keyword arguments to pass into the update call
        """
        self.name = name
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.groups = []

        self.update_call = update_call
        self.call_args = args
        self.call_kwargs = kwargs

    def __repr__(self):
        return f'GameState({self.name}, {self.all_sprites})'


s_action = GameState('action', timer.g_timer.update_current_time)
s_pause = GameState('pause', timer.g_timer.update_elapsed_time)
s_inventory = GameState('inventory', timer.g_timer.update_elapsed_time)


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

        # Calling function passed into game state at declaration
        if self.stack[-1].update_call is not None:
            self.stack[-1].update_call(*self.stack[-1].call_args, **self.stack[-1].call_kwargs)

    def __repr__(self):
        return f'GameStack({self.stack})'


gamestack = GameStack()
