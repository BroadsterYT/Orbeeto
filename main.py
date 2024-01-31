"""
Main
"""
import sys
import math

import pygame
from pygame.locals import *

import calculations as calc
import constants as cst
import controls as ctrl

import rooms
import groups

import screen

pygame.init()

clock = pygame.time.Clock()

screen.buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
screen.viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED, 0, 0, 2)
pygame.display.set_caption('Orbeeto')

vec = pygame.math.Vector2
rad = math.radians


# ============================================================================ #
#                              Redraw Game Window                              #
# ============================================================================ #
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
# Load room
main_room = rooms.Room(0, 0)


def check_key_release(is_mouse, *inputs) -> None:
    """Checks if any input(s) has been released. If one has, then its count in key_released will be updated to match.

    Args:
        is_mouse: Are the inputs mouse buttons? True if yes, false if no.
        *inputs: The input(s) to check
    """
    if not is_mouse:
        for input_key in inputs:
            if event.type == pygame.KEYUP and event.key == input_key:
                if input_key in ctrl.is_input_held and input_key in ctrl.key_released:
                    ctrl.key_released[input_key] += 1
    else:
        for button in inputs:
            if event.type == pygame.MOUSEBUTTONUP and event.button == button:
                if button in ctrl.is_input_held and button in ctrl.key_released:
                    ctrl.key_released[button] += 1


# ============================================================================ #
#                                   Main Loop                                  #
# ============================================================================ #
running = True
while running:
    for a_player in groups.all_players:
        if a_player.hp <= 0:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        keyPressed = pygame.key.get_pressed()

        if event.type == QUIT or keyPressed[K_ESCAPE]:
            sys.exit()

        ctrl.is_input_held = {
            1: pygame.mouse.get_pressed(5)[0],
            2: pygame.mouse.get_pressed(5)[1],
            3: pygame.mouse.get_pressed(5)[2],

            K_a: keyPressed[K_a],
            K_w: keyPressed[K_w],
            K_s: keyPressed[K_s],
            K_d: keyPressed[K_d],
            K_x: keyPressed[K_x],
            K_e: keyPressed[K_e],

            K_SPACE: keyPressed[K_SPACE],
        }

        check_key_release(False, K_a, K_w, K_s, K_d, K_e, K_x, K_SPACE)
        check_key_release(True, 1, 2, 3)

        if event.type == pygame.MOUSEWHEEL:
            # Player ammo refill
            if main_room.player1.ammo < main_room.player1.max_ammo:
                main_room.player1.ammo += 1

    screen.buffer_screen.fill((255, 255, 255))

    calc.draw_text(f'{main_room.player1}', 0, 0)

    # ------------------------------ Game Operation ------------------------------ #
    for portals in groups.all_portals:
        pygame.draw.rect(screen.viewport, cst.RED, portals.hitbox, 3)

    # ------------------------------- Redraw Window ------------------------------ #
    redraw_game_window()
    clock.tick_busy_loop(cst.FPS)
