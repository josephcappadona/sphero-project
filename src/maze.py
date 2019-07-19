from itertools import product
from graph import Graph
from collections import defaultdict
from math import ceil
import random
from bfs_dfs import reconstruct_path
from maze_helpers import *


def load_maze_arr_from_file(filename):
    with open(filename, 'rt') as maze_file:
        maze_text = maze_file.read()
        return maze_text_to_maze_arr(maze_text)

def maze_text_to_maze_arr(maze_text):
    return maze_text.strip('\n').split('\n')

def write_maze_arr_to_file(maze_arr, filename):
    with open(filename, 'wt+') as maze_file:
        maze_file.write('\n'.join(maze_arr))

def load_2d_maze_arr_into_graph(maze_arr):
    h = num_rows = len(maze_arr)
    l = num_cols = len(maze_arr[0])

    def is_open(c):
        return c in [' ', '*', '$']

    V = set()
    E = set()
    start = None
    goal = None

    # add coords of open spaces to V
    for x, y in product(range(num_cols), range(num_rows)):
        c = maze_arr[y][x]
        if is_open(c):
            V.add((x, y))
            if c == '*':
                start = (x, y)
            elif c == '$':
                goal = (x, y)

    # for each space, add an edge to each adjacent open space
    for x, y in V:
        u = (x,y)
        for dx, dy in cardinal_direction_tuples:
            v = (x+dx, y+dy)
            if (x != 0 or y != 0) and v in V:
                if (u, v) not in E and (v, u) not in E:
                    E.add((u,v))
    # invert y values
    E_prime = set()
    for u,v in E:
        u_prime = invert_tuple_y(u, l, h)
        v_prime = invert_tuple_y(v, l, h)
        E_prime.add((u_prime, v_prime))
    start_prime = invert_tuple_y(start, l, h)
    goal_prime = invert_tuple_y(goal, l, h)

    return Graph(V, E_prime), start_prime, goal_prime

def generate_random_2d_maze(dimensions, start=None, goal=None):
    l, h = dimensions
    if l < 6 or h < 6:
        print("ERROR:  Minimum dimensions are 6x6")
        exit()

    l, h = int(l/3), int(h/3)
    if not start:
        start = (0,0)
    if not goal:
        goal = (l-1, h-1)

    parents = defaultdict(list)
    discovered = defaultdict(lambda:False)
    delayed_exploration = set()
    delay_pctg = 0.35
    cycle_pctg = 0.01
    def DFS(u, delay_pctg):

        discovered[u] = True

        if random.random() < delay_pctg:
            delayed_exploration.add(u)
            return

        for direction in shuffle(cardinal_direction_tuples):
            v = a, b = tuple_add(u, direction)
            if 0 <= a < l and 0 <= b < h:
                if not discovered[v]:
                    parents[v].append(u)
                    DFS(v, delay_pctg)
                elif random.random() < cycle_pctg:
                    parents[v].append(u)
    DFS(start, delay_pctg)
    while delayed_exploration:
        u = random.sample(delayed_exploration, 1)[0]
        delayed_exploration.remove(u)
        DFS(u, delay_pctg)
    children = parents_to_children(parents)

    maze_text = construct_maze(dimensions, parents, children, start, goal)
    return maze_text_to_maze_arr(maze_text)

def display_solution(maze_arr, solution_path):
    l, h = len(maze_arr[0]), len(maze_arr)
    solved_maze_arr = [[' ' for _ in range(l)] for _ in range(h)]
    solution_path_set = set(solution_path)
    for x, y in product(range(l), range(h)):
        if (x, y) in solution_path_set:
            c = '#'
            if (x, y) == solution_path[0]:
                c = '*'
            elif (x, y) == solution_path[-1]:
                c = '$'
            x, y = invert_tuple_y((x,y), l, h)
            solved_maze_arr[y][x] = c
        else:
            x, y = invert_tuple_y((x,y), l, h)
            solved_maze_arr[y][x] = maze_arr[y][x]
        
    solved_maze_arr = [''.join(row) for row in solved_maze_arr]
    print_maze_arr(solved_maze_arr)

def print_maze_arr(maze_arr):
    print('\n'.join(maze_arr))

#DS_maze_arr = load_maze_arr_from_file('death_star_maze.txt')
#DS_maze_graph, DS_maze_start, DS_maze_goal = load_2d_maze_arr_into_graph(DS_maze_arr)
