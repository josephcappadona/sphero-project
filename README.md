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

# install JS packages
cd spherov2.js
yarn install
```

### Drive Mode

Drive mode allows you to control a droid in real time using your keyboard. Due to security reasons, on Mac OS, a few steps are needed to set this up to allow Python to interpret keystrokes.

1. Go to `System Preferences` -> `Security & Privacy` -> `Privacy tab` -> `Accessibility`.

2. Click the lock in the bottom left and enter your password to make changes.

3. Click the plus icon. Navigate to your Python 3.7 installation. This will likely be at `/Library/Frameworks/Python.framework/Versions/3.7/Python/`. If not, type `which python3.7` in Terminal to find the location (you will want the `Python` file at the same level as the `bin` folder you find). Click the `Python` file, then click `Open` in the bottom right.

4. Click the plus icon again. Navigate to the same location as in Step 3, except this time, go into the `Resources` folder, select the `Python` application there, and click `Open` in the bottom right.

5. Click the plus icon again. Navigate to your terminal program. If you're using the default system terminal, this will be located at `/Applications/Utilities/Terminal`. Select the program, then click `Open` in the bottom right.

6. Make sure both programs you added are checked, and click the lock in the bottom left to save changes.

For usage, see the [Usage - Drive Mode](#usage-drive-mode) below.

**Note**: If you use a terminal session manager such as `tmux`, you will also need to add that to `Accessibility` controls.

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
follow_path(droid, path, 0x88, scale_dist=0.5)

droid.turn(0)
droid.sleep()
droid.quit()
```

<h4 id="usage-drive-mode">
### Drive Mode
</h4>

Navigate to the project `src` folder and start up Python with **sudo**: `sudo python3.7`. You can then enter drive mode like this:
```
from client import DroidClient
r2 = DroidClient()
r2 = r2.connect_to_R2D2()
r2.enter_drive_mode()
```

The controls are:
```
UP = increase speed 0.1
DOWN = decrease speed 0.1
LEFT = adjust heading left 15°
RIGHT = adjust heading right 15°
SHIFT = speed/heading adjustment modifier, changes speed adjustment to 0.25, changes heading adjustment to 45°
S = stop droid (brings speed to 0)
ESC = exit drive mode
```

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
