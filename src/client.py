from telnetlib import Telnet
import time
import numpy as np
from math import sin, cos, pi
import atexit
from threading import Timer
from pynput import keyboard
import utils

class DroidClient:
    addr = '0.0.0.0'
    port = 0
    tn = None
    connected_to_droid = False
    history = []
    awake = False
    position = np.zeros(2)  # measured in meters, accurate to within a few centimeters
    angle = 0  # measured in degrees
    stance = 2
    waddling = False
    front_LED_color = (0, 0, 0)
    back_LED_color = (0, 0, 0)
    logic_display_intensity = 0
    holo_projector_intensity = 0
    drive_mode = False
    drive_mode_spreed = None
    drive_mode_angle = None
    drive_mode_shift = None

    def __init__(self, autoconnect=True):
        atexit.register(self.exit) # disconnect on quit if user did not manually disconnect
        if autoconnect:
            self.connect_to_server()

    def connect_to_server(self, addr='127.0.0.1', port=1337, timeout=10):
        self.tn = Telnet(addr, port, timeout)

        welcome = self.wait_for_response()

        if not welcome:
            print('Error communicating with the server. Try restarting the client and/or server.')
            self.tn.close()
            self.tn = None
        else:
            self.addr = addr
            self.port = port
            self.awake = True

    def send_and_receive(self, command, wait=0, **kwargs):
        self.send_command(command, wait=wait, **kwargs)
        response = self.wait_for_response(**kwargs)
        self.history.append((command, response))
        return response

    def send_command(self, command, wait=0, _print=True):
        self.tn.write(command.encode())
        if _print:
            print('Command: ' + command)
        time.sleep(wait)  # certain commands (like animations and turning) receive responses right away; let's wait so we don't accidentally interrupt them

    def wait_for_response(self, _print=True, timeout=15):

        while True:
            response = self.tn.read_until(b'\r\n', timeout).decode().strip()
            if response.startswith('Sensor Data:'):
                handle_sensor_data(response)
            else:
                break

        if _print:
            print('Response: ' + response)
        return response

    def scan(self):
        command = 'scan'
        scanning_response = self.send_and_receive(command)
        discovered_response = self.wait_for_response()
        return (scanning_response != '') and (discovered_response != '')

    def connect_to_droid(self, name):
        command = 'connect %s' % name
        response = self.send_and_receive(command, wait=2)
        if response == ('Connected to %s!' % name):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_R2D2(self):
        command = 'connect R2D2'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected to D2-'):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_R2Q5(self):
        command = 'connect R2Q5'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected to Q5-'):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_any(self):
        command = 'connect'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected to '):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def wake(self):
        command = 'wake'
        response = self.send_and_receive(command, wait=1)
        if response == 'Awake.':
            self.awake = True
            self.angle = 0
            self.stance = 2
            return True
        else:
            return False

    def sleep(self):
        command = 'sleep'
        response = self.send_and_receive(command, wait=1)
        if response == 'Asleep.':
            self.awake = False
            self.angle = 0
            self.stance = 2
            return True
        else:
            return False

    def set_stance(self, stance, **kwargs):
        if self.stance == stance:
            return True
        command = 'set_stance %d' % stance
        response = self.send_and_receive(command, wait=2, **kwargs)  # takes about 2sec to change stance
        if response == 'Stance set.':
            self.stance = stance
            return True
        else:
            return False

    def setup_for_roll(self, angle):
        if not self.awake:
            woke = self.wake()
        if self.stance != 1:
            stance_set = self.set_stance(1)
        if angle != self.angle:
            turned = self.turn(angle)

    def update_position_vector(self, speed, angle, time):
        dist = max(0, speed * time * 0.002 - 0.02)  # accurate to ~1cm
        d_x = round(dist * sin((90-angle)*pi/180), 2)
        d_y = round(dist * cos((90-angle)*pi/180), 2)
        self.position += np.array([d_x, d_y])


    def roll_time(self, speed, angle, time, turn=False):
        speed = speed           # 0 <= speed <= 1
        angle = angle % 360     # 0 <= angle < 360
        time = time             # time >= 0 (seconds)

        if not turn:
            self.setup_for_roll(angle)
        
        command = 'roll_time %d %d %d' % (speed, angle, time*1000)
        response = self.send_and_receive(command, wait=time)
        if response == 'Done rolling.':
            self.update_position_vector(speed, angle, time)
            self.angle = angle
            return True
        else:
            return False

    def roll_continuous(self, speed, angle, **kwargs):
        speed = speed
        angle = angle % 360

        command = 'roll_continuous %g %d' % (speed, angle)
        response = self.send_and_receive(command, **kwargs)
        if response == 'Initializing rolling.':
            self.angle = angle
            return True
        else:
            return False
    
    def stop_roll(self):
        self.roll_time(0, self.angle, 0)

    def turn(self, angle):
        angle = angle % 360  # 0 <= angle < 360
        return self.roll_time(0, angle, 0.5, turn=True)

    def animate(self, i, wait=3):
        command = 'animate %d' % i
        response = self.send_and_receive(command, wait=wait)  # user should adjust `wait` based on animation
        return response == 'Animation complete.'

    def set_waddle(self, waddle): # waddle = True/False
        waddleID = int(waddle) 

        command = 'set_waddle %d' % waddleID
        response = self.send_and_receive(command)
        if response == 'Waddle set.':
            self.waddle = waddle
            return True
        else:
            return False

    def play_sound(self, soundID, wait=4):
        
        command = 'play_sound %d' % soundID
        response = self.send_and_receive(command, wait=wait)
        if response:
            return True
        else:
            return False


    def set_front_LED_color(self, r, g, b): # 0 <= r,g,b <= 255

        command = 'set_front_led_color %d %d %d' % (r, g, b)
        response = self.send_and_receive(command, wait=1)

        if response == 'Front LED set.':
            self.front_LED_color = (r, g, b)
            return True
        else:
            return False

    def set_back_LED_color(self, r, g, b): # 0 <= r,g,b <= 255

        command = 'set_back_led_color %d %d %d' % (r, g, b)
        response = self.send_and_receive(command, wait=1)

        if response == 'Back LED set.':
            self.back_LED_color = (r, g, b)
            return True
        else:
            return False

    def set_holo_projector_intensity(self, intensity):
        intensity = intensity
        command = 'set_holo_intensity %d' % intensity
        response = self.send_and_receive(command)
        if response == 'Holo projector intensity set.':
            self.holo_projector_intensity = intensity
            return True
        else:
            return False

    def set_logic_display_intensity(self, intensity):
        intensity = intensity
        command = 'set_logic_intensity %d' % intensity
        response = self.send_and_receive(command)
        if response == 'Logic display intensity set.':
            self.holo_projector_intensity = intensity
            return True
        else:
            return False

    def battery(self):
        command = 'battery'
        response = self.send_and_receive(command)
        try:
            _ = float(response)
            return True
        except ValueError:
            return False

    def app_version(self):
        command = 'version'
        response = self.send_and_receive(command)
        try:
            _ = float(response)
            return True
        except ValueError:
            return False

    def help(self):
        command = 'help'
        response = self.send_and_receive(command)
        if response:
            return True
        else:
            return False

    def disconnect(self):
        command = 'disconnect'
        response = self.send_and_receive(command)
        if response:
            self.connected_to_droid = False
            return True
        else:
            return False

    def quit(self):
        try:
            self.disconnect()
            self.tn.close()
            return True
        except (EOFError, AttributeError):
            if self.tn:
                self.tn.close()
            self.tn = None
            self.connected_to_droid = False
            print('Connection closed.')
            return True

    def close(self):
        return self.quit()

    def exit(self):
        return self.quit()


    def enter_drive_mode(self):
        if not utils.is_sudo():
            print('Drive mode requires super user privilege.')
            return

        self.drive_mode_speed = 0
        self.drive_mode_angle = self.angle
        self.drive_mode_shift = False
      
        if self.connected_to_droid:
            print('\nPreparing for drive mode...\n')
            self.set_stance(1, _print=False)
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=True) as listener:
                self.drive_mode = True
                print('\nControls:\n%s\n\n' % utils.get_drive_mode_controls_text())
                print('Ready for keyboard input...\n')
                listener.join()
                print('Exiting drive move...\n')
                self.drive_mode = False
                self.drive_mode_speed = None
                self.drive_mode_angle = None
                self.drive_mode_shift = None
                self.set_stance(2, _print=False)
        else:
            print('You must connect to a droid before you can enter drive mode')

    def on_press(self, key):
        new_params = False
        try:
            #print('alphanum {0} pressed'.format(key.char))
            if key.char == 's':
                self.drive_mode_speed = 0
                new_params = True

        except AttributeError:
            #print('special {0} pressed'.format(key))
            speed_interval = 0.25 if self.drive_mode_shift else 0.1
            turn_interval = 45 if self.drive_mode_shift else 15
            if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                self.drive_mode_shift = True
            elif key == keyboard.Key.esc:
                self.roll_continuous(0, self.drive_mode_angle, _print=False)
                return False
            elif key in utils.DIRECTION_KEYS:
                if key == keyboard.Key.up:
                    self.drive_mode_speed = min(self.drive_mode_speed + speed_interval, 1)
                elif key == keyboard.Key.down:
                    self.drive_mode_speed = max(self.drive_mode_speed - speed_interval, 0)
                elif key == keyboard.Key.right:
                    self.drive_mode_angle = (self.drive_mode_angle + turn_interval) % 360
                elif key == keyboard.Key.left:
                    self.drive_mode_angle = (self.drive_mode_angle - turn_interval) % 360
                new_params = True
                
        if new_params:
            self.roll_continuous(self.drive_mode_speed, self.drive_mode_angle, _print=False)
        print()

    def on_release(self, key):
        #print('{0} released'.format(key))
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            self.drive_mode_shift = False

