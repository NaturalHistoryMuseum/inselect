# Mac OS X development environment

# Install git

Download and run the [latest Mac OS X build of git](http://git-scm.com/download/mac).
Chose:

    * Use git from command prompt
    * Checkout as-is, commit as-is

Configure git:

```
git config --global user.name "<Your name>"
git config --global user.email <Your email address>
```

# Install a sensible text editor

I use [Sublime Text](http://www.sublimetext.com/).

**Whatever you use, set your editor to use Unix line endings and to insert
spaces in place of TABs**.

# Compilers and homebrew

* Install the XCode command line tools from the app store.
* Install [homebrew](http://brew.sh/).
* Install UPX:

```
brew install upx
```

# Code repos

Start a command prompt and run

```
cd C:\Users\<your Windows username>\
mkdir projects
cd projects
git clone https://<your git username>@github.com/NaturalHistoryMuseum/inselect.git
git clone https://<your git username>@github.com/NaturalHistoryMuseum/gouda.git
```

# Paths

Append to `~/.bashrc`:

```
PYTHONPATH=/Users/lawh/projects/inselect;/Users/lawh/projects/gouda
```

## Install dependencies and useful tools

```
cd ~/projects
pip install nose Markdown
pip install cx_Freeze
conda install -c https://conda.binstar.org/jjhelmus opencv
conda install pyside
conda install Pillow
pip install pyinstaller
pip install -r inselect\requirements.txt
pip install -r gouda\requirements.txt
```

## Install Barcode readers

## LibDMTX barcode reading library

* Get source

```
git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx
git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-wrappers
git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-utils
```

* Build core library

```
cd libdmtx
git checkout v0.7.4
./autogen.sh
./configure
make
make install
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

## ZBar barcode reading library
The `conda install` build of zbar on my Mac resulted in a segfault on `import zbar`.
I compiled zbar-0.10.tar.bz2 from [source](http://zbar.sourceforge.net/download.html)
and then ran `pip install zbar`.
Test

```
python -c "import zbar; print(zbar)"
```

# Unit tests

```
cd ~/projects/gouda/
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=gouda

cd ~/projects/inselect/
nosetests --with-coverage --cover-html --cover-inclusive --cover-erase --cover-tests --cover-package=inselect
```
