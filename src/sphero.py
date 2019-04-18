#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import time
import maneuver
import r2d2_client

# parse Sphero address
if len(sys.argv) != 3:
    print('USAGE:  python sphero.py ADDR PORT')
    exit()
addr = sys.argv[1]
port = sys.argv[2]

# connect to Sphero
r2d2 = r2d2_client.SpheroClient(addr, port)

# pause for 1s
time.sleep(1)

# follow path (☑ =start node, ☒ =end node)
#         ☐ ⇒ ☒
#         ⇑   ⇓
#     ☐ ⇒ ☐   ⇓
#     ⇑       ⇓
# ☐ ⇒ ☐       ⇓
# ⇑           ⇓
# ☑ ⇐ ⇐ ⇐ ⇐ ⇐ ☐
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
speed = 0x44  # quarter speed

complete = maneuver.follow_path(r2d2, path, speed)
turned = r2d2.turn(180)
animated = r2d2.animate(10)
asleep = r2d2.sleep()
quit = r2d2.quit()
