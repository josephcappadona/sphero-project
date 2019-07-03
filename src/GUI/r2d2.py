import pygame
import time
import math
WHITE = (255, 255, 255)

class R2D2(pygame.sprite.Sprite):

    original_image = None
    
    is_rolling = False
    time_started_rolling = None
    current_roll_duration = None
    current_dist_scale = None
    roll_direction = None
    count = 0

    speed = 0
    heading = 0

    is_rotating = False
    heading_at_start = None
    current_rotate_arc = None
    rotate_speed = 3
    left_to_rotate = None
    rotate_direction = None
    time_started_rotate = None
    rotate_timing_delay = 0.15

    def __init__(self, width=492, height=654, scale=0.15):
        super().__init__()
        width, height = int(width*scale), int(height*scale)

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        image = pygame.image.load('r2d2.png').convert_alpha()
        self.image = pygame.transform.scale(image, (width, height))
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.my_x = self.rect.centerx
        self.my_y = self.rect.centery

    def set_center_position(self, x=None, y=None):
        if x != None:
            self.rect.centerx = x
            self.my_x = x
        if y != None:
            self.rect.centery = y
            self.my_y = y

    def roll(self, speed, roll_direction, duration, dist_scale=3):
        self.stop_rotate()
        self.speed = speed
        self.roll_direction = self.heading + roll_direction
        self.is_rolling = True
        self.time_started_rolling = time.time()
        self.current_roll_duration = duration
        self.current_dist_scale = dist_scale

    def stop_roll(self):
        self.is_rolling = False
        self.time_started_rolling = None
        self.current_roll_duration = None
        self.current_dist_scale = None
        self.roll_direction = None
        self.count = 0

    def update(self):

        if self.is_rotating:
            if self.left_to_rotate > 0:
                da = min(self.rotate_speed, self.left_to_rotate) * self.rotate_direction
                #self.image = pygame.transform.rotate(self.image, da)
                self.heading = (self.heading + da) % 360
                self.left_to_rotate -= abs(da)
                self.image = pygame.transform.rotozoom(self.original_image, -self.heading, 1)
                self.rect = self.image.get_rect(center=self.rect.center)
            elif time.time() > self.time_started_rotate + self.rotate_timing_delay:
                self.is_rotating = False
                self.left_to_rotate = None
                self.rotate_direction = None
 
        if self.is_rolling:
            is_done_rolling = time.time() - self.time_started_rolling > self.current_roll_duration
            if is_done_rolling:
                self.stop_roll()
            else:
                dist = self.current_dist_scale * self.speed
                dx = round(dist * math.cos((-self.roll_direction + 90) * math.pi/180), 2)
                dy = round(dist * math.sin((-self.roll_direction + 90) * math.pi/180), 2)

                #dx_int = int(dx)
                #dx_frac = dx - dx_int
                #dx_sgn = 1 if dx > 0 else -1
                #if abs(dx_frac) > 0.05 and (self.count % 10) / 10 > dx_sgn * dx_frac:
                #    dx_int += dx_sgn

                #dy_int = int(dy)
                #dy_frac = dy - dy_int
                #dy_sgn = 1 if dy > 0 else -1
                #if abs(dy_frac) > 0.05 and (self.count % 10) / 10 > dy_sgn * dy_frac:
                #    dy_int += dy_sgn

                print('\nrect.x', self.rect.x)
                print('rect.y', self.rect.y)
                print('dx: ', round(dist * math.cos((self.roll_direction + 90) * math.pi/180), 2))
                print('roll_dir:', self.roll_direction)
                self.my_x += dx
                self.my_y -= dy
                self.rect.centerx = int(round(self.my_x, 0))
                self.rect.centery = int(round(self.my_y, 0))
                self.count += 1

    def rotate(self, degrees):
        self.stop_roll()
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


    def move_right(self, pixels):
        self.rect.x += pixels

    def move_left(self, pixels):
        self.rect.x -= pixels

    def move_up(self, pixels):
        self.rect.y -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels
