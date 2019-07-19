from itertools import product
from graph import Graph
from collections import defaultdict
import random
from bfs_dfs import reconstruct_path
import sys; sys.setrecursionlimit(1000000)

def invert_tuple_y(tup, l, h):
    x, y = tup
    return (x, h-1-y)

def insert_maze_piece(maze, maze_piece, x, y):
    for dx in range(3):
        for dy in range(3):
            maze[y-dy][x+dx] = maze_piece[-1-dy][dx]

def construct_maze(dimensions, parents, children, start, goal):
    l, h = dimensions
    x_s, y_x = start
    x_g, y_g = goal
    maze = [['┼' for _ in range(l)] for _ in range(h)]
    l, h = dimensions
    l, h = int(l/3), int(h/3)

    for u in product(range(l), range(h)):
        if u not in children:
            continue

        x, y = u
        x_, y_ = 3*x, -1-3*y

        neighbors = children[u]
        dirs = set(tuple_sub(v,u) for v in neighbors)
        dirs_inverted_ys = set((a,-b) for a,b in dirs)
        maze_piece = MazePiece.dirs_to_piece(dirs_inverted_ys)
        insert_maze_piece(maze, maze_piece, x_, y_)
        if u == start:
            maze[y_-1][x_+1] = '*'
        elif u == goal:
            maze[y_-1][x_+1] = '$'
    return '\n'.join([''.join(row) for row in maze])


def tuple_add(u, v):
    return tuple([a+b for a,b in zip(u, v)])
def tuple_sub(u, v):
    return tuple([a-b for a,b in zip(u, v)])

def shuffle(l):
    return random.sample(l, len(l))

def parents_to_children(parents):
    children = defaultdict(set)
    for child, pars in parents.items():
        for par in pars:
            children[par].add(child)
            children[child].add(par)
    return children

cardinal_direction_tuples = u_r, u_u, u_l, u_d = [(1,0), (0,1), (-1,0), (0,-1)]

class MazePiece:
    _1000 = "┨ ┠\n┨ ┠\n╄┯╃".split('\n')
    _0100 = "╆┷┷\n┨  \n╄┯┯".split('\n')
    _0010 = "╆┷╅\n┨ ┠\n┨ ┠".split('\n')
    _0001 = "┷┷╅\n  ┠\n┯┯╃".split('\n')

    _1100 = "┨ ┗\n┨  \n╄┯┯".split('\n')
    _1010 = "┨ ┠\n┨ ┠\n┨ ┠".split('\n')
    _1001 = "┛ ┠\n  ┠\n┯┯╃".split('\n')
    _0110 = "╆┷┷\n┨  \n┨ ┏".split('\n')
    _0101 = "┷┷┷\n   \n┯┯┯".split('\n')
    _0011 = "┷┷╅\n  ┠\n┓ ┠".split('\n')

    _1110 = "┨ ┗\n┨  \n┨ ┏".split('\n')
    _1101 = "┛ ┗\n   \n┯┯┯".split('\n')
    _1011 = "┛ ┠\n  ┠\n┓ ┠".split('\n')
    _0111 = "┷┷┷\n   \n┓ ┏".split('\n')

    _1111 = "┛ ┗\n   \n┓ ┏".split('\n')

    @staticmethod
    def dirs_to_piece(dirs):
        if len(dirs) == 1:
            if u_d in dirs:
                return MazePiece._1000
            elif u_r in dirs:
                return MazePiece._0100
            elif u_u in dirs:
                return MazePiece._0010
            elif u_l in dirs:
                return MazePiece._0001
        elif len(dirs) == 2:
            if u_d in dirs:
                if u_r in dirs:
                    return MazePiece._1100
                else:
                    if u_u in dirs:
                        return MazePiece._1010
                    else:
                        return MazePiece._1001
            else:
                if u_r in dirs:
                    if u_u in dirs:
                        return MazePiece._0110
                    else:
                        return MazePiece._0101
                else:
                    return MazePiece._0011
        elif len(dirs) == 3:
            if u_d in dirs:
                if u_r in dirs:
                    if u_u in dirs:
                        return MazePiece._1110
                    else:
                        return MazePiece._1101
                else:
                    return MazePiece._1011
            else:
                return MazePiece._0111
        elif len(dirs) == 4:
            return MazePiece._1111

    @staticmethod
    def piece_to_string(piece):
        return '\n'.join(piece)

