# sphero-project

## Video Example
[R2D2 + A\*](https://www.youtube.com/watch?v=qjIhtkhbPT8)

## Setup

### Installation

#### Mac OS

0. If you have not already, install Xcode from the App Store: https://apps.apple.com/us/app/xcode/id497799835?mt=12

    Once it is installed, open Terminal, run `xcode-select --install`, and follow the prompts to install Xcode Command Line Tools. (If you already have the Command Line Tools installed, you will receive an error message saying so.)

1. Download and install the most current version of Python from https://www.python.org/downloads/

2. Using Finder, navigate to `/Applications/Python 3.7` and double click the file `Install Certificates.command`.

3. Verify that Python was installed to the correct location by typing the following command into Terminal: `ls /usr/local/bin/python3.7`. If it prints out `/usr/local/bin/python3.7`, you are good.

4. Clone this repo in whatever directory you would like:

    ```bash
    cd ~/Documents  # replace "Documents" with your desired directory
    git clone https://github.com/josephcappadona/sphero-project.git
    ```

5. Navigate into the repository and create a Python virtual environment:

    ```bash
    cd sphero-project
    /usr/local/bin/python3.7 -m venv virtualenv
    source virtualenv/bin/activate
    python -m pip install --upgrade pip
    ```

    If you have never used virtual environments before, you can read about them here: https://docs.python.org/3/tutorial/venv.html. Essentially, a virtual environment creates a sandbox in which you can install and manage dependencies without affecting dependencies used in other projects.

    IMPORTANT: Every time you begin to do work in this library, you must run `source virtualenv/bin/activate` in Terminal to activate your virtual environment (you must do this for each Terminal instance you are running); if you do not, it is possible you will use a different version of Python or incorrect versions of important dependencies. When you are done working with this package, run `deactivate` in Terminal to deactivate the virtual environment so that you do not accidentally modify it when doing unrelated work.

6. Set your virtual environment's PATH variable:

    ```bash
    export PATH=`pwd`/virtualenv/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin
    ```

    Your shell's PATH variable "is basically a list of directories your computer looks through to find a requested executable" (you can read more about it here: https://medium.com/@jalendport/what-exactly-is-your-shell-path-2f076f02deb4).

7. Install yarn in your virtual environment:

    ```bash
    wget https://yarnpkg.com/latest.tar.gz
    tar xfz latest.tar.gz
    mv yarn-*/lib/* virtualenv/lib/
    mv yarn-*/bin/* virtualenv/bin/
    rm -r latest.tar.gz yarn-*
    ```

8. Set up Node.js within your virtual environment:

    ```bash
    python -m pip install nodeenv
    nodeenv -p --node=10.15.3
    brew install yarn
    ```

9. Install the required Python dependencies:

    ```bash
    python -m pip install numpy pygame
    ```

10. Install the required JavaScript dependencies and compile the Spherov2.js library:

    ```bash
    cd spherov2.js
    sudo yarn install
    cd lib
    yarn rebuild
    ```

#### Linux

These instructions will assume you are using a Debian-based Linux distro (Ubuntu, Arch, Fedora). If you are not, then the steps which use a package manager (0 and 4)to install dependencies will need to be translated for your ditro's package manager.

0. Install Python:
    ```bash
    sudo apt-get install python3.7 python3.7-venv
    ```

1. Clone this repository in whatever directory you would like and grant your user ownership:
    ```bash
    cd ~/Documents  # replace "Documents" with your desired directory
    git clone https://github.com/josephcappadona/sphero-project.git
    sudo chown -R `whoami` sphero-project
    ```

2. Navigate into the repository and create a Python virtual environment:
    ```bash
    cd sphero-project
    /usr/local/bin/python3.7 -m venv virtualenv
    source virtualenv/bin/activate
    python -m pip install --upgrade pip
    ```

    If you have never used virtual environments before, you can read about them here: https://docs.python.org/3/tutorial/venv.html. Essentially, a virtual environment creates a sandbox in which you can install and manage dependencies without affecting dependencies used in other projects.

    IMPORTANT: Every time you begin to do work in this library, you must run source virtualenv/bin/activate in Terminal to activate your virtual environment (you must do this for each Terminal instance you are running); if you do not, it is possible you will use a different version of Python or incorrect versions of important dependencies. When you are done working with this package, run deactivate in Terminal to deactivate the virtual environment so that you do not accidentally modify it when doing unrelated work.

3. Set your virtual environment's PATH variable:

    ```bash
        export PATH=`pwd`/virtualenv/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin
            ```

    Your shell's PATH variable "is basically a list of directories your computer looks through to find a requested executable" (you can read more about it here: https://medium.com/@jalendport/what-exactly-is-your-shell-path-2f076f02deb4).

4. Install yarn in your virtual environment:

    ```bash
    wget https://yarnpkg.com/latest.tar.gz
    tar xfz latest.tar.gz
    mv yarn-*/lib/* virtualenv/lib/
    mv yarn-*/bin/* virtualenv/bin/
    rm -r latest.tar.gz yarn-*
    ```


5. Set up Node.js within your virtual environment:

    ```bash
    python -m pip install nodeenv
    nodeenv -p --node=10.15.3
    ```

6. Install the required Python dependencies:

    ```bash
    python -m pip install numpy pygame
    ```

7. Install the required JavaScript dependencies and compile the Spherov2.js library:

    ```bash
    cd spherov2.js
    sudo yarn install
    cd lib
    yarn rebuild
    ```

#### Windows

A windows installation guide is almost complete, but still needs to be tested. If you'd like to help us test it, please reach out to me or CCB!


### Testing Your Installation

#### Server

To test the Sphero server, navigate to `sphero-project/spherov2.js/examples` and run the following command (remember to activate your virtual environment first if necessary):

```bash
sudo yarn server
```

If it works, you will see `Listening...`. For instructions on how to actually use this server, see [below](#usage).


#### Client

To test the Python client (the program you will use to send commands to the JavaScript server), leave the server running and open up a new Terminal, navigate to where you cloned this project, and activate your virtual environment:

```bash
cd ~/Documents/sphero-project  # Replace "Documents" with the location you cloned this repository
source virtualenv/bin/activate
```

Then, navigate into the `src` directory and launch a Python REPL:

```bash
cd src
python
```

Then, run these commands:

```python
from client import DroidClient
droid = DroidClient()
droid.scan()  # Scan the area for droids
droid.connect_to_droid('D2-55A2')  # Replace 'D2-55A2' with your droid's identifier
droid.disconnect()
droid.quit()
exit()
```

If it is working, you should receive no errors, and your droid should do a funny little animation once you connect to him. For more details on how to use this Python client, see [below](#start-client).


## Usage

### Activate Virtual Enviornment

```bash
cd sphero-project
source virtualenv/bin/activate
```

### Start Server
```bash
cd sphero-project/spherov2.js/examples
sudo yarn server  # must use sudo to access bluetooth adapter
```

### Start Client
Navigate to `sphero-project/src`, and in a Python REPL:
```python
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

droid.turn(180)
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

## Development

Should you change any of the `spherov2.js/lib` files, you must rebuild the library:

```bash
cd sphero-project/spherov2.js/lib
yarn rebuild
```

## TODO

* document interface properly
* create scripts to start the server for simplicity (?)
