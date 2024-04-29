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
import gamestack as gs
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
    gs.gamestack.update()
    screen.viewport.blit(screen.buffer_screen, calc.screen_shake_queue.run())
    pygame.display.flip()

    screen.buffer_screen.fill((255, 255, 255))


# ============================================================================ #
#                         Initialization for Main Loop                         #
# ============================================================================ #
main_room = rooms.Room(0, 0)
gs.s_action.groups.append(main_room)

# Pause menu
pause_menu = menus.PauseMenu()
pause_release = 0

inventory_menu = menus.InventoryMenu()
inventory_release = 0

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

        # ----- Opening and closing pause menu ----- #
        global pause_release
        if pause_release == ctrl.key_released[ctrl.K_PAUSE] - 1 and not pause_menu.is_open:
            gs.gamestack.push(gs.s_pause)
            pause_release = ctrl.key_released[ctrl.K_PAUSE]
            pause_menu.is_open = True

        elif pause_release == ctrl.key_released[ctrl.K_PAUSE] - 1 and pause_menu.is_open and gs.s_pause in gs.gamestack.stack:
            gs.gamestack.pop()
            pause_release = ctrl.key_released[ctrl.K_PAUSE]
            pause_menu.is_open = False

        elif pause_menu.is_open and gs.s_pause not in gs.gamestack.stack:
            pause_release = ctrl.key_released[ctrl.K_PAUSE]
            pause_menu.is_open = False
        pause_menu.update()

        # ----- Opening and closing inventory menu ----- #
        global inventory_release
        if inventory_release == ctrl.key_released[ctrl.K_MENU] - 1 and not inventory_menu.is_open:
            gs.gamestack.push(gs.s_inventory)
            inventory_release = ctrl.key_released[ctrl.K_MENU]
            inventory_menu.is_open = True

        elif inventory_release == ctrl.key_released[ctrl.K_MENU] - 1 and inventory_menu.is_open and gs.s_inventory in gs.gamestack.stack:
            gs.gamestack.pop()
            inventory_release = ctrl.key_released[ctrl.K_MENU]
            inventory_menu.is_open = False

        elif inventory_menu.is_open and gs.s_inventory not in gs.gamestack.stack:
            inventory_release = ctrl.key_released[ctrl.K_MENU]
            inventory_menu.is_open = False
        inventory_menu.update()

        # Draw framerate on screen
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
