# Inselect on Linux

These instructions use the system's Python and many system python packages.
For an approach using `miniconda` see `.travis.yml`.

1. Setup Python virtual environment

```
sudo apt-get install python-pip python-dev build-essential
sudo pip2 install --upgrade pip
sudo pip2 install virtualenv virtualenvwrapper
```

Append to ``~/.bash_profile`

```

# Setup virtualenvwrapper
export WORKON_HOME=~/Envs/
source /usr/local/bin/virtualenvwrapper.sh
```


2. Install system dependencies
```
sudo apt-get install python-pyside pyside-tools python-numpy python-scipy python-sklearn python-opencv libzbar-dev libdmtx-dev
```

3. Create virtual environment for Inselect and install dependencies from pip

```
mkvirtualenv --system-site-packages inselect
pip2 install -r requirements.pip
```

4. Test and run

```
python -m bin.freeze_icons
nosetests --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
./inselect.py
```
