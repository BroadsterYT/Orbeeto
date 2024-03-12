"""
Main program. Contains the game loop.
"""
import asyncio
import os
import sys
import time

import pygame
from pygame.locals import QUIT

import controls as ctrl
import screen
import text

import calculations as calc
import constants as cst
import groups
import rooms

pygame.init()
pygame.display.set_caption('Orbeeto')
pygame.display.set_icon(pygame.image.load(os.path.join(os.getcwd(), 'other/orbeeto.png')))

screen.buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
screen.viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED | pygame.RESIZABLE)


def redraw_game_window() -> None:
    """Draws all sprites onto the screen

    Returns:
        None
    """
    groups.all_sprites.update()
    groups.all_sprites.draw(screen.buffer_screen)
    main_room.update()
    screen.viewport.blit(screen.buffer_screen, calc.screen_shake_queue.run())
    pygame.display.update()

    screen.buffer_screen.fill((255, 255, 255))


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
main_room = rooms.Room(0, 0)


def check_key_release(event, is_mouse) -> None:
    """Checks if any input(s) has been released. If one has, then its count in key_released will be updated to match.

    Args:
        event:
        is_mouse: Are the inputs mouse buttons? True if yes, false if no.

    Returns:
        None
    """
    if not is_mouse:
        for input_key in ctrl.key_released.keys():
            if event.type == pygame.KEYUP and event.key == input_key:
                ctrl.key_released[input_key] += 1
    else:
        for button in ctrl.key_released.keys():
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                ctrl.key_released[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
prev_time = time.time()  # Used for delta time


async def main(max_frame_rate):
    loop = asyncio.get_event_loop()
    next_frame_target = 0.0
    sec_per_frame = 1 / max_frame_rate

    running = True
    while running:
        if sec_per_frame:
            # Framerate limiter
            delay = next_frame_target - time.time()
            if delay > 0:
                await asyncio.sleep(delay)
            next_frame_target = time.time() + sec_per_frame

        # Delta time
        global prev_time
        now = time.time()
        screen.dt = now - prev_time
        prev_time = now

        text.draw_text(f'{screen.dt}', 0, 0)

        for a_player in groups.all_players:
            if a_player.hp <= 0:
                pygame.quit()
                sys.exit()

        # ------------------------------- Redraw Window ------------------------------ #
        redraw_game_window()

        events_to_handle = list(pygame.event.get())
        events_handled = loop.create_task(handle_events(events_to_handle))
        await loop.run_in_executor(None, pygame.display.flip)  # noqa
        await events_handled


async def handle_events(events_to_handle):
    for any_event in events_to_handle:
        key_pressed = pygame.key.get_pressed()

        if any_event.type == QUIT or key_pressed[ctrl.K_PAUSE]:
            sys.exit()

        # Key input updating
        for key in ctrl.is_input_held.keys():
            if key in [1, 2, 3]:
                ctrl.is_input_held[key] = pygame.mouse.get_pressed(5)[key - 1]
            else:
                ctrl.is_input_held[key] = key_pressed[key]

        # Key release updating
        check_key_release(any_event, False)
        check_key_release(any_event, True)

        if any_event.type == pygame.MOUSEWHEEL:  # TODO: Implement this in players.py
            # Player ammo refill
            if main_room.player1.ammo < main_room.player1.max_ammo:
                main_room.player1.ammo += 1


if __name__ == '__main__':
    asyncio.run(main(cst.FPS))
