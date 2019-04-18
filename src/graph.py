from collections import defaultdict

class Graph:

    V = None
    E = None

    def __init__(self, V, E):
        
        self.V = V
        self.E = E

        neighborhood = defaultdict(set)
        for (u,v) in E:
            neighborhood[u].add(v)
            neighborhood[v].add(u) # assumes undirected graph
        self.neighborhood = neighborhood

    def neighbors(self, u):
        return self.neighborhood[u]

    def dist_between(self, u, v):
        if v not in self.neighbors(u):
            return None
        return 1 # assumes unweighted graph
