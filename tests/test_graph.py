from src.graph import Graph
from itertools import product


# create sample graph
# ☐   ☐
# ║
# ☐ ══☐
V = list(product(range(2), range(2)))
E = [((0,0), (0,1)),
     ((0,0), (1,0))]
G = Graph(V, E)


def test_neighbors():
    assert (0,1) in G.neighbors((0,0))
    assert (1,0) in G.neighbors((0,0))
    assert (1,1) not in G.neighbors((0,0))

    assert (0,0) in G.neighbors((0,1))
    assert (1,0) not in G.neighbors((0,1))
    assert (1,1) not in G.neighbors((0,1))

    assert (0,0) in G.neighbors((1,0))
    assert (0,1) not in G.neighbors((1,0))
    assert (1,1) not in G.neighbors((1,0))

    assert len(G.neighbors((1,1))) == 0


def test_dist_between():
    assert G.dist_between((0,0), (0,1)) == 1
    assert G.dist_between((0,1), (0,0)) == 1
    assert G.dist_between((0,1), (1,1)) == None
    assert G.dist_between((1,0), (1,1)) == None
    assert G.dist_between((0,0), (1,1)) == None
    assert G.dist_between((0,1), (1,0)) == None
