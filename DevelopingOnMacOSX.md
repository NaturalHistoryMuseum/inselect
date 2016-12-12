# Mac OS X development environment

# Compilers and homebrew

* Install the XCode command line tools from the app store.
* Install [homebrew](http://brew.sh/).
* Install dependencies `UPX` and `zbar`:

```
brew install upx zbar libdmtx
```

# Install Miniconda

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O /tmp/Miniconda3-latest-MacOSX-x86_64.sh
bash /tmp/Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda3
rm /tmp/Miniconda3-latest-MacOSX-x86_64.sh

export PATH=~/miniconda3/bin:$PATH
conda update --yes conda
```

# Inselect env

```
conda env create -f inselect.yml
source activate inselect
pip install -r requirements.pip
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
pyrcc5 icons.qrc > inselect/gui/icons.py
```

# Test and run

```
nosetests --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
```

Run inselect

```
python -m inselect.scripts.inselect
```

# Build

The build script freezes icons, runs tests, freezes python and assembles files
into a `.dmg` file.

```
./build.sh
```

The `.dmg` file will be in `dist`.
