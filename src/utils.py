import sys,tty,os,termios

def get_drive_mode_controls_text():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'drive_mode_controls.txt'), 'rt') as f:
        return f.read()

special_key_mapping = {127: 'backspace',
                       10: 'return',
                       32: 'space',
                       9: 'tab',
                       27: 'esc',
                       65: 'up',
                       66: 'down',
                       67: 'right',
                       68: 'left'}
def get_key():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
                print("3 KEY1=%d %d %d" % (ord(b[0]), ord(b[1]), ord(b[2])))
            else:
                k = ord(b)
                print("%d KEY2=%d" % (len(b), k))
            
            return special_key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
