import sys
import time
import r2d2_client
import courses
import a_star
import maneuver

# parse Sphero address
if len(sys.argv) != 3:
    print('USAGE:  python sphero.py ADDR PORT')
    exit()
addr = sys.argv[1]
port = sys.argv[2]

# connect to Sphero
r2d2 = r2d2_client.R2D2Client(addr, port)

# get course, find path
G = courses.grid_1
path = a_star.A_star(G, (0,0), (3,3))
speed = 0x88  # half speed

# traverse path
maneuver.follow_path(r2d2, path, speed, dist_constant=0.75)
r2d2.animate(10)
r2d2.quit()
