from telnetlib import Telnet
import time
import numpy as np
from math import sin, cos, pi

class R2D2Client:
    addr = '0.0.0.0'
    port = 0
    tn = None
    history = []
    awake = False
    position = np.zeros(2)  # measured in meters, accurate to within a few centimeters
    angle = 0  # measured in degrees
    stance = 2
    main_light = (0, 0, 0) #initial (r, g, b) values
    back_light = 0 #initial intensity value
    head_angle = 0

    def __init__(self, addr='127.0.0.1', port=1337):
        self.connect(addr, port)
        self.addr = addr
        self.port = port

    def connect(self, addr, port, timeout=10):
        self.tn = Telnet(addr, port, timeout)

        welcome = self.tn.read_until(b'\r\n', 15).decode().strip()
        print(welcome)  # "Connected to R2D2 server."

        looking = self.tn.read_until(b'\r\n', 10).decode().strip()
        print(looking)  # "Looking for R2D2..."

        connected = self.tn.read_until(b'\r\n', 10).decode().strip()
        print(connected)  # "Connected to R2D2!"

        ready = self.tn.read_until(b'\r\n', 10).decode().strip()
        print(ready)  # "Ready for commands!"

        if not (welcome and looking and connected and ready):
            print('Could not connect to R2D2. Try restarting the server.')
            self.tn.close()
            self.tn = None
        else:
            self.awake = True

    def send_command(self, command, wait=0):
        print('Command: ' + command)
        self.tn.write(command.encode())
        time.sleep(wait)  # certain commands (like animations and turning) receive responses right away; let's wait so we don't accidentally interrupt them
        response = self.tn.read_until(b'\r\n').decode().strip()
        print('Response: ' + response)
        self.history.append((command, response))
        return response

    def set_stance(self, stance):
        command = 'set_stance %d' % stance
        response = self.send_command(command, wait=2)  # takes about 2sec to change stance
        if response == 'Stance set.':
            self.stance = stance
            return True
        else:
            return False

    def roll(self, speed, angle, time): 
        speed = min(max(0, speed), 255)  # 0 <= speed <= 255
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
        response = self.send_command(command, wait=time)
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
        response = self.send_command(command, wait=0.5)
        if response == 'Done rolling.':
            self.angle = angle
            return (self.awake or woke) and (self.stance == 1 or stance_set)
        else:
            return False

    def animate(self, i, wait=3):
        command = 'animate %d' % i
        response = self.send_command(command, wait=wait)  # user should adjust `wait` based on animation
        return response == 'Animation complete.'

    def sleep(self):
        command = 'sleep'
        response = self.send_command(command, wait=1)
        if response == 'Asleep.':
            self.awake = False
            self.angle = 0
            self.stance = 2
            return True
        else:
            return False

    def wake(self):
        command = 'wake'
        response = self.send_command(command, wait=1)
        if response == 'Awake.':
            self.awake = True
            self.angle = 0
            self.stance = 2
            return True
        else:
            return False

    def quit(self):
        command = 'quit'
        try:
            response = self.send_command(command)
            return False
        except EOFError:
            self.tn.close()
            print('Connection closed.')
            return True

    def battery(self):
        command = 'battery'
        response = self.send_command(command)
        try:
            _ = float(response)
            return True
        except ValueError:
            return False

    def app_version(self):
        command = 'version'
        response = self.send_command(command)
        try:
            _ = float(response)
            return True
        except ValueError:
            return False

    #return the rgb values of the color, if it exists
    #else, return the input rgb values
    def color_to_rgb(self, color, r, g, b):
      if color == "black":
        return 0, 0, 0
      elif color == "white":
        return 255, 255, 255
      elif color == "red":
        return 255, 0, 0
      elif color == "orange":
        return 255,165,0
      elif color == "yellow":
        return 255,255,0
      elif color == "green":
        return 0,128,0
      elif color == "blue":
        return 0,0,255
      elif color == "purple":
        return 128,0,128
      else:
        #make sure the input values are valid
        r = min(max(0, r), 255) 
        g = min(max(0, g), 255)  
        b = min(max(0, b), 255)  
        return r, g, b

    def main_light_color(self, r = 0, g = 0, b = 0, color = ""):
        r, g, b = self.color_to_rgb(color, r, g, b)

        if not self.awake:  # if we are not awake
            woke = self.wake()  # then wake preemptively 

        command = 'set_main_led_color %d %d %d' % (r, g, b)
        response = self.send_command(command, wait=1)
        if response == 'Main LED set.':
            # update light vector
            self.main_light = (r, g, b)
            return True
        else:
            return False

    def back_light_intensity(self, intensity = 0):
        intensity = min(max(0, intensity), 255) 
        
        if not self.awake:  # if we are not awake
            woke = self.wake()  # then wake preemptively 

        command = 'set_back_led %d' % (intensity,)
        response = self.send_command(command, wait=1)
        if response == 'Back LED set.':
            # update light vector
            self.back_light = intensity
            return True
        else:
            return False

    def rotate_head(self, angle = 0):
      #the robot physically cannot turn between -160 and -180
      angle = min(max(-160, angle), 180) 

      if not self.awake:  # if we are not awake
            woke = self.wake()  # then wake preemptively 
      
      command = 'turn_dome %d' % (angle,)
      response = self.send_command(command, wait=1)
      if response == 'Back LED set.':
          # update head angle
          self.head_angle = angle
          return True
      else:
          return False