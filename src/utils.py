import os
from pynput import keyboard

DIRECTION_KEYS = set([keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right])

def is_sudo():
    return os.getenv('SUDO_USER') != None

def get_drive_mode_controls_text():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'drive_mode_controls.txt'), 'rt') as f:
        return f.read()
