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
enemy1 = (3, 3)
enemy1_bound = (5, 6)

enemy2 = (4, 4)
enemy2_bound = (3, 4)
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
    path =  path[0:2]
    maneuver.follow_path(agent_droid, path, speed, scale_dist = 0.75)#dist_constant=0.75)

    G.update(new_obstacles, free_edges)

    # BAD DROID 1
    dest1 = G.move_enemy(enemy1, enemy1_bound)
    maneuver.follow_path(bad_droid_1, [enemy2, dest2], speed, scale_dist = 0.75)#dist_constant=0.75)
    enemy1 = dest1

    G.update(new_obstacles, free_edges)

    # BAD DROID 2
    dest2 = G.move_enemy(enemy1, enemy1_bound)
    maneuver.follow_path(bad_droid_2, [enemy3, dest3], speed, scale_dist = 0.75)#dist_constant=0.75)
    enemy2 = dest2

    G.update(new_obstacles, free_edges)
