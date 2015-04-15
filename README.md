# Inselect

[ ![Travis status](https://travis-ci.org/NaturalHistoryMuseum/inselect.svg?branch=master) ](https://travis-ci.org/NaturalHistoryMuseum/inselect)

A tool for the semi-automated segmentation and annotation of scanned images of museum objects.

You can download the latest release of Inselect for Windows, for Mac and the Python source from our [Project page](http://naturalhistorymuseum.github.io/inselect).

## Windows development environment

- Install [git](http://git-scm.com/download/win) ;
- Download the latest build of [Anaconda](https://store.continuum.io/cshop/anaconda/), Python 2.7.x build, and install using default options;
- Install PySide

    conda install PySide

- Download [OpenCV 2.4.10](http://opencv.org/)

    * Extract OpenCV 2.4.10 to c:\opencv\
    * If you installed 32-bit Anaconda:

        copy C:\opencv\build\python\2.7\x86\cv2.pyd C:\Users\lawh\Anaconda\DLLs`

    * If you installed 64-bit Anaconda:

        copy C:\opencv\build\python\2.7\x64\cv2.pyd C:\Users\lawh\Anaconda\DLLs`

    * Test by start Anaconda prompt and running

        python -c "import cv2; print cv2"

- Get the Inselect source:
```shell
git clone https://github.com/NaturalHistoryMuseum/inselect.git
cd inselect
python inselect.py
```

## To build the Windows installer

```shell
pip install coverage cx_Freeze
build.bat
```

The installer will in the `dist` directory.

## OS X development environment

- Install [git](http://git-scm.com/download/mac) ;
- Download the latest build of [Anaconda](https://store.continuum.io/cshop/anaconda/), Python 2.7.x build, and install using default options ;
- Install precompiled OpenCV package:
```shell
conda install -c https://conda.binstar.org/jjhelmus opencv
```

- Install other dependencies:
```shell
conda install PySide
```

- Get the Inselect source:
```shell
git clone https://github.com/NaturalHistoryMuseum/inselect.git
cd inselect
./inselect.py
```

## To build the OS X installer

Install homebrew.

```shell
pip install pyinstaller
brew install upx
./build.sh
```

## Ubuntu 12.04-LTS development environment

```shell
apt-get install python-pip git python-pyside python-opencv python-numpy python-scipy python-matplotlib python2.7-dev
git clone https://github.com/NaturalHistoryMuseum/inselect.git
cd inselect
./inselect.py
```

## Barcode reading

Install [gouda](https://github.com/NaturalHistoryMuseum/gouda/) and either the
`libdmtx` or `Inlite` barcode engines. See `inselect/gui/plugins/barcode.py`.

## Toolbar icons in the compiled application,
If the toolbar icons in inselect/data change then you need to refresh a Python
file:
```shell
pyside-rcc icons.qrc > inselect/gui/icons.py
```
This taken from a [stackoverflow thread](http://stackoverflow.com/a/11547144)


## License

Inselect is Copyright (c) 2014, The Trustees of the Natural History Museum, London and licensed under the Modified BSD License. See the [LICENSE](https://github.com/NaturalHistoryMuseum/inselect/blob/master/LICENSE.md) file for more information.
