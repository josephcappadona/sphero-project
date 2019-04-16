#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from sphero_driver import sphero_driver
import time
import maneuver

# parse Sphero address
if len(sys.argv) != 2:
    print('USAGE:  python sphero.py SPHERO_ADDR')
    exit()
addr = sys.argv[1]

# connect to Sphero
sphero = sphero_driver.Sphero()
while True:
    try:
        sphero.connect()
        break
    except:
        print('Trying to connect again.')

# pause for 1s
sphero.roll(0, 0, None)
time.sleep(0.5)

# follow path (☑ =start node, ☒ =end node)
#         ☐ ══☒
#         ║
#     ☐ ══☐
#     ║
# ☐ ══☐
# ║
# ☑
path = [(0,0), (0,1), (1,1), (2,1), (2,2), (3,2), (3,3)]
api_response = maneuver.follow_path(sphero, path)
