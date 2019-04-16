## Details

`graph.py` implements the `Graph` data structure, which implements the `neighbors` and `dist_between` methods.

`a_star.py` implements the [A\* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) in the method `A_star` which uses helper functions `reconstruct_path` and `heuristic_cost_estimate`.

`maneuver.py` implements the `follow_path` method using the helper functions `roll`, which extends the `sphero_driver` roll method, and `compute_roll_parameters`, which computes the distance and angle between the Sphero's current position and its next position on the path.

`sphero.py` attempts to connect to a Sphero using the `sphero_driver` library and command it to follow a simple zig-zag path using `maneuver.py`'s `follow_path` method.
