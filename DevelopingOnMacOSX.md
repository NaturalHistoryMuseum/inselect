# Mac OS X development environment

# Compilers and homebrew

* Install the XCode command line tools from the app store.
* Install [homebrew](http://brew.sh/).
* Install dependencies `UPX` and `zbar`:

```
brew install upx zbar
```

# Install Miniconda

```
wget https://repo.continuum.io/miniconda/Miniconda-latest-MacOSX-x86_64.sh -O /tmp/Miniconda-latest-MacOSX-x86_64.sh
bash /tmp/Miniconda-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda
rm /tmp/Miniconda-latest-MacOSX-x86_64.sh

export PATH=~/miniconda/bin:$PATH
conda update --yes conda
```

# Inselect env

```
conda env create -f inselect-osx.yml
source activate inselect
conda install --channel https://conda.anaconda.org/jjhelmus --yes opencv=2.4.12=np110py27_0
pip install -r requirements.pip
```

## LibDMTX barcode reading library

* Install the `libdmtx` shared lib

    ```
    brew install libdmtx
    ```

* Test

    ```
    python -c "import libdmtx; print(libdmtx)"
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

# Build

The build script freezes icons, runs tests, freezes python and assembles files
into a `.dmg` file.

```
./build.sh
```

The `.dmg` file will be in `dist`.
