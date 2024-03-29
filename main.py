"""Main program. Contains the game loop."""
import asyncio
import os
import sys
import time

import pygame
from pygame.locals import QUIT

import controls as ctrl
import menus
import screen
import text

import audio as aux
import calculations as calc
import constants as cst
import groups
import rooms

pygame.init()
pygame.display.set_caption('Orbeeto')
pygame.display.set_icon(pygame.image.load(os.path.join(os.getcwd(), 'other/orbeeto.png')))

screen.buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
screen.viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED | pygame.RESIZABLE)

# Audio setup
aux.track_channel = pygame.mixer.Channel(1)


def redraw_game_window() -> None:
    """Draws all sprites onto the screen

    Returns:
        None
    """
    groups.all_sprites.update()
    groups.all_sprites.draw(screen.buffer_screen)
    main_room.update()
    screen.viewport.blit(screen.buffer_screen, calc.screen_shake_queue.run())
    pygame.display.flip()

    screen.buffer_screen.fill((255, 255, 255))


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
main_room = rooms.Room(0, 0)
pause_menu = menus.PauseMenu()
inventory_menu = menus.InventoryMenu()

last_pause_release = ctrl.key_released[ctrl.K_PAUSE]
prev_time = time.time()  # Used for delta time


async def main(max_frame_rate) -> None:
    """The main loop of the program.

    Args:
        max_frame_rate: The maximum framerate the game should run at
    """
    loop = asyncio.get_event_loop()
    next_frame_target = 0.0
    sec_per_frame = 1 / max_frame_rate

    running = True
    while running:
        # print(ctrl.is_input_held[4], ctrl.is_input_held[5])
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

        # Open pause menu
        if pause_menu.last_pause_release != ctrl.key_released[ctrl.K_PAUSE]:
            pause_menu.trigger()
            pause_menu.last_pause_release = ctrl.key_released[ctrl.K_PAUSE]

        # print(pause_menu.last_pause_release, ctrl.key_released[ctrl.K_PAUSE])

        # Update inventory menu
        inventory_menu.update()

        try:
            text.draw_text(f'{pow(screen.dt, -1)}', 0, 0)
        except ZeroDivisionError:
            pass

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


def check_mouse_scroll(event) -> None:
    """Checks if the mouse wheel is being scrolled up or down and updates ctrl.is_input_held accordingly

    Args:
        event: The Pygame event currently being evaluated
    """
    if event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
        ctrl.is_input_held[event.button] = True

    if event.type == pygame.MOUSEBUTTONUP and event.button in (4, 5):
        ctrl.is_input_held[event.button] = False


def check_key_release(event, is_mouse) -> None:
    """Checks if any input(s) has been released. If one has, then its count in key_released will be updated to match.

    Args:
        event: The Pygame event currently being evaluated
        is_mouse: Are the inputs mouse buttons? True if yes, false if no.
    """
    if not is_mouse:
        for input_key in ctrl.key_released.keys():
            if event.type == pygame.KEYUP and event.key == input_key:
                ctrl.key_released[input_key] += 1
    else:
        for button in ctrl.key_released.keys():
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                ctrl.key_released[button] += 1


async def handle_events(events_to_handle) -> None:
    """Handles the list of pygame events given

    Args:
        events_to_handle: The list of pygame events to handle
    """
    for event in events_to_handle:
        key_pressed = pygame.key.get_pressed()

        if event.type == QUIT:
            sys.exit()

        check_mouse_scroll(event)

        # Key input updating
        for key in ctrl.is_input_held.keys():
            if key in [1, 2, 3]:
                ctrl.is_input_held[key] = pygame.mouse.get_pressed(5)[key - 1]
            else:
                ctrl.is_input_held[key] = key_pressed[key]

        # Key release updating
        check_key_release(event, False)
        check_key_release(event, True)

        if event.type == pygame.MOUSEWHEEL:  # TODO: Implement this in players.py
            # Player ammo refill
            if main_room.player1.ammo < main_room.player1.max_ammo:
                main_room.player1.ammo += 1


if __name__ == '__main__':
    asyncio.run(main(cst.FPS))
