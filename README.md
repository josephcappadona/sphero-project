# sphero-project

## Video Example
[R2D2 + A*](https://www.youtube.com/watch?v=qjIhtkhbPT8)

## Setup
```
# clone this repo
git clone https://github.com/josephcappadona/sphero-project.git
cd sphero-project

# install python dependencies
python3.7 -m pip install numpy pygame pynput

# setup node.js
cd src
bash setup_node_mac.sh
cd ..

# compile the server library and dependencies
cd spherov2.js/lib
yarn rebuild
cd ..
yarn install
```

## Usage

### Start Server
```
cd sphero-project/spherov2.js/examples
sudo yarn server  # must use sudo to access bluetooth adapter
```

### Start Client
Navigate to `sphero-project/src`, and in `python3.7` REPL:
```
from client import DroidClient
droid = DroidClient()
droid.scan()

droid.connect_to_droid('D2-2A86')
# or droid.connect_to_R2D2()
# or droid.connect_to_R2Q5()
# or droid.connect_to_any()

droid.animate(10)
droid.set_logic_display_intensity(1)
droid.set_holo_projector_intensity(1)
droid.set_front_LED_color(255, 255, 0)
droid.set_back_LED_color(0, 255, 255)
droid.play_sound(10)

droid.roll(0.5, 180, 2)  # drive at half speed, at a 180deg heading, for 2 seconds
droid.set_stance(2)  # transition back to bipod

from maneuver import follow_path
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
follow_path(droid, path, 1.0, scale_dist=0.5)

droid.turn(0)
droid.sleep()
droid.quit()
```

### Drive Mode

Drive mode allows you to drive your droid using your keyboard. Once you have the server running, you can start drive mode like this:

```python
from client import DroidClient
droid = DroidClient()
droid.connect_to_droid('D2-2A86')  # or other connect command
droid.enter_drive_mode()  # droid will change stance to tripod and python will start accepting keystrokes
droid.exit()
```

You can also run `python drive_mode.py` from the `src` directory, but be sure to change the connect command with the name of your droid.

The controls for drive mode are:

```
UP = increase speed 0.1
DOWN = decrease speed 0.1
LEFT = adjust heading left 15°
RIGHT = adjust heading right 15°
S = stop droid (brings speed to 0)
ESC = quit drive mode
```

### GUI

There is a PyGame GUI that will allow you to control R2D2 in a virtual sandbox using the same DroidClient interface that is used to control the actual droids.

In one terminal:

```
cd sphero-project/src/GUI
python main.py
```

In another terminal:
```
cd sphero-project/src
python -i connect_to_r2d2.py
```

A PyGame window will pop up that should show R2D2 on a white background. `python -i connect_to_r2d2.py` will run the script `connect_to_r2d2.py` and then drop you into a Python REPL with access to a DroidClient variable called `r2`. In the REPL, you can control R2D2 using any of the methods implemented by DroidClient (a few of the cosmetic commands such as LED colors and sounds are not implemented):

```python
r2.set_stance(1)
r2.turn(90)
r2.roll(0.5, 90, 2)
r2.roll(0.5, 0, 2)
```

You can even use [Drive Mode](#drive-mode):

```python
r2.enter_drive_mode()
```

#### Loading a Map into the GUI

You can load a map into the GUI by running `main.py` with an additional argument. We will use the `generate_random_maze.py` script in `sphero-project/src` to generate a random 25x30 maze and load it into the GUI:

```
cd sphero-project/src
python generate_random_maze.py 25 30 > GUI/test_maze.txt

cd GUI
python main.py test_maze.txt
```

Then, in another terminal, connect to the GUI the same way you did above: `python -i connect_to_r2d2.py`.

## Development

Should you change any of the `spherov2.js/lib` files, you must rebuild the library:

```
cd sphero-project/spherov2.js/lib
yarn rebuild
```

## TODO

* implement GUI
* document interface properly
* move `spherov2.js` into a `lib` folder
* create scripts to start the server for simplicity (?)
