# R2D2 GUI

## Setup

If you have not already, you will need to install PyGame to run this GUI:

```bash
cd sphero-project
source virtualenv/bin/activate  # if necessary
python -m pip install pygame
```

## Usage

### Activate Virtual Environment (if necessary)

```bash
cd sphero-project
source virtualenv/bin/activate
```

### Launching the GUI
Navigate to this directory (`sphero-project/src/GUI`), and start up the GUI by running:

```bash
python main.py
```

In a new terminal, start up a Python REPL in the parent directory (`sphero-project/src`) (after activating your virtual environment), instantiate a `DroidClient` object and call `connect_to_R2D2`:

```python
from client import DroidClient
r2 = DroidClient()
r2.connect_to_R2D2()
```

You should then see a GUI pop up. You can now control R2D2 using the same commands that you use to control the real droid (minus some of the purely aesthetic commands); see [here](https://github.com/josephcappadona/sphero-project#start-client) or type `help(r2)` within the REPL to see the full list of commands.

### Drive Mode

You can also control R2D2 with your keyboard:

```python
r2.enter_drive_mode()
```

There will be a few automatic preparation steps (e.g., switching R2D2's stance to tripod), and you should then see this prompt

```
Controls:
UP = increase speed 0.1
DOWN = decrease speed 0.1
LEFT = adjust heading left 15°
RIGHT = adjust heading right 15°
S = stop droid (brings speed to 0)
ESC = quit drive mode


Ready for keyboard input...
```

and you're ready to go. Remember to keep the Python REPL window in focus, since it is the Python program that is interpreting your keystrokes.

### Loading a Maze into the GUI

#### Generating a Maze
Within the parent folder (`sphero-project/src`), there is a script called `generate_random_maze.py`. It takes as arguments two inputs, the width and the height of the maze you'd like to generate. It will print the generated maze to stdout, so, in order to use it in the GUI, you should pipe the results to a text file within the GUI directory. So,

```bash
cd sphero-project/src
python generate_random_maze.py 30 30 > GUI/my_maze.txt
```

It is probably best to keep the maze size between 30 and 50 to avoid overflowing the edges of your screen.

You can then load the maze into the GUI by running `main.py` with an additional argument of the path to the maze you saved:

```bash
cd GUI
python main.py my_maze.txt
```

Now you can connect to R2D2 the same way [detailed above](#usage) and control him using commands or drive mode.

#### Loading a Maze into a Graph Object

Within the file `sphero-project/src/maze.py`, there are two methods called `load_maze_arr_from_file` and `load_2d_maze_arr_into_graph` that can be used as follows (assume our maze was generated using the same commands from the [previous step](#generating-a-maze):

```bash
cd sphero-project/src
```

Then in a Python REPL:

```python
import maze
maze_arr = maze.load_maze_arr_from_file('GUI/my_maze.txt')
maze_graph = maze.load_2d_maze_arr_into_graph(maze_arr)
```

You can then use this `maze_graph` object perform algorithms on the maze graph! See `sphero-project/src/graph.py` for the precise implementation of this `Graph` object, or call `help(maze_graph)` to see a list of the available commands.

## Troubleshooting

There is a [bug in PyGame for Mac OS Mojave](https://github.com/pygame/pygame/issues/555) if you installed Python with HomeBrew. If you get nothing but a blank grey screen when starting up the GUI, you should explore the linked thread to find the solution that works best for you. We are trying to figure out the best way to circumvent this issue in the future (e.g., by using [virtual environments](https://www.geeksforgeeks.org/python-virtual-environment/)), but in the meantime, we appreciate your patience.

If you have any other questions or problems, feel free to email me or CCB.
