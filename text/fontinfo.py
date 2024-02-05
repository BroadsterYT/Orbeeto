"""
Contains the custom font class and all information about every custom font.
"""


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


# -------------------- Initialized Fonts -------------------- #
font1 = Font('sprites/ui/font.png', 9, 14, 37, 37)
font_small = Font('sprites/ui/small_font.png', 5, 7, 37, 37)

dialogue_font = Font('sprites/fonts/dialogue_font1.png', 32, 32, 26, 81)