import pygame
import constants as cst

buffer_screen = pygame.Surface((cst.WINWIDTH, cst.WINHEIGHT))
viewport = pygame.display.set_mode((cst.WINWIDTH, cst.WINHEIGHT), pygame.SCALED, 0, 0, 1)

dt = 0.0
