## Details

### Graph & A* Search
* `graph.py` implements a `Graph` data structure, which implements the `neighbors` and `dist_between` methods.

* `courses.py` impelements pre-made graphs for quick testing.

* `a_star.py` implements the [A\* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) in the method `A_star` which uses helper functions `reconstruct_path` and `heuristic_cost_estimate`.

### Sphero & Path Traversal
* `r2d2_client.py` implements the client side of a Telnet connection via the `R2D2Client` class, which implements all of the commands that the `spherov2.js` library implements for R2D2.

* `maneuver.py` implements the `follow_path` method using the helper function `compute_roll_parameters`, which computes the distance and angle between the Sphero's current position and the next position on the path.

* `sphero.py` attempts to connect to a Sphero using the `R2D2Client` object and command it to follow a simple zig-zag path using `maneuver.py`'s `follow_path` method.
