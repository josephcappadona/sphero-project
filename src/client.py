from telnetlib import Telnet
import time
import numpy as np
from math import sin, cos, pi
import atexit
from threading import Timer
from pynput import keyboard
import utils
from threading import Timer

class DroidClient:
    addr = '0.0.0.0'
    port = 0
    tn = None
    connected_to_droid = False
    history = []
    awake = False
    #position = np.zeros(2)  # measured in meters, accurate to within a few centimeters
    angle = 0  # measured in degrees
    stance = 2
    waddling = False
    front_LED_color = (0, 0, 0)
    back_LED_color = (0, 0, 0)
    logic_display_intensity = 0
    holo_projector_intensity = 0
    roll_continuous = False
    roll_continuous_params = None
    drive_mode = False
    drive_mode_spreed = None
    drive_mode_angle = None
    drive_mode_shift = None
    continuous_roll_timer = None

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
        self.tn.write((command+'\r\n').encode())
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
        if response.startswith('Connected'):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_R2D2(self):
        command = 'connect R2D2'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected'):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_R2Q5(self):
        command = 'connect R2Q5'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected'):
            ready_response = self.wait_for_response()
            self.connected_to_droid = True
            return True
        else:
            return False

    def connect_to_any(self):
        command = 'connect'
        response = self.send_and_receive(command, wait=2)
        if response.startswith('Connected'):
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
        if angle != None and angle != self.angle:
            turned = self.turn(angle)

    def update_position_vector(self, speed, angle, time):
        dist = max(0, speed * time * 0.002 - 0.02)  # accurate to ~1cm
        d_x = round(dist * sin((90-angle)*pi/180), 2)
        d_y = round(dist * cos((90-angle)*pi/180), 2)
        self.position += np.array([d_x, d_y])

    def roll(self, speed, angle, time):
        return self.roll_time(speed, angle, time)

    def roll_time(self, speed, angle, time, **kwargs):

        self.setup_for_roll(angle)
        
        command = 'roll_time %g %d %g' % (speed, angle, time)
        response = self.send_and_receive(command, wait=time, **kwargs)
        if response == 'Done rolling.':
            #self.update_position_vector(speed, angle, time)
            self.angle = angle
            if speed == 0:
                self.is_continuous_roll = False
                self.roll_continuous_params = None
            return True
        else:
            return False

    def roll_continuous(self, speed, angle, **kwargs):
        if self.continuous_roll_timer:
            self.continuous_roll_timer.cancel()
            self.continuous_roll_timer = None
       
        self.setup_for_roll(None)

        command = 'roll_continuous %g %d' % (speed, angle)
        response = self.send_and_receive(command, **kwargs)
        if response == 'Initializing rolling.':
            self.angle = angle
            if speed > 0:
                self.is_continuous_roll = True
                self.roll_continuous_params = (speed, angle)
                self.continuous_roll_timer = Timer(1.5, self.restart_continuous_roll)
                self.continuous_roll_timer.start()
            return True
        else:
            return False

    def restart_continuous_roll(self):
        if self.continuous_roll_timer:
            self.continuous_roll_timer.cancel()
            self.continuous_roll_timer = None
        if self.is_continuous_roll:
            speed, angle = self.roll_continuous_params
            self.roll_continuous(speed, angle, _print=False)

    def stop_roll(self, **kwargs):
        if self.continuous_roll_timer:
            self.continuous_roll_timer.cancel()
            self.continuous_roll_timer = None
        self.roll_time(0, self.angle, 0, **kwargs)
        self.is_continuous_roll = False
        self.roll_continuous_params = None

    def turn(self, angle, **kwargs):
        angle = min(angle - self.angle, (angle - self.angle) % 360, key=lambda x: abs(x))

        self.setup_for_roll(None)

        command = 'turn %d' % angle
        response = self.send_and_receive(command, **kwargs)
        if response == 'Done turning.':
            self.angle = angle
            return True
        else:
            return False

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
        try:
            self.set_stance(2, _print=False)
            command = 'disconnect'
            response = self.send_and_receive(command)
            if response:
                self.connected_to_droid = False
                return True
            else:
                return False
        except:
            print('Disconnected.')
            return True

    def quit(self):
        try:
            if self.connected_to_droid:
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
        if self.connected_to_droid:
            print('\nPreparing for drive mode...\n')
            self.set_stance(1, _print=False)

            self.drive_mode = True
            print('\nControls:\n%s\n' % utils.get_drive_mode_controls_text())
            print('Ready for keyboard input...\n')

            speed, angle = 0, self.angle
            while True:
                key = utils.get_key()
                break_, speed, angle = self.process_key(key, speed, angle)
                if break_:
                    break

            print('Exiting drive move...\n')
            self.drive_mode = False
            self.set_stance(2, _print=False)
        else:
            print('You must connect to a droid before you can enter drive mode')

    def process_key(self, key, prev_speed, prev_angle, speed_interval=0.1, turn_interval=15):
        new_params = False
        next_speed, next_angle = prev_speed, prev_angle

        if key == 's':
            next_speed = 0
            new_params = True

        elif key == 'esc':
            next_speed = 0
            self.stop_roll()
            return True, next_speed, next_angle

        elif key in ['left', 'right', 'up', 'down']:
            if key == 'up':
                next_speed = round(min(prev_speed + speed_interval, 1), 1)
            elif key == 'down':
                next_speed = round(max(prev_speed - speed_interval, 0), 1)
            elif key == 'right':
                next_angle = (prev_angle + turn_interval) % 360
            elif key == 'left':
                next_angle = (prev_angle - turn_interval) % 360
            new_params = True
                
        if new_params:
            if next_speed > 0 or next_angle != prev_angle:
                self.roll_continuous(next_speed, next_angle, _print=False)
            else:
                self.stop_roll(_print=False)
            print('Speed: %g' % next_speed)
            print('Heading: %d' % next_angle)
        print()
        return False, next_speed, next_angle


