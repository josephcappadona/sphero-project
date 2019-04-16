#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from Queue import PriorityQueue
from collections import defaultdict
inf = float('inf')

# adapted from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def A_star(G, start, goal):

    closedSet = set()
    openSet = set([start])
    frontier = PriorityQueue()
    cameFrom = dict()

    gScore = defaultdict(lambda:inf)  # gScore[v] = cost(start, v)
    gScore[start] = 0

    fScore = defaultdict(lambda:inf)  # fScore[v] = cost(start, v) + cost(v, goal)
    fScore[start] = heuristic_cost_estimate(G, start, goal)
    frontier.put((fScore[start], start))

    while openSet:
        _, current = frontier.get()
        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)
        closedSet.add(current)

        for neighbor in G.neighbors(current):
            if neighbor in closedSet:
                continue

            tentative_gScore = gScore[current] + G.dist_between(current, neighbor)

            if neighbor not in openSet:
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue

            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + heuristic_cost_estimate(G, neighbor, goal)
            frontier.put((fScore[neighbor], neighbor))

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path[::-1]

def heuristic_cost_estimate(G, u, v):
    return 0  # simple, admissable heuristic
