from src.graph import Graph
from src.a_star import A_star
from itertools import product


# create sample graph (☑ =start node, ☒ =goal nodes)
# ☒ ══☐   ☐ ══☒
# ║   ║   ║   ║
# ☐   ☐ ══☐   ☐
# ║   ║   ║   ║
# ☐ ══☐   ☐ ══☐
# ║       ║   ║
# ☑   ☐ ══☐   ☒
V = list(product(range(4), range(4)))
E = [((0,0), (0,1)), ((0,1), (0,2)),
     ((0,1), (1,1)), ((0,2), (0,3)),
     ((0,3), (1,3)), ((1,1), (1,2)),
     ((1,2), (1,3)), ((1,2), (2,2)),
     ((2,2), (2,1)), ((2,1), (2,0)),
     ((2,1), (3,1)), ((2,0), (1,0)),
     ((2,2), (2,3)), ((2,3), (3,3)),
     ((3,3), (3,2)), ((3,2), (3,1)),
     ((3,1), (3,0))]
G = Graph(V, E)


def test_a_star_1():
    # bottom left -> top left
    computed_path = A_star(G, (0,0), (0,3))
    correct_path = [(0,0), (0,1), (0,2), (0,3)]
    assert computed_path == correct_path

def test_a_star_2():
    # bottom left -> top right
    computed_path = A_star(G, (0,0), (3,3))
    correct_path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3)]
    assert computed_path == correct_path

def test_a_star_3():
    # bottom left -> bottom right
    computed_path = A_star(G, (0,0), (3,0))
    correct_path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,1), (3,1), (3,0)]
    assert computed_path == correct_path
