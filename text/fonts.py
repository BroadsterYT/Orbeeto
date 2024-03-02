"""
Contains the custom font class and all information about every custom font.
"""
import os

import pygame
from pygame.math import Vector2 as vec

import constants as cst
import spritesheet


class Font:
    """
    Stores all the critical data of a font
    """
    def __init__(self, font_image_path: str, char_width: int, char_height: int, chars_per_row: int, char_count: int):
        """Stores all the critical data of a font.

        Args:
            font_image_path: The directory path of the image
            char_width: The width of each individual character
            char_height: The height of each individual character
            chars_per_row: The number of characters in each row of the font's sprite sheet
            char_count: The total number of characters in the font's sprite sheet
        """
        self.path = font_image_path
        self.char_width = char_width
        self.char_height = char_height
        self.chars_per_row = chars_per_row
        self.char_count = char_count


def text_to_image(any_text: str, a_font: Font) -> pygame.Surface:
    """Converts a string of text into an image with a given font.

    Args:
        any_text: The text string to convert into an image
        a_font: The font object to retrieve font data from

    Returns:
        pygame.Surface: The converted image
    """
    sheet = spritesheet.Spritesheet(a_font.path, a_font.chars_per_row)
    images = sheet.get_images(a_font.char_width, a_font.char_height, a_font.char_count)
    char_list = []

    final_image = pygame.Surface(vec(len(any_text) * a_font.char_width, a_font.char_height))

    # TODO: Make all fonts follow the same text-to-image logic
    if (a_font.path == os.path.join(os.getcwd(), 'sprites/ui/font.png') or
            a_font.path == os.path.join(os.getcwd(), 'sprites/ui/small_font.png')):
        for char in any_text:
            if char in cst.LETTERS.keys():
                char_list.append(images[cst.LETTERS[char]])
            elif char in cst.NUMBERS:
                char_list.append(images[int(char) + 26])
            elif char in cst.SYMBOLS:
                char_list.append(images[cst.SYMBOLS[char] + 36])
    else:
        for char in any_text:
            if char in cst.UPPERCASE.keys():
                char_list.append(images[cst.UPPERCASE[char]])
            elif char in cst.LOWERCASE.keys():
                char_list.append(images[cst.LOWERCASE[char]])
            elif char in cst.NEW_NUMBERS.keys():
                char_list.append(images[cst.NEW_NUMBERS[char]])
            elif char in cst.NEW_SYMBOLS.keys():
                char_list.append(images[cst.NEW_SYMBOLS[char]])

    count = 0
    for _ in char_list:
        final_image.blit(char_list[count], vec(count * a_font.char_width, 0))
        count += 1

    final_image.set_colorkey(cst.BLACK)
    return final_image


# -------------------- Initialized Fonts -------------------- #
font1 = Font(os.path.join(os.getcwd(), 'sprites/ui/font.png'), 9, 14, 37, 37)
font_small = Font(os.path.join(os.getcwd(), 'sprites/ui/small_font.png'), 5, 7, 37, 37)

dialogue_font = Font(os.path.join(os.getcwd(), 'sprites/fonts/dialogue_font1.png'), 32, 32, 26, 81)


if __name__ == '__main__':
    print(help(Font))