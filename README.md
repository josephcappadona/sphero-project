# sphero-project

## Video Example
[https://www.youtube.com/watch?v=qjIhtkhbPT8](R2D2 + A*)

## Setup
```
git clone https://github.com/josephcappadona/sphero-project.git
cd sphero-project/spherov2.js
yarn install
```

## Usage

### Start Server
```
cd sphero-project/spherov2.js/examples
sudo yarn r2d2-server  # must use sudo to access bluetooth adapter
```

### Start Client
Navigate to `sphero-project/src`, and in `python` REPL:
```
from r2d2_client import R2D2Client
r2d2 = R2D2Client('127.0.0.1', 1337)

r2d2.animate(10)
r2d2.roll(0x88, 180, 2)  # drive at half speed, at a 180deg heading, for 2 seconds
r2d2.set_stance(2)  # transition to bipod

from maneuver import follow_path
path = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3), (3,0), (0,0)]
follow_path(r2d2, path, 0x88, scale_dist=0.5)

r2d2.turn(0)
r2d2.sleep()
r2d2.quit()
```

or, from the command line:
```
python simple_routine.py
```

## Tests
```
python -m pytest tests/test_*.py
```
