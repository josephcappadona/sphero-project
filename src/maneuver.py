import math
import time

def follow_path(sphero, path, speed, dist_constant=1):

    cur_pos = path[0]
    for next_pos in path[1:]:

        # compute distance and angle to next position
        print('%s -> %s' % (cur_pos, next_pos))
        dist, ang = compute_roll_parameters(cur_pos, next_pos)
        rolled = roll(sphero, speed, ang, dist*dist_constant)
        if not rolled:
            print('Something went wrong.')
            return False

        cur_pos = next_pos
    print('Path complete.')
    return True

def roll(sphero, speed, ang, time):
    return sphero.roll(speed, ang, time)

def compute_roll_parameters(old_pos, new_pos):

    x_1, y_1 = old_pos
    x_2, y_2 = new_pos
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)

    dist = math.sqrt(d_x**2 + d_y**2)
    ang = 90 - math.atan2(d_y, d_x) * (180/math.pi)

    return dist, ang
