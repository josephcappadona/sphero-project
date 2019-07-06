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
follow_path(droid, path, 0x88, scale_dist=0.5)

droid.turn(0)
droid.sleep()
droid.quit()
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
