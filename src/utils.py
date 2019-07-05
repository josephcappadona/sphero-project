import os
from pynput import keyboard

def is_sudo():
    return os.getenv('SUDO_USER') != None

DIRECTION_KEYS = set([keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right])
