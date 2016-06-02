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
conda create --yes --name inselect pillow=3.2.0 qt=4.8.7 pyside=1.1.2 numpy=1.10.1 scipy==0.17.0 scikit-learn=0.17.1
source activate inselect
```

# Dependencies

```
cd ~/projects/inselect
pip install -r requirements.txt
```

## OpenCV
Version of `numpy` is pinned by opencv installation but we want a later
version.

`jjhelmus` provides versions after `2.4.10` but these make the Mac build
extremely problematic by introducing many `dylib` dependencies that are
troublesome to freeze.
```
conda install --yes -c https://conda.binstar.org/jjhelmus opencv=2.4.10
conda install --yes numpy=1.10.1
```

## setuptools
A [bug in PyInstaller 3.1.1](https://github.com/pyinstaller/pyinstaller/issues/1773)
means that we need to use setupools 19.2:

```
conda install --yes setuptools=19.2
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

The build script freezes icons.

```
./build.sh
```

Installer will be in `dist`.
