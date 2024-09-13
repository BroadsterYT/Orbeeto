"""
Contains the custom font class and all information about every custom font.
"""
import os

import pygame
from pygame.math import Vector2 as vec

import constants as cst
import spritesheet


class Font:
    """Stores all the critical data of a font"""
    def __init__(self, font_image_path: str, char_width: int, char_height: int, chars_per_row: int, char_count: int):
        """Stores all the critical data of a font.

        :param font_image_path: The directory path of the image
        :param char_width: The width of each individual character
        :param char_height: The height of each individual character
        :param chars_per_row: The number of characters in each row of the font's sprite sheet
        :param char_count: The total number of characters in the font's sprite sheet
        """
        self.path = font_image_path
        self.char_width = char_width
        self.char_height = char_height
        self.chars_per_row = chars_per_row
        self.char_count = char_count


indicator_font = Font(os.path.join(os.getcwd(), 'sprites/fonts/font.png'), 9, 14, 26, 81)
font_small = Font(os.path.join(os.getcwd(), 'sprites/fonts/small_font.png'), 5, 7, 26, 81)
dialogue_font = Font(os.path.join(os.getcwd(), 'sprites/fonts/dialogue_font1.png'), 32, 32, 26, 81)

# ------------------------------ Text-to-image mapping ------------------------------ #
TEXT_MAP = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13,
    'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,

    'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38,
    'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50, 'z': 51,

    '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61,

    '.': 62, '!': 63, '\'': 64, ',': 65, ';': 66, ':': 67, '/': 68, '\\': 69, '\"': 70, '~': 71, '?': 72, '(': 73,
    ')': 74, '[': 75, ']': 76, '{': 77, '}': 78, '<': 79, '>': 80
}


def text_to_image(any_text: str, a_font: Font) -> pygame.Surface:
    """Converts a string of text into an image with a given font.

    :param any_text: The text string to convert into an image
    :param a_font: The font object to retrieve font data from
    :return: The converted image
    """
    sheet = spritesheet.Spritesheet(a_font.path, a_font.chars_per_row)
    images = sheet.get_images(a_font.char_width, a_font.char_height, a_font.char_count)
    char_list = []

    final_image = pygame.Surface(vec(len(any_text) * a_font.char_width, a_font.char_height))

    for char in any_text:
        if char in TEXT_MAP.keys():
            char_list.append(images[TEXT_MAP[char]])
        elif char == ' ':
            char_list.append(pygame.Surface(vec(a_font.char_width, a_font.char_height)))
        else:
            pass  # TODO: Add underscore, hyphen, and pound to fonts

    count = 0
    for _ in char_list:
        final_image.blit(char_list[count], vec(count * a_font.char_width, 0))
        count += 1

    final_image.set_colorkey(cst.BLACK)
    return final_image


def text_to_image_test(any_text: str, a_font: Font, space: int = 0) -> pygame.Surface:
    """Converts a string of text into an image with a given font.

    :param any_text: The text string to convert into an image
    :param a_font: The font object to retrieve font data from
    :return: The converted image
    """
    sheet = spritesheet.Spritesheet(a_font.path, a_font.chars_per_row)
    images = sheet.get_images(a_font.char_width, a_font.char_height, a_font.char_count)
    char_list = []




if __name__ == '__main__':
    print(help(Font))
