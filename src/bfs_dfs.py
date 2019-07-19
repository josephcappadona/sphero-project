from queue import Queue
from collections import defaultdict

# https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
def BFS(G, start, goal):
    frontier = Queue()
    discovered = defaultdict(lambda:False)
    parent = {}
    discovered[start] = True
    frontier.put(start)
    while not frontier.empty():
        u = frontier.get()
        if u == goal:
            break
        for v in G.neighbors(u):
            if not discovered[v]:
                discovered[v] = True
                parent[v] = u
                frontier.put(v)
    return reconstruct_path(start, goal, parent)

# https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode
def DFS_recursive(G, start, goal):
    discovered = defaultdict(lambda:False)
    parent = {}
    def DFS(G, u):
        discovered[u] = True
        if u == goal:
            return
        for v in G.neighbors(u):
            if not discovered[v]:
                parent[v] = u
                DFS(G, v)
    DFS(G, start)
    return reconstruct_path(start, goal, parent)

# https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode
def DFS_iterative(G, start, goal):
    discovered = defaultdict(lambda:False)
    parent = {}
    stack = []
    stack.append(start)
    while stack:
        u = stack.pop()
        if u == goal:
            break
        if not discovered[u]:
            discovered[u] = True
            for v in G.neighbors(u):
                stack.append(v)
                if v not in parent:
                    parent[v] = u
    return reconstruct_path(start, goal, parent)
    

def reconstruct_path(start, goal, parent):
    path = [goal]
    current = goal
    while current != start:
        current = parent[current]
        path.append(current)
    return path[::-1]
