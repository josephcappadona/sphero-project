#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import math
import time

def follow_path(sphero, path, speed=0x88, time_constant=1):

    cur_pos = path[0]
    for next_pos in path[1:]:

        # compute distance and angle to next position, roll
        dist, ang = compute_roll_parameters(cur_pos, next_pos)
        _ = roll(sphero, speed, ang)
        time.sleep(dist * time_constant)

        # stop and wait for a moment
        _ = roll(sphero, 0, ang)
        time.sleep(0.5)
        cur_pos = next_pos

def roll(sphero, speed, ang):
    api_response = None
    sphero.roll(speed, ang, api_response)
    return api_response

def compute_roll_parameters(old_pos, new_pos):
    x_1, y_1 = old_pos
    x_2, y_2 = new_pos
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)
    dist = math.sqrt(d_x**2 + d_y**2)

    try:
        z = d_y / d_x
    except ZeroDivisionError:  # => d_x=0
        sign = int(d_y / abs(d_y))
        z = sign * math.inf
    ang = math.atan(z) * (180 / math.pi)

    return dist, ang
