from pygame.locals import *

# Keeps track of whether each input is held or not
is_input_held = {
    1: False,
    2: False,
    3: False,

    K_a: False,
    K_w: False,
    K_s: False,
    K_d: False,
    K_x: False,
    K_e: False
}

# Keeps track of the number of times each key has been released
key_released = {
    # Mouse
    1: 0,
    2: 0,
    3: 0,

    # Keyboard
    K_a: 0,
    K_w: 0,
    K_s: 0,
    K_d: 0,
    K_e: 0,
}
