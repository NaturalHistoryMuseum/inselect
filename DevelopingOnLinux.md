# Inselect on Linux

These instructions use the system's Python and many system python packages.
Tested on Ubuntu 14.04 and 16.04, both with 2GB RAM.
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
python2 -m bin.freeze_icons
```

# Test and run

```
nosetests --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
```

Ubuntu 16.04 appears to come with `nose` already installed so the
`pip2 install -r requirements.pip` step above will not install `nose` within
the virtual env so `nosetests` will not find the packages within the
virtualenv and you will see lots of `ImportErrors`. If this is the case, run

```
python -m nose --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
```

Run `nosetests` as shown above.

Run inselect:

```
./inselect.py
```

