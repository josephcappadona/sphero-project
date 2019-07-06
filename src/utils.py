import sys,tty,os,termios

def get_drive_mode_controls_text():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'drive_mode_controls.txt'), 'rt') as f:
        return f.read()

arrow_key_mapping = {65: 'up',
                     66: 'down',
                     67: 'right',
                     68: 'left'}
regular_key_mapping = {27: 'esc',
                       9: 'tab',
                       32: 'space',
                       10: 'return',
                       127: 'backspace'}
def get_key():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
                return arrow_key_mapping.get(k, None)
            else:
                k = ord(b)
                return regular_key_mapping.get(k, chr(k))
            
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
