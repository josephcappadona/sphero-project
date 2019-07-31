# arturo-ai
The galactic headquarter for Arturo, the best AI bot for R2D2s.

# Instructions

Download the current version of Python from https://www.python.org/downloads/
Double click on the "Install Certificates.command" file in the /Applications/Python\ 3.7 folder
The Mac installer will put it at /usr/local/bin/python3 which you can verify by checking the date after typing

```
ls -la /usr/local/bin/py*
```

You should see today’s date.
Make sure you have brew installed.  
```
which brew
```

if you don’t have it, then install it from here: https://brew.sh
Download the repo
```
git clone https://github.com/BetweenTwoTests/arturo-ai.git
cd arturo-ai
```

Set your Path
```
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin 
```

Create a virtual environment
```
/usr/local/bin/python3 -m venv r2d2
source r2d2/bin/activate
python -m pip install --upgrade pip
```

Set up Node in your virtual environment
```
python -m pip install nodeenv
nodeenv -p --node=10.15.3
brew install yarn
```

install python dependencies
```
python -m pip install numpy pygame pynput
```

compile the server library and dependencies
```
cd spherov2.js
sudo yarn install

cd lib/
yarn rebuild
```

start the server
```
cd ../examples/
sudo yarn server
```

Leave the server running in its own Terminal window.
Open a new Terminal window
change into your sphero-project director
```
cd arturo-ai
source r2d2/bin/activate 
```
