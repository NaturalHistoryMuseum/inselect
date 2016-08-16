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
```

## LibDMTX barcode reading library

* Get source for the library and the wrappers

    ```
    cd ~/projects
    git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx
    git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-wrappers
    ```

* Build library

    ```
    cd libdmtx
    git checkout v0.7.4
    ./autogen.sh
    ./configure
    make
    ```

* Build Python library

    ```
    cd ../dmtx-wrappers/
    ./autogen.sh
    ./configure
    make
    ```

* Install Python library

    ```
    cd python
    python setup.py install
    ```

* Test

    ```
    python -c "import pydmtx; print(pydmtx)"
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
