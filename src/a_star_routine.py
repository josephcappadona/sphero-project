import sys
import time
from client import DroidClient
import courses
from a_star import A_star
import maneuver


# connect to Sphero
droid = DroidClient()
droid.scan()
droid.connect_to_droid('Q5-8CC0')
#droid.connect_to_R2D2()

# get course, find path
G = courses.grid_1
start = (0,0)
goal = (3,0)
path = A_star(G, start, goal)

# ☑ =start node, ☒ =goal node
# ☐ ══☐   ☐ ══☐
# ║   ║   ║   ║
# ☐   ☐ ══☐   ☐
# ║   ║   ║   ║
# ☐ ══☐   ☐ ══☐
# ║       ║   ║
# ☑   ☐ ══☐   ☒

# traverse path
speed = 0x88  # half speed
maneuver.follow_path(droid, path, speed, scale_dist = 0.75)#dist_constant=0.75)
droid.animate(10)
droid.quit()
