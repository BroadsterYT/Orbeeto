"""
Contains all the dialogue in the game.
"""
RED = '\u2764'
YELLOW = '\U0001F49B'

SKIP = {
    RED, YELLOW
}


def style_text(text: str, *styles: str) -> str:
    style_list = []
    for style in styles:
        style_list.append(style)

    all_styles = ''.join(style_list)

    # Separating each character in the input text
    text_list = []
    for char in text:
        text_list.append(char)

    final_text = all_styles + all_styles.join(text_list[char] for char in range(0, len(text_list)))
    return final_text


all_dialogue_lines = {
    'error': [
        'The dialog function\nencountered an ' +
        style_text('error', RED) + '.',
        'Check your code.'
    ],

    'default': [
        '> There\'s nothing to ' + style_text('observe.', RED)
    ],

    'box_test': [
        'There\'s a box here.'
    ],
}


if __name__ == '__main__':
    pass
