# Inselect on Linux

These instructions use the system's Python and many system python packages.
For an approach using `miniconda` see `.travis.yml`.

# Setup Python virtual environment

```
sudo apt-get install python-pip python-dev build-essential
sudo pip2 install --upgrade pip
sudo pip2 install virtualenv virtualenvwrapper
```

Append to ``~/.bash_profile`


```

## Setup virtualenvwrapper
export WORKON_HOME=~/Envs/
source /usr/local/bin/virtualenvwrapper.sh
```


# Install system dependencies
```
sudo apt-get install python-pyside pyside-tools python-numpy python-scipy python-sklearn python-opencv libdmtx-dev libzbar-dev
```

# Create virtual environment for Inselect and install dependencies from pip

```
mkvirtualenv --system-site-packages inselect
pip2 install -r requirements.pip
```

## LibDMTX barcode reading library

* Get source for the wrappers

    ```
    cd ~/projects
    git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-wrappers
    ```

* Install Python library

    ```
    cd python
    python2 setup.py install
    ```

## Test barcode reading libraries

Inselect has optional barcode reading capabilities. The dependent libraries
should have been installed.

```
python -c "from gouda.engines import ZbarEngine; print(ZbarEngine.available())"
python -c "from gouda.engines import LibDMTXEngine; print(LibDMTXEngine.available())"
```

# Developing

Icons are stored as individual files in `icons`. They are frozen into
a python file `inselect/gui/icons.py` by running

```
python -m bin.freeze_icons
```

Test and run

```
nosetests --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
./inselect.py
```

