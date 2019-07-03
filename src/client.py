from telnetlib import Telnet
import time
import numpy as np
from math import sin, cos, pi

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

    def __init__(self, autoconnect=True):
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
        response = self.tn.read_until(b'\r\n', timeout).decode().strip()
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

    def set_stance(self, stance):
        command = 'set_stance %d' % stance
        response = self.send_and_receive(command, wait=2)  # takes about 2sec to change stance
        if response == 'Stance set.':
            self.stance = stance
            return True
        else:
            return False

    def roll(self, speed, angle, time): 
        speed = int(max(0, speed)*255)  # 0 <= speed <= 255
        angle = angle % 360  # 0 <= angle < 360
        time = max(0, time)  # time >= 0

        # prepare to roll
        if not self.awake:  # if we are not awake
            woke = self.wake()  # then wake preemptively so we don't waste roll time on waking
        if self.stance != 1:  # if we are not in the correct stance
            stance_set = self.set_stance(1)  # then change stance preemptively so we don't waste roll time changing stance
        if angle != self.angle:  # if we are not facing the correct direction
            turned = self.turn(angle)  # then turn preemptively so we don't waste roll time on turning

        command = 'roll %d %d %d' % (speed, angle, time*1000)
        response = self.send_and_receive(command, wait=time)
        if response == 'Done rolling.':
            # update position vector
            dist = max(0, speed * time * 0.002 - 0.02)  # accurate to ~1cm
            d_x = round(dist * sin((90-angle)*pi/180), 2)
            d_y = round(dist * cos((90-angle)*pi/180), 2)
            self.position += np.array([d_x, d_y])
            return (self.awake or woke) and (self.stance == 1 or stance_set) and (self.angle == angle or turned)
        else:
            return False

    def turn(self, angle):
        angle = angle % 360  # 0 <= angle < 360
        # prepare to turn
        if not self.awake:  # if we are not awake
            woke = self.wake()  # then wake preemptively so we don't waste turn time on waking
        if self.stance != 1:  # if we are not in the correct stance
            stance_set = self.set_stance(1)  # then change stance preemptively so we don't waste turn time changing stance
        command = 'roll 0 %d 500' % angle  # takes about 0.5sec to turn 180deg
        response = self.send_and_receive(command, wait=0.5)
        if response == 'Done rolling.':
            self.angle = angle
            return (self.awake or woke) and (self.stance == 1 or stance_set)
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


    def set_front_LED_colors(self, r, g, b): # 0 <= r,g,b <= 255

        command = 'set_front_led_color %d %d %d' % (r, g, b)
        response = self.send_and_receive(command, wait=1)

        if response == 'Front LED set.':
            self.front_LED_color = (r, g, b)
            return True
        else:
            return False

    def set_back_LED_colors(self, r, g, b): # 0 <= r,g,b <= 255

        command = 'set_back_led_color %d %d %d' % (r, g, b)
        response = self.send_and_receive(command, wait=1)

        if back_response == 'Back LED set.':
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
            return True
        else:
            return False

    def quit(self):
        command = 'quit'
        try:
            response = self.send_and_receive(command)
            return False
        except EOFError:
            self.tn.close()
            self.tn = None
            self.connected_to_droid = False
            print('Connection closed.')
            return True

    def close(self):
        return self.quit()

