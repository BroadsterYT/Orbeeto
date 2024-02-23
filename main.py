"""
Main program. Contains the game loop.
"""
import sys

import pygame
from pygame.locals import QUIT

import controls.key_trackers as kt
from controls.keybinds import *

import calculations as calc
import constants as cst
import groups
import rooms
import screen

pygame.init()

clock = pygame.time.Clock()

screen.buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
screen.viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED | pygame.RESIZABLE, 0, 0, 2)
pygame.display.set_caption('Orbeeto')

print(pygame.display.get_desktop_sizes())

def redraw_game_window():
    """Draws all sprites every frame.
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


def check_key_release(is_mouse) -> None:
    """Checks if any input(s) has been released. If one has, then its count in key_released will be updated to match.

    Args:
        is_mouse: Are the inputs mouse buttons? True if yes, false if no.

    Returns:
        None
    """
    if not is_mouse:
        for input_key in kt.key_released.keys():
            if event.type == pygame.KEYUP and event.key == input_key:
                kt.key_released[input_key] += 1
    else:
        for button in kt.key_released.keys():
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                kt.key_released[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
def main():
    """Main sequence"""
    running = True
    while running:
        for a_player in groups.all_players:
            if a_player.hp <= 0:
                pygame.quit()
                sys.exit()

        global event
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if event.type == QUIT or key_pressed[K_PAUSE]:
                sys.exit()

            # Key input updating
            for key in kt.is_input_held.keys():
                if key in [1, 2, 3]:
                    kt.is_input_held[key] = pygame.mouse.get_pressed(5)[key - 1]
                else:
                    kt.is_input_held[key] = key_pressed[key]

            # Key release updating
            check_key_release(False)
            check_key_release(True)

            if event.type == pygame.MOUSEWHEEL:
                # Player ammo refill
                if main_room.player1.ammo < main_room.player1.max_ammo:
                    main_room.player1.ammo += 1

        screen.buffer_screen.fill((255, 255, 255))

        # ------------------------------ Game Operation ------------------------------ #
        for portals in groups.all_portals:
            pygame.draw.rect(screen.viewport, cst.RED, portals.hitbox, 3)

        # ------------------------------- Redraw Window ------------------------------ #
        redraw_game_window()
        clock.tick_busy_loop(cst.FPS)


if __name__ == '__main__':
    main()
