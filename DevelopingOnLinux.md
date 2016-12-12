# Inselect on Linux

Tested on Ubuntu 12.04, 14.04 and 16.04, all with 2GB RAM.
Inselect runs on Python 3.4 or later and OpenCV 3.
While Ubuntu provides a `deb` package for Python 3, it does not provide
(at time of writing) a `deb` package of Python 3 bindings for `OpenCV`.
For these reasons, and to provide a consistent environment among distributions,
we recommend using
[Continuum's Miniconda](http://conda.pydata.org/miniconda.html) as shown below.
To run Inselect with system packages, you will need to compile OpenCV.

# Install Miniconda

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/Miniconda3-latest-Linux-x86_64.sh
bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
rm /tmp/Miniconda3-latest-Linux-x86_64.sh

export PATH=~/miniconda3/bin:$PATH
conda update --yes conda
```

# Inselect env

```
conda env create -f inselect.yml
source activate inselect
pip install -r requirements.pip
```

## Install and test barcode reading libraries

Inselect has optional barcode reading capabilities. The dependent libraries
can be installed with

```
sudo apt-get install libzbar-dev libdmtx0a
```

Test

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

Ubuntu 16.04 appears to come with `nose` already installed so the
`pip2 install -r requirements.pip` step above will not install `nose` within
the virtual env. `nosetests` will not find the packages within the
virtualenv and you will see lots of `ImportErrors`. If this is the case, run

```
python -m nose --verbose --with-coverage --cover-inclusive --cover-tests --cover-package=inselect inselect
```

Run inselect

```
python -m inselect.scripts.inselect
```
