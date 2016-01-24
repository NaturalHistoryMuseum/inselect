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

export PATH=$PATH:~/miniconda/bin
conda update --yes conda
```

# Inselect env
```
conda create --yes --name inselect pillow pyside
```

# OpenCV
`numpy` is pinned by opencv installation

```
conda install --yes -c https://conda.binstar.org/jjhelmus opencv
```

# Dependencies

```
cd ~/projects/inselect
pip install -r requirements.txt
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

# Unit tests

```
cd ~/projects/inselect/
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect
```
