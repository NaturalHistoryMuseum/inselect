# Inselect

A tool for the semi-automated segmentation and annotation of specimen trays.

Project page: http://naturalhistorymuseum.github.io/inselect

## Installation under Microsoft Windows

We provide Microsoft Windows installer packages which can be found [on our downloads page](). Once installed, Inselect will be available in your Programs Menu. You will need to install the [Microsoft Visual C++ 2008 Redistributable Package](http://www.microsoft.com/en-us/download/details.aspx?id=29) as well - however this is usually already included on your operating system, so only download it if Inselect fails to start.

If you would like to install the project from source on Windows, you will need to:

- Install [git](http://git-scm.com/download/win) ;
- Download the latest build of [Anaconda](https://store.continuum.io/cshop/anaconda/), Python 2.7.x build, and install using default options;
- Download [OpenCV](http://opencv.org/downloads.html) (You want a 2.x version) and extract the archive ;
- Copy the file `<open cv extract root>/build/python/2.7/x86/cv2.pyd` to `<anaconda root>/Lib/site-packages` (Replace x86 by 64 as appropriate) ;
- Open an Anaconda Shell and run `pip install -e git+https://github.com/NaturalHistoryMuseum/inselect.git#egg=inselect`.

From the Anaconda Shell you can now run Inselect by typing `inselect.exe`, and the source code is in `src\inselect`. If you would like to create a Microsoft Installer package, you can do the following:

- Open an Anaconda shell and run (the first time) `pip install cx_Freeze`;
- cd into `src/inselect` and run `python setup.py bdist_msi`.

The installer can be found in the `dist` subdir.

## Installation under OS X

We do not provide ready-built binaries for OS X. These build instructions will install inselect within a local anaconda environment.

- Install [git](http://git-scm.com/download/mac) ;
- Download the latest build of [Anaconda](https://store.continuum.io/cshop/anaconda/), Python 2.7.x build, and install using default options ;
- Install [OpenCV](http://opencv.org/):

```shell
~/anaconda/bin/conda install -c https://conda.binstar.org/jjhelmus opencv
```

- Install other dependencies:

```shell
~/anaconda/bin/conda install PySide
~/anaconda/bin/pip install docopt
```

- Install inselect source:

```shell
~/anaconda/bin/pip install -e git+https://github.com/NaturalHistoryMuseum/inselect.git#egg=inselect
```

- Run inselect:

```shell
~/anaconda/bin/inselect
```

## Installation under Linux (Global)

We do not provide ready-built binaries for Linux. These build instructions will install inselect globally on Ubuntu 12.04-LTS. If you wish to install inselect in a virtual environment, see the instructions in the next section.

```shell
apt-get install python-pip git python-pyside python-opencv python-numpy python-scipy python-matplotlib python2.7-dev
pip install git+https://github.com/NaturalHistoryMuseum/inselect.git#egg=inselect
```

You can then run inselect simply with:

```shell
inselect
```

## Installation undex Linux (Virtual environment)

These instructions are for Ubuntu 12.04-LTS. Note that there is no functioning build script for OpenCV at this stage, we install globally and copy it into the virtual environment.

```shell
apt-get install python-pip git cmake python2.7-dev python-opencv
apt-get build-dep python-matplotlib
apt-get build-dep python-pyside
apt-get build-dep python-scipy

pip install virtualenv
virtualenv inselect
cd inselect
. bin/activate
cp /usr/lib/pymodules/python2.7/cv* ./lib/python2.7/site-packages

pip install git+https://github.com/NaturalHistoryMuseum/inselect.git#egg=inselect
```

From within the virtual environment, you can then run inselect with:

```shell
inselect
```
## License

Inselect is Copyright (c) 2014, The Trustees of the Natural History Museum, London and licensed under the Modified BSD License. See the [LICENSE](https://github.com/NaturalHistoryMuseum/inselect/blob/master/LICENSE.md) file for more information.
