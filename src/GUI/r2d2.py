import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import time
from utils import sin, cos
WHITE = (255, 255, 255)

class R2D2(pygame.sprite.Sprite):

    socket_delegate = None

    original_image = None
    name = 'R2D2'
    
    is_rolling = False
    time_started_rolling = None
    current_roll_duration = None
    current_dist_scale = None
    roll_direction = None
    count = 0

    speed = 0
    heading = 0
    stance = 2

    is_rotating = False
    heading_at_start = None
    current_rotate_arc = None
    rotate_speed = 3
    left_to_rotate = None
    rotate_direction = None
    time_started_rotate = None
    rotate_timing_delay = 0.15
    send_done_turning_response = True
    block_vertical = False
    block_horizontal = False

    def __init__(self, pos, width=50, height=50):
        super().__init__()
        x, y = pos

        self.image = pygame.Surface([width, height]).convert_alpha()
        self.image.fill((0,0,0,0))

        bipod_image = pygame.image.load('pics/r2d2_top_bipod.png').convert_alpha()
        bipod_image = pygame.transform.scale(bipod_image, (width, height))
        self.bipod_image = pygame.transform.rotozoom(bipod_image, 0, 1)

        tripod_image = pygame.image.load('pics/r2d2_top_tripod.png').convert_alpha()
        tripod_image = pygame.transform.scale(tripod_image, (width, height))
        self.tripod_image = pygame.transform.rotozoom(tripod_image, 0, 1)

        self.image = self.bipod_image.copy()

        self.rect = self.image.get_rect(x=x, y=y)
        self.my_x = self.rect.centerx
        self.my_y = self.rect.centery
        self.mask = pygame.mask.from_surface(self.image)

    def set_socket_delegate(self, sock):
        self.socket_delegate = sock

    def receive_data(self):
        if self.socket_delegate:
            return self.socket_delegate.receive_data()
    
    def handle_data(self, data):
        self.socket_delegate.handle_data(data, self)

    def receive_and_handle_data(self):
        data = self.receive_data()
        if data:
            self.handle_data(data)

    def set_center_position(self, x=None, y=None):
        if x != None:
            self.rect.centerx = x
            self.my_x = x
        if y != None:
            self.rect.centery = y
            self.my_y = y

    def roll(self, speed, roll_direction, duration, dist_scale=2):
        self.stop_rotate()
        if self.stance == 2:
            self.set_stance(1, send_response=False)
        if self.heading != (roll_direction % 360):
            self.image = pygame.transform.rotozoom(self.tripod_image if self.stance == 1 else self.bipod_image, -roll_direction, 1)
            self.heading = (roll_direction % 360)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = speed
        self.roll_direction = roll_direction
        self.is_rolling = True
        self.time_started_rolling = time.time()
        self.current_roll_duration = duration
        self.current_dist_scale = dist_scale

    def stop_roll(self, send_response=True):
        self.is_rolling = False
        self.time_started_rolling = None
        self.current_roll_duration = None
        self.current_dist_scale = None
        self.roll_direction = None
        self.count = 0
        if send_response and self.socket_delegate != None:
            self.socket_delegate.done_rolling()

    def stop_turn(self, send_response=True):
        self.is_rotating = False
        self.left_to_rotate = None
        self.rotate_direction = None
        if send_response and self.send_done_turning_response and self.socket_delegate != None:
            self.socket_delegate.done_turning()

    def update(self):

        if self.is_rotating:
            if self.left_to_rotate > 0:
                da = min(self.rotate_speed, self.left_to_rotate) * self.rotate_direction
                self.heading = (self.heading + da) % 360
                self.left_to_rotate -= abs(da)
                self.image = pygame.transform.rotozoom(self.tripod_image if self.stance == 1 else self.bipod_image, -self.heading, 1)
                self.rect = self.image.get_rect(center=self.rect.center)
            elif time.time() > self.time_started_rotate + self.rotate_timing_delay:
                self.stop_turn(send_response=self.send_done_turning_response)
 
        if self.is_rolling:
            is_done_rolling = time.time() - self.time_started_rolling > self.current_roll_duration
            if is_done_rolling:
                self.stop_roll()
            else:
                dist = self.current_dist_scale * self.speed
                dx = round(dist * cos(-self.roll_direction + 90), 2)
                dy = round(dist * sin(-self.roll_direction + 90), 2)

                if not self.block_horizontal:
                    self.my_x += dx
                if not self.block_vertical:
                    self.my_y -= dy
                self.rect.centerx = int(round(self.my_x, 0))
                self.rect.centery = int(round(self.my_y, 0))
                self.count += 1
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, degrees, send_response=True):
        self.send_done_turning_response = send_response
        self.stop_roll(send_response=False)
        self.is_rotating = True
        self.heading_at_start = self.heading
        self.current_rotate_arc = degrees
        self.left_to_rotate = abs(degrees)
        self.rotate_direction = 1 if degrees > 0 else -1
        self.time_started_rotate = time.time()

    def stop_rotate(self):
        self.is_rotating = False
        self.left_to_rotate = None
        self.rotate_direction = None

    def set_stance(self, stance, send_response=True):
        self.stance = stance
        if stance == 1:
            self.image = pygame.transform.rotozoom(self.tripod_image, -self.heading, 1)
        elif stance == 2:
            self.image = pygame.transform.rotozoom(self.bipod_image.copy(), -self.heading, 1)
        if send_response:
            self.socket_delegate.stance_set()

