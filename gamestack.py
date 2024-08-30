import pygame

import screen
import timer


class GameLayer(pygame.sprite.LayeredUpdates):
    def __init__(self, *sprites, **kwargs):
        super().__init__(sprites, kwargs)  # noqa

    def draw(self, surface):
        """Updates version of

        LayeredUpdates.draw(surface): return Rect_list

        """
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect  # noqa
        for spr in [s for s in self.sprites() if s.in_gamestate]:
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect)
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


class GameState:
    def __init__(self, name: str, priority: int, update_call=None, *args, **kwargs):
        """A mode of gameplay that is placed into the game stack

        :param name: The name of the game state
        :param priority: The priority the gamestate takes. (ex. a priority 2 gamestate cannot be placed above a priority
        3 gamestate)
        :param update_call: A function to call every frame when the game state is at the top of the stack
        :param args: The arguments to pass into the update call
        :param kwargs: The keyword arguments to pass into the update call
        """
        self.name = name
        self.priority = priority
        self.all_sprites = GameLayer()
        self.groups = []

        self.update_call = update_call
        self.call_args = args
        self.call_kwargs = kwargs

    def __repr__(self):
        return f'GameState({self.name}, {self.all_sprites})'


s_action = GameState('action', 0,  timer.g_timer.update_current_time)
s_pause = GameState('pause', 2, timer.g_timer.update_elapsed_time)
s_settings = GameState('settings', 3, timer.g_timer.update_elapsed_time)
s_inventory = GameState('inventory', 1, timer.g_timer.update_elapsed_time)


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
        elif self.stack[-1].priority > gamestate.priority:
            print(f'Gamestate \"{gamestate.name}\" (priority {gamestate.priority}) cannot be placed on top of gamestate'
                  f' \"{self.stack[-1].name}\" (priority {self.stack[-1].priority})')
        else:
            self.stack.append(gamestate)

    def pop(self) -> None:
        if len(self.stack) == 1:
            raise RuntimeError(f'Cannot pop {self.stack[0]} from gamestack')
        self.stack.pop()

    def replace(self, old_gamestate: GameState, new_gamestate: GameState) -> None:
        """Replaces a gamestate in the gamestack with another. If the gamestate being replaced in the stack is not
        present, then a ValueError will be raised.

        :param old_gamestate: The gamestate being replaced
        :param new_gamestate:
        :return: None
        :raises ValueError: If the gamestate being replaced is not present in the gamestack
        """
        old_index = self.stack.index(old_gamestate)
        self.stack.insert(old_index, new_gamestate)
        self.stack.remove(old_gamestate)

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
