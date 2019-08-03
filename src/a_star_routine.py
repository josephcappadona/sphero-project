import sys
import time
from client import DroidClient
import courses
from a_star import A_star
import maneuver


# connect to Sphero
agent_droid = DroidClient()
agent_droid.scan()
agent_droid.connect_to_droid('Q5-8CC0') # Agent

bad_droid_1 = DroidClient()
bad_droid_1.scan()
bad_droid_1.connect_to_droid('Q5-ACC0') # Bad Agent 1

bad_droid_2 = DroidClient()
bad_droid_2.scan()
bad_droid_2.connect_to_droid('Q5-8CC0') # Bad Agent 2

# get course, find path
G = courses.grid_1
start = (0,0)

# ☑ =start node, ☒ =goal node
# ☐ ══☐   ☐ ══☐
# ║   ║   ║   ║
# ☐   ☐ ══☐   ☐
# ║   ║   ║   ║
# ☐ ══☐   ☐ ══☐
# ║       ║   ║
# ☑   ☐ ══☐   ☒
goal = (3,0)
speed = 0x88  # half speed

while True:

    #  AGENT
    path = A_star(G, start, goal)
    maneuver.follow_path(agent_droid, path, speed, scale_dist = 0.75)#dist_constant=0.75)
    agent_droid.animate(10)
    agent_droid.quit()

    # BAD DROID 1
    path2 = move_enemy(G)
    maneuver.follow_path(bad_droid_1, path2, speed, scale_dist = 0.75)#dist_constant=0.75)
    bad_droid_1.animate(10)
    bad_droid_1.quit()

    # BAD DROID 2
    path3 = move_enemy(G)
    maneuver.follow_path(bad_droid_2, path3, speed, scale_dist = 0.75)#dist_constant=0.75)
    bad_droid_2.animate(10)
    bad_droid_2.quit()
