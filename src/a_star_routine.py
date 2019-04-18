import sys
import time
import r2d2_client
import courses
import a_star
import maneuver


# connect to Sphero
r2d2 = r2d2_client.R2D2Client('127.0.0.1', 1337)

# get course, find path
G = courses.grid_1
start = (0,0)
goal = (3,0)
path = a_star.A_star(G, start, goal)

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
maneuver.follow_path(r2d2, path, speed, dist_constant=0.75)
r2d2.animate(10)
r2d2.quit()
