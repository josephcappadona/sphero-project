from collections import defaultdict
from itertools import product
from collections import defaultdict

obstacles = [
    ((0,0), (1,0)),
    ((1,0), (1,1))
]

g = Graph(obstacles)

class Graph:
    # obstacle = { (row, col): True }
    def __init__(self, obstacles):
        self.row = 8
        self.col = 5

        self.V = list(product(range(self.row), range(self.col)))

        offsets = ((1, 0), (0, 1), (0, -1), (-1, 0),
                   (-1, 1), (1, 1), (-1, -1), (1, -1))
        E = []
        for u_x in range(self.col):
            for u_y in range(self.row):
                for offset_row, offset_col in offsets:
                    v_x, v_y = (r + offset_row, c + offset_col)
                    if (0 <= u_x < self.row and 0 <= u_y < self.col and
                        0 <= v_x < self.row and 0 <= v_y < self.col and
                        not obstacles[(v_x, v_y)]:
                        edges.append(
                            ((u_x, u_y), (v_x, v_y))
                        )

        neighborhood = defaultdict(set)
        for (u,v) in E:
            neighborhood[u].add(v)
            neighborhood[v].add(u) # assumes undirected graph
        self.neighborhood = neighborhood

    def neighbors(self, u):
        return self.neighborhood[u]

    def update(self, new_obstacles, free_edges):
        # add new obstacles
        for (u, v) in new_obstacles.keys():
            self.neighborhood[u].remove(v)
            self.neighborhood[v].remove(u)

        # delete old obstacles and recover as new_edge
        for (u, v) in free_edges.keys():
            self.neighborhood[u].add(v)
            self.neighborhood[v].add(u)


    def dist_between(self, u, v):
        if v not in self.neighbors(u):
            return None
        return 1 # assumes unweighted graph

    def move_enemy(self, pos, bound):
        n = self.neighborhood[pos]

        for new_pos in n:
            if new_pos[1] <= bound[1] and new_pos[1] >= bound[0]:
                return new_pos
