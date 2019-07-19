import maze
import bfs_dfs
import a_star
from sys import argv

if len(argv) < 3:
    print('USAGE:  python generate_random_maze.py LENGTH HEIGHT')
    exit()
l, h = int(argv[1]), int(argv[2])

rand_maze_arr = maze.generate_random_2d_maze((l,h))
print('\n'.join(rand_maze_arr))
