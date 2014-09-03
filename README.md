# Inselect

A tool for the semi-automated segmentation and annotation of specimen trays.

## Requirements

- numpy (>= 1.6)
- scikit-image (>= 0.10)
- opencv (>= 2.4)

## Installation under OSX

- Install Anaconda
- Install OpenCV:

    conda install -c https://conda.binstar.org/jjhelmus opencv
    conda install pyside

## Installation under Linux (Global)

We do not provide ready-built binaries for Linux. These build instructions will install inselect globally on Ubuntu 12.04-LTS. If you wish to install inselect in a virtual environment, see the instructions in the next section.

```shell
apt-get install python-pip git python-pyside python-opencv python-numpy python-scipy python-matplotlib python2.7-dev
pip install git+https://github.com/vls-lab/inselect.git#egg=inselect
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

pip install git+https://github.com/vls-lab/inselect.git#egg=inselect
```

From within the virtual environment, you can then run inselect with:

```shell
inselect
```
