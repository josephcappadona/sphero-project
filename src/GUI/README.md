# R2D2 GUI

## Setup

You will need to install PyGame to run this GUI:

```
python -m pip install pygame
```

## Usage

From this directory, start up the GUI and server:

```
python main.py
```

In a new terminal, start up a Python REPL in the parent directory (`src`), initiate a `DroidClient` object and call `connect_to_R2D2`:

```python
from client import DroidClient
r2 = DroidClient()
r2.connect_to_R2D2()
```

You should then see a GUI pop up. To control R2D2, call `enter_drive_mode` from the Python REPL:

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



### Troubleshooting

There is a [bug in PyGame for Mac OS Mojave](https://github.com/pygame/pygame/issues/555) if you installed Python with HomeBrew. If you get nothing but a blank grey screen when starting up the GUI, you should explore the linked thread to find the solution that works best for you. We are trying to figure out the best way to circumvent this issue in the future (e.g., by using [virtual environments](https://www.geeksforgeeks.org/python-virtual-environment/)), but in the meantime, we appreciate your patience.
